'''
Created on 25/11/2011

@author: dev
'''
from TetrisPlayer import TetrisPlayer
from TetrisGame import TetrisGame, TetrisEvent

class StatisticPlayer(TetrisPlayer):

    def __init__(self):
        self.__game = NotImplemented
        self.__clear()
    
    def __clear(self):
        self.tetromino = 0
        self.tetroCount = [0 for __ in xrange(8)]
        self.totalTime = 0
        self.erodedRows = [0 for __ in xrange(5)]
        self.level = 0
        self.sumTime = 0  
        self.lastTetro = TetrisGame.osTimer()
        self.sumErodedRows = 0
        self.erodedRowsScoringFactors = [0, 40, 100, 3000, 1200]
        self.score = 0
        self.aiScore = 0
        self.downDelay = 1
        self.minDownDelay = 0.005
        self.blockedMoves = 0
        self.attractions = 0
        self.levelErodedRows = 20
        self.lastMoveTime = 0

    def configure(self, game):
        self.__game = game
        self.__clear()
        self.id = game.getName()
        game.setDownDelay(self.downDelay)
        game.eventRegistry(self, [TetrisEvent.TETROMINO_START], 
                           self.__tetrominoChange)
        game.eventRegistry(self, [TetrisEvent.BOARD_CHANGE], 
                           self.__boardChange)
        game.eventRegistry(self, [TetrisEvent.TETROMINO_BLOCKED], 
                           self.__tetrominoBloked)
        game.eventRegistry(self, [TetrisEvent.TETROMINO_GRAVITY], 
                           self.__tetrominoAttracted)
        
        
    def __tetrominoChange(self, arg):
        self.tetromino += 1
        self.tetroCount[arg] += 1
        timer = TetrisGame.osTimer()
        self.lastMoveTime = (timer - self.lastTetro)
        self.sumTime += self.lastMoveTime  
        self.lastTetro = timer
            
    def __tetrominoBloked(self, arg):
        self.blockedMoves += 1

    def __tetrominoAttracted(self, arg):
        self.attractions += 1

    def __boardChange(self, arg):
        rows = len(arg)
        self.erodedRows[rows] += 1
        self.sumErodedRows += rows
        level = int(self.sumErodedRows / self.levelErodedRows)
        if level > self.level:
            self.level = level
            if self.downDelay > self.minDownDelay:
                self.downDelay = max(self.minDownDelay, 
                                     self.downDelay - self.minDownDelay)
                self.__game.setDownDelay(self.downDelay)
        if rows > 0:
            self.score += self.erodedRowsScoringFactors[rows] * (self.level + 1)
            self.aiScore += self.erodedRowsScoringFactors[rows]
        
    def setLevelErodedRows(self, rows):
        self.levelErodedRows = rows
        
    def show(self):
        print "Game  =", self.id
        print "Score =", self.score
        print "AIScore =", self.aiScore
        print "Level =", self.level
        tetroCount = sum(self.tetroCount) - self.tetroCount[0] 
        print "Tretominoes         =", self.tetromino, "(", tetroCount, ")" 
        for i in xrange(1,len(self.tetroCount)):
            print "              [",i,"] =", self.tetroCount[i]
        erodedRows = sum(self.erodedRows) - self.erodedRows[0] 
        print "Eroded rows         =", erodedRows, "(", self.__game.getLines(), ")" 
        for i in xrange(len(self.erodedRows)):
            print "              [",i,"] =", self.erodedRows[i]
        print "Time spent          =", self.sumTime 
        print "Average time        =", self.sumTime / tetroCount
        print "Blocked moves       =", self.blockedMoves
        print "Gravity attractions =", self.attractions
