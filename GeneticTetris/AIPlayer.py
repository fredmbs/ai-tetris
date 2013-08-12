# -*- coding:utf-8 -*-

#import threading
from TetrisGame import TetrisGame, TetrisEvent
from TetrisAI import TetrisAI
from TetrisPlayer import TetrisPlayer
from CachedFilePlayer import CachedFilePlayer 
from StatisticPlayer import StatisticPlayer

#import multiprocessing

class AIPlayer(TetrisPlayer):
    
    def __init__(self):
        self.active = False
        
    def configure(self, game):
        self.__game = game
        self.__tetromino = game.getTetromino() 
        self.__board = game.getBoard() 
        self.__height, self.__width  = self.__board.getSize()
        self.__maxRow, self.__maxCol = self.__height - 1, self.__width - 1 
        self.__ai = TetrisAI(self.__board, self.__tetromino)
        self.active = True
        game.eventRegistry(self, [TetrisEvent.GAME_OVER], 
                           self.__gameOver)
    def getId(self):
        return self.__ai.getGenome().getId()
    
    def getAI(self):
        return self.__ai
    
    def play(self):
        dr, dx = self.__ai.play()
        self.__game.enforceGravity()
        for i in xrange(abs(dr)):
            self.__game.rotationCcw()
        if dx >= 0:
            for i in xrange(dx):
                self.__game.right()
        else:
            for i in xrange(abs(dx)):
                self.__game.left()
        self.__game.drop()

    def __gameOver(self, arg):
        self.active = False
        #TerminalPlayer.drawBoard(self.__board)

def playGame(name):
    playerAI = AIPlayer()
    playerFile = CachedFilePlayer("database/TetrisGame.txt")
    playerStatistics = StatisticPlayer()
    game = TetrisGame(20, 10, name)
    game.appendPlayer(playerAI)
    game.appendPlayer(playerStatistics)
    game.appendPlayer(playerFile)
    print "PLAYING " + name
    game.play()
    while playerAI.active:
        playerAI.play()
    playerStatistics.show()
    game.removePlayer(playerFile)
    game.removePlayer(playerStatistics)
    game.removePlayer(playerAI)
    print "GAME " + name + " IS OVER"

if __name__ == '__main__':
    
    playGame("Teste")
    
#    n = multiprocessing.cpu_count()
#    print "CPU COUNT         = ", n
#    p = []
#    n = max(n - 1, 1)
#    print "PROCESS TRIGGERED = ", n
#    for i in xrange(n):
#        gameName = "Teste " + str(i)
#        p.append(multiprocessing.Process(target=playGame, args=(gameName,)))
#    
#    for i in xrange(n):
#        p[i].start()
#        
#    for i in xrange(n):
#        p[i].join()
