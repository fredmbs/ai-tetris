# -*- coding:utf-8 -*-

#import threading
from TetrisGame import TetrisEvent, TetrisGame
from TerminalPlayer import TerminalPlayer 
from CachedFilePlayer import CachedFilePlayer
from StatisticPlayer import StatisticPlayer
from TetrisAI import TetrisAI
from AIPlayer import AIPlayer
import threading

class AIThreadPlayer(AIPlayer, threading.Thread):
    
    def __init__(self):
        self.__autoControl = False
        self.__thinking = False 
        self.__running = False
        self.__ = False
        self.__suggest = threading.Event()
        threading.Thread.__init__(self)
        self.cnt = 0
                
    def bind(self, game):
        pass        
        
    def unbind(self, game):
        pass        
        
    def setAutoControl(self, isAutoControled = False):
        self.__autoControl = isAutoControled
        
    def start(self):
        threading.Thread.start(self)
        self.__running = True
        self.__thinking = False
    
    def stop(self):
        self.__running = False
        self.__thinking = True
        self.__suggest.clear()
        
    def configure(self, game):
        self.__game = game
        self.__tetromino = game.getTetromino() 
        self.__board = game.getBoard() 
        self.__height, self.__width  = self.__board.getSize()
        self.__maxRow, self.__maxCol = self.__height - 1, self.__width - 1 
        self.__ai = TetrisAI(self.__board, self.__tetromino)
        game.eventRegistry(self, [TetrisEvent.TETROMINO_START], 
                           self.__suggestMove)
        game.eventRegistry(self, [TetrisEvent.GAME_START], 
                           self.__gameStart)
        game.eventRegistry(self, [TetrisEvent.GAME_OVER], 
                           self.__gameOver)
        if self.__autoControl and (not self.__running):
            self.start()
            
    def getId(self):
        return self.__ai.getGenome().getId()
    
    def getAI(self):
        return self.__ai
    
    def play(self):
        self.__suggest.clear()
        if self.__thinking:
            return False
        self.__thinking = True
        try:
            dr, dx = self.__ai.play()
            self.__game.enforceGravity()
            for __ in xrange(abs(dr)):
                self.__game.rotationCcw()
            if dx >= 0:
                for __ in xrange(dx):
                    self.__game.right()
            else:
                for __ in xrange(abs(dx)):
                    self.__game.left()
            self.__game.drop()
        finally:
            self.__thinking = False
            return True

    def __suggestMove(self, arg):
        if self.__running:
            self.__suggest.set()
            
    def __gameStart(self, arg):
        self.__thinking = False
        self.__running = True
        self.__suggest.clear()
            
    def __gameOver(self, arg):
        self.__thinking = False
        self.__running = False
        self.__suggest.clear()
        if self.__autoControl:
            self.stop()

    def run(self):
        while True:
            self.__suggest.wait()
            self.play()
                
if __name__ == '__main__':
    playerAI = AIThreadPlayer()
    playerStatistics = StatisticPlayer()
    playerStdout = TerminalPlayer(playerStatistics)
    playerFile = CachedFilePlayer("database/TetrisGame.txt")
    game = TetrisGame(22, 10, "AI TEST")
    game.appendPlayer(playerAI)
    game.appendPlayer(playerStdout)
    game.appendPlayer(playerStatistics)
    game.appendPlayer(playerFile)
    playerAI.setAutoControl(True)
    game.play()
    playerAI.join(600)
    playerStatistics.show()
    game.removePlayer(playerFile)
    game.removePlayer(playerStatistics)
    game.removePlayer(playerStdout)
                    
