# -*- coding:utf-8 -*-

import cPickle

class TetrisBoard:
    """
    Board control class
    
    Controls the game dimentions and insert Tetromino on the surface.
    Verify if it is inside the board and its chance of drop.
    
        Parameters:
            
            width  : width of the game board
            height : height of the game board
    """
        
    def __init__(self, height, width):
        
        # height and width of the board
        self.__width  = width
        self.__height = height
        
        if (width < 4) or (height < 4):
            raise "FATAL: Board dimension too small"
        
        # Intialise the board data matrix with zeros
        self.__board = [[0 for col in xrange(width)] for row in xrange(height)]

    def clear(self):
        """
         Initialise the board data matrix 
        """
        for row in xrange(self.__height):
            for col in xrange(self.__width):
                self.__board[row][col] = 0
    
    def getSize(self):
        """ Getter method for the board size """
        return self.__height, self.__width  
    
    def getData(self):
        return self.__board
    
    def getCopy(self):
        return cPickle.loads(cPickle.dumps(self, -1))

    def getDataCopy(self):
        return cPickle.loads(cPickle.dumps(self.__board, -1))

    def getStartPosition(self):
        return self.__height - 2, int((self.__width - 1)/2)

    def isInside(self, shape):
        """ Returns True if shape is inside the board, otherwise False """
        for i in shape:
            if (i[0] < 0) or (i[1] < 0) or \
               (i[0] >= self.__height) or (i[1] >= self.__width):
                return False
        return True
    
    def fits(self, shape):
        for i in shape:
            pr = i[0]
            pc = i[1]
            if (pc < 0) or (pr < 0) or \
               (pc >= self.__width) or (pr >= self.__height) or \
               self.__board[pr][pc] != 0:
                return False
        return True
        
    def fitsAt(self, row, col, tetroShape):
        for i in tetroShape:
            pr = i[0] + row
            pc = i[1] + col
            if (pc < 0) or (pr < 0) or \
               (pc >= self.__width) or (pr >= self.__height) or \
               self.__board[pr][pc] != 0:
                return False
        return True

    def getDropTo(self, row, col, tetroShape):
        resp = row
        for testRow in xrange(row, -1, -1):
            if self.fitsAt(testRow, col, tetroShape):
                resp = testRow
            else:
                return resp
        return resp
    
    def getShapeDropPreview(self, tetromino):
        row, col = tetromino.getPosition()
        row = self.getDropTo(row, col, tetromino.getShape())
        return tetromino.getShapeAtPosition(row, col)
    
    def unsafeInsert(self, tetroType, shape):
        for i in shape:
            self.__board[i[0]][i[1]] = tetroType
            

    ''' Board Analysis Functions '''
                
    def eliminateRows(self):
        rows = []
        count = 0
        for row in xrange(self.__height - 1, -1, -1):
            if min(self.__board[row]) > 0:
                count += 1
                rows.append(row)
                self.__board.pop(row)
                self.__board.append([0 for col in xrange(self.__width)])
        return rows, count

    def calculateErosion(self, shape):
        rows = pieces = 0
        foundRows = [ -1, -1, -1, -1]
        for row in xrange(self.__height):
            if min(self.__board[row]) > 0:
                foundRows[rows] = row
                rows += 1
        for piece in shape:
            if piece[0] in foundRows:
                pieces += 1
        return rows, pieces

    def calculatePileMaxHeight(self):
        for row in xrange(self.__height - 1, -1, -1):
            for col in xrange(self.__width):
                if self.__board[row][col] != 0:
                    return row + 1
        return 0

    def calculateTransitionForRow(self, row):
        count = 0
        for col in xrange(self.__width - 1):
            a = self.__board[row][col] == 0            
            b = self.__board[row][col + 1] == 0
            if ((not a) and b) or (a and (not b)):
                count += 1
        if self.__board[row][0] == 0:
            count += 1
        if self.__board[row][self.__width - 1] == 0:
            count += 1            
        return count
    
    def calculateTransitionForColumn(self, col):
        count = 0
        for row in xrange(self.__height - 1):
            a = self.__board[row][col] == 0            
            b = self.__board[row + 1][col] == 0
            if ((not a) and b) or (a and (not b)):
                count += 1
        if self.__board[0][col] == 0:
            count += 1
        if self.__board[self.__height - 1][col] != 0:
            count += 1            
        return count
    
    def calculateBuriedHolesForColumn(self, col):
        top = 0
        for row in xrange(self.__height - 1, -1, -1):
            if self.__board[row][col] != 0:
                top = row
                break
        if top > 0:
            count = 0
            for row in xrange(top):
                if self.__board[row][col] == 0:
                    count += 1
            return count
        return 0

    def blanksDownBeforeBlockedForColumn(self, top, col):
        count = 0
        for row in xrange(top, -1, -1):
            if self.__board[row][col] != 0:
                break
            count += 1
        return count
    
    def calculateAllWellsForColumn(self, col):
        wellValue = 0 
        if col == 0:
            for row in xrange(self.__height - 1, -1, -1):
                if (self.__board[row][0] == 0) and \
                   (self.__board[row][1] != 0):
                    wellValue += self.blanksDownBeforeBlockedForColumn(row, col)
        elif col == self.__width - 1: 
            for row in xrange(self.__height - 1, -1, -1):
                if (self.__board[row][col] == 0) and \
                   (self.__board[row][self.__width - 2] != 0):
                    wellValue += self.blanksDownBeforeBlockedForColumn(row, col)
        else:
            for row in xrange(self.__height - 1, -1, -1):
                if (self.__board[row][col - 1] != 0) and \
                   (self.__board[row][col + 1] != 0):
                    wellValue += self.blanksDownBeforeBlockedForColumn(row, col)
        return wellValue

