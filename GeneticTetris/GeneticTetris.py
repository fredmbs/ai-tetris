# -*- coding:utf-8 -*-
'''
Created on 17/11/2011

@author: dev
'''

from Tetromino import Tetromino
from TetrisGame import TetrisGame
from CachedFilePlayer import CachedFilePlayer 
import aitetris 
import sys
import time

if sys.platform == 'win32':
    _timer = time.clock
else:
    _timer = time.time


#from TerminalPlayer import TerminalPlayer 

''' Genotype of tetris organism '''
class GeneLocus:
    
    # list of genes by traits used in genetic algorithm 
    PileHeight          = 0
    LandingHeight       = 1
    ErodedPieces        = 2
    ErodedRows          = 3
    ErodedMetric        = 4
    RowTransitions      = 5
    ColumnTransitions   = 6
    ColumnBuriedHoles   = 7
    ColumnWells         = 8
    RANGE               = 9

class TetrisOrganism:
    '''Individual'''
    
    ''' Individual - Any possible solution
        Population - Group of all individuals
        Search Space - All possible solutions to the problem
        Chromosome - Blueprint for an individual
        Trait - Possible aspect of an individual
        Allele - Possible settings for a trait
        Locus - The position of a gene on the chromosome
        Genome - Collection of all chromosomes for an individual
    '''
    
    __defaultGenome = [5.671504912205824, -9.49592892788563, 
                       2.01539413359251, -8.37674001734818, 
                       2.9089163698839204, -2.3118950065170125, 
                       -8.932548918392895, -8.247085669016204, 
                       -2.8006237653192523]
    __default_id = "Defalut"
    
    def __init__(self):
        #self.__chromosome = [0 for i in xrange(GeneLocus.RANGE)]
        self.__chromosome = TetrisOrganism.__defaultGenome 
        self.__id = TetrisOrganism.__default_id 
        #self.setGenome(TetrisGenomeExample.PyEvolve1)
        #self.setGenome(TetrisGenomeExample.PierreDellacherie)
        #self.setGenome(TetrisGenomeExample.Eltetris)
        #self.setGenome(TetrisGenomeExample.ThieryScherrer)
        
        #self.__hfile = open("debug_python.txt", 'w')
        #self.__count = 0

    @staticmethod 
    def setDefaultGenome(genome, id = "Unknown"):
        from types import DictType, ListType
        if (type(genome) == DictType):
            genome = TetrisOrganism.dictToList(genome)
        if (type(genome) != ListType):
            raise Exception("Genome must be a list or a dict.")
        if (len(genome) != GeneLocus.RANGE):
            raise Exception("Genome size is invalid")
        TetrisOrganism.__defaultGenome = genome
        TetrisOrganism.__default_id = id

    @staticmethod 
    def dictToList(chromosome):
        genome = [0 for i in xrange(GeneLocus.RANGE)]
        if "PileHeight" in chromosome:
            genome[GeneLocus.PileHeight]        = chromosome["PileHeight"]
        if "LandingHeight" in chromosome:
            genome[GeneLocus.LandingHeight]     = chromosome["LandingHeight"]
        if "ErodedPieces" in chromosome:
            genome[GeneLocus.ErodedPieces]      = chromosome["ErodedPieces"]
        if "ErodedRows" in chromosome:
            genome[GeneLocus.ErodedRows]        = chromosome["ErodedRows"]
        if "ErodedMetric" in chromosome:
            genome[GeneLocus.ErodedMetric]      = chromosome["ErodedMetric"]
        if "ErodedMetric" in chromosome:
            genome[GeneLocus.RowTransitions]    = chromosome["RowTransitions"]
        if "ColumnTransitions" in chromosome:
            genome[GeneLocus.ColumnTransitions] = chromosome["ColumnTransitions"]
        if "ColumnBuriedHoles" in chromosome:
            genome[GeneLocus.ColumnBuriedHoles] = chromosome["ColumnBuriedHoles"]
        if "ColumnWells" in chromosome:
            genome[GeneLocus.ColumnWells]       = chromosome["ColumnWells"]
        return genome

    @staticmethod 
    def listToDict(genome):
        chromosome = {}
        chromosome["PileHeight"]        = genome[GeneLocus.PileHeight]  
        chromosome["LandingHeight"]     = genome[GeneLocus.LandingHeight]  
        chromosome["ErodedPieces"]      = genome[GeneLocus.ErodedPieces] 
        chromosome["ErodedRows"]        = genome[GeneLocus.ErodedRows] 
        chromosome["ErodedMetric"]      = genome[GeneLocus.ErodedMetric] 
        chromosome["RowTransitions"]    = genome[GeneLocus.RowTransitions] 
        chromosome["ColumnTransitions"] = genome[GeneLocus.ColumnTransitions]
        chromosome["ColumnBuriedHoles"] = genome[GeneLocus.ColumnBuriedHoles] 
        chromosome["ColumnWells"]       = genome[GeneLocus.ColumnWells] 
        return chromosome 

    def setGenome(self, chromosome, id = "Unknown"):
        self.__chromosome = TetrisOrganism.dictToList(chromosome)
        self.__id = id
        
    def getGenome(self):
        return TetrisOrganism.listToDict(self.__chromosome) 
        
    def setId(self, id = "Unknown"):
        self.__id = id
        
    def getId(self):
        return self.__id 
        
    def getGameFileScore(self, game, gameFile, tetroCount):
        height, width = game.getBoardSize()
        score = aitetris.play_file(int(height), int(width), self.__chromosome, 
                                   gameFile, tetroCount)
        return score

    def getGameScore(self, game, sortedTetroTypes):
        height, width = game.getBoardSize()
        score = aitetris.play(int(height), int(width), self.__chromosome, 
                                  sortedTetroTypes, len(sortedTetroTypes))
        return score

    def getGameLines(self, game, sortedTetroTypes):
        height, width = game.getBoardSize()
        lines = aitetris.play_lines(int(height), int(width), self.__chromosome, 
                                    sortedTetroTypes, len(sortedTetroTypes))
        return lines

    #def getDropFitness(self, originalBoard, tetromino):
    def getDropFitness(self, originalBoard, tetromino):
        '''Reaction To The Environment'''

        # get informations of tetromino and board
        trow, tcol = tetromino.getPosition()
        trotation = tetromino.getRotation()
        tshape = tetromino.getShapeRotation(trotation)
        tetroType = tetromino.getType()
        height, width = originalBoard.getSize()
        
        # drop tetromino in trial board
        board = originalBoard.getCopy()
        landingRow = board.getDropTo(trow, tcol, tshape)
        shape = tetromino.getShapeAtRotation(landingRow, tcol, trotation)
        board.unsafeInsert(tetroType, shape)
        
        # calculate landing height 
        minRow, minCol, maxRow, maxCol = Tetromino.getBoundingRectangle(shape)
        landingHeight = (0.5) * (minRow + maxRow + 2)

        # calculate erosion: removed (1) lines and (2) pieces of tetromino        
        completedRows, pieceCellsEliminated = board.calculateErosion(shape)
        if completedRows > 0: 
            board.eliminateRows()
        # calculate erosion metric 
        erodedPieceCellsMetric = (completedRows * pieceCellsEliminated);

        # calculate board rows factors
        # -- board max pile height        
        pileHeight = board.calculatePileMaxHeight()
        # -- row transitions
        boardRowTransitions = 2 * (height - pileHeight)
        for row in xrange(pileHeight):
            rowT = board.calculateTransitionForRow(row)
            boardRowTransitions += rowT
        
        # calculate board colums factors 
        boardColumnTransitions = 0
        boardBuriedHoles = 0
        boardWells = 0
        for col in xrange(width):
            boardColumnTransitions += board.calculateTransitionForColumn(col)
            boardBuriedHoles += board.calculateBuriedHolesForColumn(col)
            boardWells += board.calculateAllWellsForColumn(col)    
            
        genome = self.__chromosome
        fitness = \
            (genome[GeneLocus.LandingHeight]     * landingHeight) + \
            (genome[GeneLocus.ErodedPieces]      * pieceCellsEliminated) + \
            (genome[GeneLocus.ErodedRows]        * completedRows) + \
            (genome[GeneLocus.ErodedMetric]      * erodedPieceCellsMetric) + \
            (genome[GeneLocus.RowTransitions]    * boardRowTransitions) + \
            (genome[GeneLocus.ColumnTransitions] * boardColumnTransitions) + \
            (genome[GeneLocus.ColumnBuriedHoles] * boardBuriedHoles) + \
            (genome[GeneLocus.ColumnWells]       * boardWells)

        return fitness 
    
    @staticmethod    
    def playGame(name):
        gameFile = "database/TetrisGame.txt"
        game = TetrisGame(20, 10, name)
        filePlayer = CachedFilePlayer(gameFile)
        tetris = TetrisOrganism()
        print "PLAYING " + name
        score = tetris.getGameScore(game, filePlayer.getCacheData())
        #score = tetris.getGameFileScore(game, gameFile, 10000000)
        print "GAME SCORE = " + str(score)

    @staticmethod    
    def playGameLines(name):
        gameFile = "database/TetrisGame.txt"
        game = TetrisGame(20, 10, name)
        filePlayer = CachedFilePlayer(gameFile)
        filePlayer.generateRandomGame(10000)
        tetris = TetrisOrganism()
        print "PLAYING " + name
        time = _timer()
        statistic = tetris.getGameLines(game, filePlayer.getCacheData())
        elapsed = _timer() - time
        lines = 0
        moviments = 0
        for i in xrange(5):
            print "Line[" + str(i) + "] = " + str(statistic[i])
            lines += (i * statistic[i])
            moviments += statistic[i]
        tetros = statistic[5]
        evaluations = statistic[6]
        print "Elapsed time      = ", elapsed
        print "Total tetrominos  = ", tetros, " -- ", tetros/elapsed, "tetrominos/second"
        print "Total lines       = ", lines, " -- ", lines/elapsed, "lines/second"
        print "Total moviments   = ", moviments, " -- ", moviments/elapsed, "moviments/second"
        print "Total evaluations = ", evaluations, " -- ", evaluations/elapsed, "evaluations/second"
        print "Average evaluations per trominos = ", float(evaluations)/float(tetros)
        print "GAME SCORE        = ", statistic[7]

    @staticmethod    
    def playFileGame(name):
        gameFile = "database/TetrisGame.txt"
        game = TetrisGame(20, 10, name)
        tetris = TetrisOrganism()
        print "PLAYING " + name
        score = tetris.getGameFileScore(game, gameFile, 10000000)
        print "GAME SCORE = " + str(score)

if __name__ == '__main__':
    import time
    t1 = time.time()
    tc1 = time.clock()
    TetrisOrganism.playGameLines("Teste")
    t2 = time.time()
    tc2 = time.clock()
    print "Elapsed time : ", t2-t1
    print "Elapsed clock : ", tc2-tc1

    