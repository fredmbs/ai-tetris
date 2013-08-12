# -*- coding:utf-8 -*-
from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import DBAdapters
from pyevolve import Initializators, Mutators
from pyevolve import GAllele
from time import time
import aitetris
from GeneticTetris import GeneLocus
from types import BooleanType
import os.path
from CachedFilePlayer import CachedFilePlayer

class PyEvolveTetris:

    def __init__(self, id = "default", numTetros = 1000000):
        self.id = id
        self.scoreSum = 0
        self.resetDB = False
        self.gameFile = "database/TetrisGame.txt"
        self.height = 20
        self.width = 10
        self.filePlayer = CachedFilePlayer(self.gameFile)
        self.filePlayer.generateRandomSZGame(numTetros)
        self.gameData = self.filePlayer.getCacheData()
        self.numTetroTypes = len(self.gameData)
        self.logFile = "database/PyEvolve." + id + ".txt"
        ''' try to create a new file, insted append '''
        tmp = 1
        while os.path.exists(self.logFile):
            self.logFile = "database/PyEvolve." + id + "_" + str(tmp) + ".txt"
            tmp += 1
            if (tmp > 100):
                raise Exception("Too many evolution log files of " + id)
        self.__hfile = open(self.logFile, 'a')
        self.__generation = 0;
        self.mutation = 0.02
        self.crossover = 0.9
        self.setChangeGenerationGame(False)
        self.resetAllGeneRange(0.0, 10.0, True)
        self.configure(1, 10, 10)
        
    def callback_generation(self, ga_engine):
        if self.__changeGenerationGame:
            print "Changing next generation game..."
            self.filePlayer.generateRandomSZGame(self.numTetroTypes)
            self.gameData = self.filePlayer.getCacheData()
            self.numTetroTypes = len(self.gameData)
        self.__generation = ga_engine.getCurrentGeneration() + 1
        
    def eval_func(self, genome):
        chromosome = [i for i in genome]
        score = aitetris.play(self.height, self.width, chromosome, 
                              self.gameData, self.numTetroTypes)
        self.scoreSum[self.__generation] += score;
        log = str(self.__generation) + "," + str(score)
        print log
        self.__hfile.write(str(score)+":"+str(chromosome)+"\n")
        return score
    
    def setResetDB(self, reset):
        self.resetDB = reset

    def setChangeGenerationGame(self, value):
        if type(value) != BooleanType:
            raise Exception("value must be a boolean")
        self.__changeGenerationGame = value

    def resetAllGeneRange(self, begin, end, real):
        ''''''
        if begin == end:
            raise Exception("Gene range invalid")
        
        if (begin > end):
            tmp = begin
            begin = end 
            end = tmp
            
        if (begin < 0) and (end > 0):
            begin_c = begin
            end_c = end
        elif (begin >= 0) and (end > 0):
            begin_c = -end
            end_c = begin
        elif (begin < 0) and (end <= 0):
            begin_c = end
            end_c = -begin
        elif (begin >= 0) and (end < 0):
            raise Exception("It is impossible here")
            
        self.allelle = []
        #PileHeight          = 0
        self.allelle.append({"begin": begin_c, "end": end_c, "real": real})
        #LandingHeight       = 1
        self.allelle.append({"begin": begin_c, "end": end_c, "real": real})
        #ErodedPieces        = 2
        self.allelle.append({"begin": begin, "end": end, "real": real})
        #ErodedRows          = 3
        self.allelle.append({"begin": begin, "end": end, "real": real})
        #ErodedMetric        = 4
        self.allelle.append({"begin": begin, "end": end, "real": real})
        #RowTransitions      = 5
        self.allelle.append({"begin": begin_c, "end": end_c, "real": real})
        #ColumnTransitions   = 6
        self.allelle.append({"begin": begin_c, "end": end_c, "real": real})
        #ColumnBuriedHoles   = 7
        self.allelle.append({"begin": begin_c, "end": end_c, "real": real})
        #ColumnWells         = 8
        self.allelle.append({"begin": begin_c, "end": end_c, "real": real})
    
    def setGeneRange(self, locus, begin, end, real):
        ''''''
        if (begin == end) and (not real):
            raise Exception("Gene range invalid")
        
        if (begin > end):
            tmp = begin
            begin = end 
            end = tmp

        self.allelle[locus] = {"begin": begin, "end": end, "real": real}

    def getGeneRange(self, locus):
        return GAllele.GAlleleRange(begin = self.allelle[locus]["begin"],
                                    end   = self.allelle[locus]["end"],
                                    real  = self.allelle[locus]["real"])

    def configure(self, preserve, population, generations):
        self.preserve = preserve
        self.population = population
        self.generations = generations

    def setElitism(self, preserve):
        self.preserve = preserve

    def setPopulation(self, population):
        self.population = population

    def setGenerations(self, generations):
        self.generations = generations
        
    def setMutation(self, rate):
        self.mutation = rate
        
    def setCrossover(self, rate):
        self.crossover = rate
        
    def run(self):
        
        # score control
        self.scoreSum = [0 for i in xrange(self.generations + 1)]
        self.__generation = 0;
        
        # configure alleles
        setOfAlleles = GAllele.GAlleles()
        for i in xrange(GeneLocus.RANGE):
            setOfAlleles.add(self.getGeneRange(i))
        
        # Genome instance, 1D List of GeneLocus.RANGE elements
        genome = G1DList.G1DList(GeneLocus.RANGE)
    
        # Sets the range max and min of the 1D List
        genome.setParams(allele=setOfAlleles, full_diversity=True)
        genome.mutator.set(Mutators.G1DListMutatorAllele)
        genome.initializator.set(Initializators.G1DListInitializatorAllele)
        #genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
        # The evaluator function (evaluation function)
        genome.evaluator.set(self.eval_func)
    
        # Genetic Algorithm Instance
        ga = GSimpleGA.GSimpleGA(genome)
        ga.stepCallback.set(self.callback_generation)
        #ga.setMultiProcessing()
    
        # Set the Roulette Wheel selector method, the number of generations and
        # the termination criteria
        ga.selector.set(Selectors.GRouletteWheel)
        ga.setElitism(True)
        ga.setElitismReplacement(self.preserve)
        ga.setPopulationSize(self.population)
        ga.setGenerations(self.generations)
        ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
        ga.setMutationRate(self.mutation)
        ga.setCrossoverRate(self.crossover)
    
        # Sets the DB Adapter, the resetDB flag will make the Adapter recreate
        # the database and erase all data every run, you should use this flag
        # just in the first time, after the pyevolve.db was created, you can
        # omit it.
        #sqlite_adapter = DBAdapters.DBSQLite(identify=self.id, resetDB=True)
        sqlite_adapter = DBAdapters.DBSQLite(identify=self.id, resetDB=self.resetDB)
        ga.setDBAdapter(sqlite_adapter)
    
        # Do the evolution, with stats dump
        # frequency of 20 generations
        ga.evolve(freq_stats=1)
        ga.printStats()
    
        # Show results
        report = "Configuration: \n" +  \
                 "ID................. = " + str(self.id) + " \n" +  \
                 "Elitism............  = " + str(self.preserve) + " \n" +  \
                 "Population......... = " + str(self.population) + " \n" +  \
                 "Generations........ = " + str(self.generations) + " \n" + \
                 "Mutation rate...... = " + str(self.mutation) + " \n"
                 
        if self.__changeGenerationGame:
            report += "Diferent generations games \n"
        else: 
            report += "Same generations games \n"
                
        bestGeneration = 0
        bestGenerationScore = 0
        for i in xrange(self.generations):
            if bestGenerationScore < self.scoreSum[i]:
                bestGeneration = i
                bestGenerationScore = self.scoreSum[i]
                
            report += "  - Score generation " + str(i) + " = " + \
                      str(self.scoreSum[i]) 
            if (i > 0): 
                percent = ((self.scoreSum[i] * 100) / self.scoreSum[i - 1]) - 100  
                report += "(" + str(percent) + "%) \n"
            else :
                report += " \n" 
                
        report += "Best generation = " + str(bestGeneration) + " \n"
                  
        print report
        print ga.bestIndividual()
        print ga.getStatistics()
        ga.printTimeElapsed()
        total_time = time() - ga.time_init
        self.__hfile.write(report)
        self.__hfile.write(str(ga.bestIndividual())+"\n")
        self.__hfile.write(str(ga.getStatistics()))
        self.__hfile.write("Total time elapsed: %.3f seconds.\n"%total_time)
        self.__hfile.close()
        
if __name__ == "__main__":
    # cria uma execução da evolução, identificando o banco de dados
    evolution = PyEvolveTetris("SZ", 1000000)
    # inicia os limites (min, max) dos genomas, 
    # informando que devem usar números reais (argumento True)
    evolution.resetAllGeneRange(-10, 10, True)
    # configura o limite (min, max) individualmente por gene
    #evolution.setGeneRange(GeneLocus.PileHeight, 0, 0, True)
    #evolution.setGeneRange(GeneLocus.ErodedPieces, 0, 0, True)
    #evolution.setGeneRange(GeneLocus.ErodedRows, 0, 0, True)
    #evolution.setGeneRange(GeneLocus.ErodedMetric, 0, 0, True)
    # informa se deve (True) ou não (False) alterar a sequencia de tetrominos
    # a cada nova geração
    #evolution.setChangeGenerationGame(True)
    # SELEÇÃO: informa quantos indivíduos devem ser preservados por elitismo 
    evolution.setElitism(20)
    # informa o tamanho da população que deve ser mantida ao longo das gerações
    evolution.setPopulation(100)
    # informa a taxa de mutação aplicada entre as gerações
    evolution.setMutation(0.01)
    # informa o número de gerações que devem ser executadas
    evolution.setGenerations(200)
    evolution.setResetDB(True)
    # executa a evolução
    evolution.run()


