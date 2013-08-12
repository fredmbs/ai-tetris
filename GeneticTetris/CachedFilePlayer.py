'''
Created on 18/11/2011

@author: dev
'''

import random
import cStringIO
from FilePlayer import FilePlayer

class CachedFilePlayer(FilePlayer):
    
    def __init__(self, fileName):
        FilePlayer.__init__(self, fileName)
        self.__loaded = False
        self.__numTetros = 0
        
    def __loadCache(self):
        self.__tetroCount = -1;
        hfile = open(self.fileName, 'r')
        self.__cache = hfile.read()
        hfile.close() 
        self.__loaded = True
        self.__numTetros = len(self.__cache)

    def getCacheData(self):
        if not self.__loaded:
            self.__loadCache()
        return self.__cache
        
    def configure(self, game):
        self.__tetroCount = -1
        game.setDice(self.getNextTetromino)

    def getNextTetromino(self):
        if self.__tetroCount >= self.__numTetros:
            self.__tetroCount = 0
        else:
            self.__tetroCount += 1
        if not self.__loaded:
            self.__loadCache()
        return int(self.__cache[self.__tetroCount])
    
    def generateRandomGame(self, n):
        self.__hfile = cStringIO.StringIO()
        for i in xrange(n):
            self.__hfile.write(str(random.randint(1,7)))
        self.__cache = self.__hfile.getvalue() 
        self.__numTetros = len(self.__cache)
        self.__hfile.close()
        self.__loaded = True

    def generateRandomSZGame(self, n):
        self.__hfile = cStringIO.StringIO()
        for i in xrange(n):
            self.__hfile.write(str(random.randint(3,4)))
        self.__cache = self.__hfile.getvalue() 
        self.__numTetros = len(self.__cache)
        self.__hfile.close()
        self.__loaded = True

        
if __name__ == '__main__':
    pass