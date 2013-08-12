# -*- coding:utf-8 -*-

'''
Created on 08/11/2011

@author: dev
'''
class TetrominoBoardControl:
    '''
    classdocs
    '''

    def __init__(self, board, tetromino):
        '''
        Constructor
        '''
        # Initiate the thread
        self.__board = board;
        self.__row = 0
        self.__col = 0
        self.__tetroType = 0
        self.__tetroRotation = 0
        self.__tetromino = tetromino
        # set initial position os tretominoes
        self.__startRow, self.__startCol = board.getStartPosition()


    def newTetromino(self, tetroType):
        shape = self.__tetromino.changeTetromino(tetroType, 
                                                 self.__startRow, 
                                                 self.__startCol)
        if self.__board.fits(shape):
            self.__tetroType = tetroType
            self.__tetroRotation = 0
            self.__row = self.__startRow
            self.__col = self.__startCol
            return True
        else:
            return False
        
    def down(self):
        row = self.__row - 1
        shape = self.__tetromino.getShapeAtPosition(row, self.__col) 
        if self.__board.fits(shape):
            self.__row = row
            self.__tetromino.setPosition(self.__row, self.__col) 
            return True
        else:
            return False
        
    def right(self):
        col = self.__col + 1
        shape = self.__tetromino.getShapeAtPosition(self.__row, col) 
        if self.__board.fits(shape):
            self.__col = col
            self.__tetromino.setPosition(self.__row, self.__col) 
            return True
        else:
            return False
        
    def left(self):
        col = self.__col - 1
        shape = self.__tetromino.getShapeAtPosition(self.__row, col) 
        if self.__board.fits(shape):
            self.__col = col
            self.__tetromino.setPosition(self.__row, self.__col) 
            return True
        else:
            return False
        
    def rotationCcw(self):
        r = self.__tetroRotation + 1;
        shape = self.__tetromino.getShapeAtRotation(self.__row, self.__col, r) 
        if self.__board.fits(shape):
            self.__tetroRotation = self.__tetromino.changeRotation(r)
            return True
        else:
            return False

    def rotationCw(self):
        r = self.__tetroRotation - 1;
        shape = self.__tetromino.getShapeAtRotation(self.__row, self.__col, r) 
        if self.__board.fits(shape):
            self.__tetroRotation = self.__tetromino.changeRotation(r)
            return True
        else:
            return False

    def drop(self):
        tetroShape = self.__tetromino.getShape() 
        row = self.__board.getDropTo(self.__row, self.__col, tetroShape)
        if row >= 0:
            shape = self.__tetromino.getShapeAtPosition(row, self.__col)
            if self.__board.fits(shape):
                self.__row = row
                self.__board.unsafeInsert(self.__tetroType, shape)
                return True
        return False

