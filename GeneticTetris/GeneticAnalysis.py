'''
Created on 01/12/2011

@author: dev
'''

from GeneticTetris import TetrisOrganism, GeneLocus
from TetrisGenomeExample import TetrisGenomeExample
from CachedFilePlayer import CachedFilePlayer
from types import DictType
import aitetris
import sys  
import time

if sys.platform == 'win32':
    _timer = time.clock
else:
    _timer = time.time

class GeneticAnalisys:
    
    def __init__(self):
        self.geneticList = []
        self.height = 20
        self.width = 8
        self.gameFile = "database/TetrisGame.txt"
        self.filePlayer = CachedFilePlayer(self.gameFile)
        
    def addIndividual(self, id, chromosome):
        if type(chromosome) == DictType:
            chromosome = TetrisOrganism.dictToList(chromosome)
        if (len(chromosome) == GeneLocus.RANGE):
            self.geneticList.append((id, chromosome))
        else:
            print "Ignoring chromosome: ", id, chromosome

    def run(self):
        self.gameData = self.filePlayer.getCacheData()
        self.numTetroTypes = len(self.gameData)
        bestIndividual = self.geneticList[0]
        bestScore = -1
        for individual in self.geneticList:
            print "Testing :", individual[0]  
            score = aitetris.play(self.height, self.width, individual[1], 
                                  self.gameData, self.numTetroTypes)
            print "Score...:", individual[0], score 
            if score > bestScore:
                bestScore = score
                bestIndividual = individual
        print "BEST SCORE:", bestScore, bestIndividual[0], bestIndividual[1] 
    
    def multipleGames(self, n, dice, numTetroType):
        self.gameData = self.filePlayer.getCacheData()
        self.numTetroType = numTetroType
        bestIndividual = self.geneticList[0]
        bestScore = -1
        victoryCount = {}
        for i in xrange(len(self.geneticList)):
            victoryCount[self.geneticList[i][0]] = 0
        for game in xrange(n):
            print "Sorting tetromino sequence..."
            t = _timer()
            dice(numTetroType)
            elapsed = _timer() - t
            print "Time to sorting =", elapsed 
            self.gameData = self.filePlayer.getCacheData()
            gameBestIndividual = self.geneticList[0]
            gameBestScore = -1
            for individual in self.geneticList:
                t = _timer()
                print game, " - Testing:", individual[0]  
                score = aitetris.play(self.height, self.width, individual[1], 
                                      self.gameData, numTetroType)
                elapsed = _timer() - t
                print game, " - Score..:", individual[0], score, " time=", elapsed 
                if score > gameBestScore:
                    gameBestScore = score
                    gameBestIndividual = individual
                if score > bestScore:
                    bestScore = score
                    bestIndividual = individual
            victoryCount[gameBestIndividual[0]] += 1
            print "Game " + str(game) + " best score:", gameBestScore, gameBestIndividual[0], gameBestIndividual[1] 
        print "BEST SCORE:", bestScore, bestIndividual[0], bestIndividual[1]
        print victoryCount 
    
if __name__ == "__main__":
    
    test = GeneticAnalisys()
#    test.addIndividual("x01",[-83.65990179129726, 15.052979381918519, -27.142923708353706, -29.297816088940355, -2.209856824766354, -56.62642170834119, -32.50683262555, -32.39159621025992])
#    test.addIndividual("x02",[-44.21572072104753, 3.2779347700182315, -4.485825248530362, -8.160616473467108, -19.597291314906805, -76.97866997513479, -72.22018309090282, -34.3850881783179])
#    test.addIndividual("x03",[-0.03379908949437871, -0.46847677345020333, 0.28274809557508795, 0.032468373548663165, 0.038337956111531235, -0.18388640556189328, -0.5079823424225695, -0.9010797224549004, -0.2720440602251979])
#    test.addIndividual("x04",[-1.3820282920367188, -6.047820563211421, 0.477749978085511, 2.500707942987316, 3.079986486230867, -1.2706377879221586, -8.091479122413238, -6.271291338580008, -2.544149577501692])
#    test.addIndividual("x05",[0.8289823664499232, -434.1804410212419, 140.89941910933513, 63.91082037152218, 246.773757267982, -274.5849939579971, -834.106533899265, -822.548697541376, -316.2370057636458])
#    test.addIndividual("x06",[0.0, -56.34441992955155, 0.0, 0.0, 25.160002295790907, -21.073885962160432, -70.94291300255718, -81.7541860917633, -30.529664695917972])
#    test.addIndividual("x07",[-1.4421225345650157, -3.8602859438140413, 0.4002540059522597, 8.413785055545942, 0.0, -2.358826409207584, -9.675590700170662, -8.108212951073103, -2.768808413642356])
#    test.addIndividual("x08",[-1.2200218605428148, -44.39301752824289, 28.70243420215406, 26.67657980669874, 0.0, -20.27555836019343, -66.32271763635006, -79.99666384756011, -34.735461908200165])
#    test.addIndividual("09",[5.671504912205824, -9.49592892788563, 2.01539413359251, -8.37674001734818, 2.9089163698839204, -2.3118950065170125, -8.932548918392895, -8.247085669016204, -2.8006237653192523])
#    test.addIndividual("x10",[-0.3742079080556593, -6.055521800282635, 0.0, 0.0, 0.47785880520100754, -2.5986111747379192, -4.25649166520135, -8.251165407066619, -1.1584615489993162])
#    test.addIndividual("11",[0.0, -2, 0.0, 0.0, 1, -1, -5, -4, -2])
#    test.addIndividual("12",[0.0, -1, 0.0, 0.0, 1, -1, -1, -1, 0])
#    test.addIndividual("13",[0.0, -1, 0.0, 0.0, 0, -1, -2, -2, -1])
#    test.addIndividual("14",[0.0, -3, 0.0, 0.0, -1, -2, -5, -5, -2])
#    test.addIndividual("20",[-1, -1, 0.0, 0.0, 1, -1, -4, -3, -2])
#    test.addIndividual("15",[1.6023347691738383, -6.095409479837761, -3.5503569518897526, 1.4006201739553852, 2.8230263863575615, -2.5994577625000854, -7.510058150749968, -7.521172198773456, -4.305339873482652])
#    test.addIndividual("16",[-3.905994236724011, -7.928067336680571, -5.037497580060737, -6.443569239637359, 6.490951869486111, -2.037486960722463, -6.095005606987982, -8.755796541418482, -5.900543200723951])
#    test.addIndividual("17",[-3.175196574776802, -4.458137573866969, -6.200869563251383, -8.863020621540139, 7.2794026688404365, -2.2614358777098387, -3.950959049564604, -9.62881957370171, -2.901174292961583])
    test.addIndividual("SZR",[99.68460465396407, -45.73430286504265, 31.79062306116279, 98.20340577309378, -9.285784921471944, 13.506876614498339, -93.51310760128506, -54.45437830207589, -88.03546571266037])
    test.addIndividual("SZI",[0.0, -2, -1, 0, 0.0, 2, -5, -4, -5])
    test.addIndividual("SZR2",[45.1362768269496, -45.808368938957635, -14.202197727503105, 75.7375462470144, -5.527659262751229, 26.94780368906946, -81.76622331990022, -74.028993387458, -56.43604288298643])
    test.addIndividual("SZR3",[3.0808565927191083, -5.269882351960793, -1.8382574108506144, 1.0501037127603254, -1.8288077114653198, 3.130367202039226, -7.4451498006137795, -9.208655761294953, -8.01328739119027])
    test.addIndividual("SZR4",[4.519056360531808, -3.9656485066737, -4.64786021273397, -1.8978671581722253, 3.867017478306934, 2.6262155683873374, -4.855565996475444, -8.82065417244946, -8.940028832899946])
    test.addIndividual("SZR5",[-0.2239107425146063, 0.11926946272005878, -2.8022019274518435, -6.485110318656002, 6.681160798278519, -5.943938400097586, -4.58939486226458, -9.92794585498514, -6.046799095661219])
#    test.addIndividual("Eltetris",TetrisOrganism.dictToList(TetrisGenomeExample.Eltetris))
#    test.addIndividual("04",[ -1, -1, 0.0, 0.0, +1, -1, -4, -3, -2])
#    test.addIndividual("HEIGHT",[-0.1, -1, 0.0, 0.0, +1, -1, -1, -4, -1])
#    test.addIndividual("PierreDellacherie",TetrisOrganism.dictToList(TetrisGenomeExample.PierreDellacherie))
#    test.addIndividual("ThieryScherrer",TetrisOrganism.dictToList(TetrisGenomeExample.ThieryScherrer))
#    test.addIndividual("PyEvolve1",TetrisOrganism.dictToList(TetrisGenomeExample.PyEvolve1))
#    test.addIndividual("Teste10",[-22.53713416296894, -31.396409569793107, -74.73342511145393, 2.49795653742612, 0.49482223271648706, -19.516051225660163, -98.72514821724174, -73.37489814420404, -10.639777550437856])
#    test.addIndividual("Teste11",[2.667493739734523, -6.9309509423553095, -5.304539752800432, -7.954554446697244, 2.996760400525666, -1.7255603353824434, -7.406603237124926, -9.185020766778875, -0.9422132771658092])
#    test.addIndividual("Teste13",[2.595883487514607, -3.5312610838234875, -8.217237241847787, 2.9536303834831283, 2.137691065590184, -1.7945639054268785, -9.04662418316981, -2.203730161513528, -0.2692343602843543])
#    test.addIndividual("Teste15",[3.9342674926688375, -6.0662700310020545, -6.762210811584195, -8.678686665688469, 3.7959481865766413, -1.868919037439781, -8.78693457135703, -8.769305387138626, -1.6041351809587212])
#    test.addIndividual("Teste14",[27.306006511940325, -60.56146346900497, -22.385290866567757, -53.7231424470368, 8.409708397033299, -16.4524650693119, -66.32112844050133, -95.35229934550253, -8.014057188301436])
#    test.addIndividual("Teste17",[-0.43672817550544707, -3.115158697424187, -4.794446018411245, 5.76262543036192, 0.83917405157624, -2.197691582028396, -8.626487498117648, -7.121189575256239, -1.4500159437079105])
    #test.run()
    test.multipleGames(100, test.filePlayer.generateRandomSZGame, 100000)
    
    