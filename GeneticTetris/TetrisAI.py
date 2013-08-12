# -*- coding:utf-8 -*-
'''

REF: http://www.colinfahey.com/tetris/tetris_en.html

'''

from GeneticTetris import TetrisOrganism

class TetrisAI():
    """
    Board analysis class
    
    """
        
    def __init__(self, board, tetromino):

        self.__board = board
        self.__tetromino = tetromino
        self.__height, self.__width = board.getSize()
        self.__startRow, self.__startCol = board.getStartPosition()
        self.__startColTranslated = self.__startCol + 2;
        self.__individual = TetrisOrganism()

    def getGenome(self):
        return self.__individual

    def doEvaluateMovement(self, trow, tcol, trotation, tetroShape):

        tetromino = self.__tetromino.getCopy()
        tetromino.setPosition(trow, tcol)
        tetromino.changeRotation(trotation)
        rating = self.__individual.getDropFitness(self.__board, tetromino)

        col = tcol + 1
        absoluteDistanceX = abs(col - self.__startColTranslated)
        priority = (100 * absoluteDistanceX)
        if (col < self.__startColTranslated): 
            priority += 10;
        priority -= abs(self.trialRotationDelta)

        ''' If this move is better than any move considered before,
            or if this move is equally ranked but has a higher priority,
            then update this to be our best move. (http://www.colinfahey.com/) 
        '''
        if  (rating >  self.currentBestMerit) or    \
            ((rating == self.currentBestMerit) and  \
             (priority > self.currentBestPriority)): 
            self.currentBestMerit            = rating
            self.currentBestPriority         = priority
            self.currentBestTranslationDelta = tcol - self.__col
            self.currentBestRotationDelta    = self.trialRotationDelta


    def doAllLateralMovements(self, r):
        '''  '''
        # Fits in position while rotate?
        tetroShape = self.__tetromino.getShapeRotation(r)
        if not self.__board.fitsAt(self.__row, self.__col, tetroShape):
            return False
        cols = [self.__col]
        
        # Try translations to the right
        for col in xrange(self.__col + 1, self.__width):
            if not self.__board.fitsAt(self.__row, col, tetroShape):
                break
            cols.append(col)
        
        # Try translations to the left
        for col in xrange(self.__col - 1, -1, -1):
            if not self.__board.fitsAt(self.__row, col, tetroShape):
                break
            cols.append(col)

        cols.sort(None, None, True)            
        for col in cols:
            self.doEvaluateMovement(self.__row, col, r, tetroShape)
        
        return True
#        # Fits in position while rotate?
#        tetroShape = self.__tetromino.getShapeRotation(r)
#        if not self.__board.fitsAt(self.__row, self.__col, tetroShape):
#            return False
#        self.doEvaluateMovement(self.__row, self.__col, r, tetroShape)
#        
#        # Try translations to the right
#        for col in xrange(self.__col + 1, self.__width):
#            if not self.__board.fitsAt(self.__row, col, tetroShape):
#                break
#            self.doEvaluateMovement(self.__row, col, r, tetroShape)
#        
#        # Try translations to the left
#        for col in xrange(self.__col - 1, -1, -1):
#            if not self.__board.fitsAt(self.__row, col, tetroShape):
#                break
#            self.doEvaluateMovement(self.__row, col, r, tetroShape)
#        
#        return True
    
    def play(self):

       
        self.__tetroType =  self.__tetromino.getType()
        self.__rotation = self.__tetromino.getRotation()
        self.__row, self.__col = self.__tetromino.getPosition() 

        self.currentBestMerit            = (-1.0e+20)
        self.currentBestPriority         = 0
        self.currentBestTranslationDelta = 0
        self.currentBestRotationDelta    = 0
        
        for rotation in xrange(self.__tetromino.getRotations()):
            self.trialRotationDelta = rotation
            if not self.doAllLateralMovements(self.__rotation + rotation):
                break  # supposing only one rotate direction 

        #=======================================================================
        # # supposing rotate in two direction: CCW (+1) e CW (-1)
        # rotations = self.__tetromino.getRotations()
        # if rotations >= 1:
        #    self.trialRotationDelta = 0
        #    if self.doAllLateralMovements(self.__rotation):
        #        if rotations >= 2:
        #            self.trialRotationDelta = 1
        #            rp1 = self.doAllLateralMovements(self.__rotation + 1)
        #        if rotations >= 4:
        #            self.trialRotationDelta = -1
        #            rm1 = self.doAllLateralMovements(self.__rotation - 1)
        #            if rp1 or rm1:
        #                self.trialRotationDelta = 2
        #                self.doAllLateralMovements(self.__rotation + 2)
        #=======================================================================

        return self.currentBestRotationDelta, self.currentBestTranslationDelta
    
    