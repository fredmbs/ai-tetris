'''
Created on 18/11/2011

@author: dev
'''

import random
from TetrisPlayer import TetrisPlayer

class FilePlayer(TetrisPlayer):
    
    def __init__(self, fileName):
        self.fileName = fileName
        self.__hfile = NotImplemented
        self.__opened = False
        self.__oldGameDice = NotImplemented
        self.__oldGameName = ""
        self.__game = NotImplemented
        
    def bind(self, game):
        if self.__game == NotImplemented:
            self.__game = game
            self.__oldGameDice = game.getDice()
            self.__oldGameName = game.getName() 
            game.setName(self.fileName)
        
    def unbind(self, game):
        if self.__opened:
            self.__hfile.close()
        self.__opened = False
        game.setName(self.__oldGameName)
        game.setDice(self.__oldGameDice)        
        
    def configure(self, game):
        if self.__opened:
            self.__hfile.close()
        self.__hfile = open(self.fileName, 'r')
        self.__opened = True
        game.setDice(self.getNextTetromino)

    def getNextTetromino(self):
        if self.__opened:
            tetroTypeStr =  self.__hfile.read(1)
            if tetroTypeStr == "":
                self.__playing = False
            else:
                return int(tetroTypeStr)
        return 0 
        
    def generateRandomGame(self, n):
        if not self.__opened:
            self.__hfile = open(self.fileName, 'w')
            for i in xrange(n):
                tetroType = random.randint(1,7)
                self.__hfile.write(str(tetroType))
            self.__hfile.close()

    def generateRandomSZGame(self, n):
        if not self.__opened:
            self.__hfile = open(self.fileName, 'w')
            for i in xrange(n):
                tetroType = random.randint(3,4)
                self.__hfile.write(str(tetroType))
            self.__hfile.close()

if __name__ == '__main__':
    pass
#    print "Creating game file..."
#    fp = FilePlayer("database\TetrisGame_sz.txt")
#    fp.generateRandomSZGame(1000000)
#    print "File created!"
