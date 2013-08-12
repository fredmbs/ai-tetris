# -*- coding:utf-8 -*-

#import threading
from TetrisGame import TetrisEvent
from TetrisPlayer import TetrisPlayer

class TerminalPlayer(TetrisPlayer):
    
    def __init__(self, statistic = NotImplemented):
        self.statistic = statistic
        self.drawing = False
        pass 
    
    def configure(self, game):
        self.__game = game
        self.setBoard(game.getBoard())
        self.setTetromino(game.getTetromino())
        game.eventRegistry(self, [TetrisEvent.TETROMINO_START,
                                  TetrisEvent.TETROMINO_MOVE,
                                  TetrisEvent.BOARD_CHANGE], 
                           self.__output)
        game.eventRegistry(self, [TetrisEvent.GAME_START], 
                           self.__gameStart)
        game.eventRegistry(self, [TetrisEvent.GAME_OVER], 
                           self.__gameOver)

    def __output(self, arg):
            self.draw(self.__board.getDataCopy(),
                      self.__tetromino.getType(), 
                      self.__tetromino.getShapeAt())
            
    def __gameStart(self, arg):
        print "GAME START!"

    def __gameOver(self, arg):
        print "GAME OVER..."

    def setTetromino(self, tetromino):
        self.__tetromino = tetromino 

    def setBoard(self, board):
        self.__board = board 
        self.__height, self.__width  = self.__board.getSize()
        self.__maxRow, self.__maxCol = self.__height - 1, self.__width - 1 

    def draw(self, boardData, tetroType, shape):
        if self.drawing:
            return
        try:
            self.drawing = True
            if self.statistic != NotImplemented:
                print "Level =", self.statistic.level
                print "Score =", self.statistic.score
                print "Rows  =", self.statistic.sumErodedRows
                print "Round =", self.statistic.tetromino
                print "Timer =", self.statistic.lastMoveTime
            for i in shape:
                boardData[i[0]][i[1]] = tetroType
            for row in range(self.__maxRow,-1,-1):
                line = ""
                for col in range(self.__width):
                    if boardData[row][col] > 0:
                        line += str(boardData[row][col])
                    else:
                        line += " "
                print "{0:2d}|{1}|".format(row,line)
            print "--+{0}+".format("-" * self.__width)
        finally:
            self.drawing = False

    @staticmethod    
    def drawBoard(board):
        height, width  = board.getSize()
        maxRow = height - 1
        boardData = board.getData() 
        for row in range(maxRow,-1,-1):
            line = ""
            for col in range(width):
                if boardData[row][col] > 0:
                    line += str(boardData[row][col])
                else:
                    line += " "
            print "{0:2d}|{1}|".format(row,line)
        print "--+{0}+".format("-" * width)
    
    @staticmethod    
    def drawBoardFile(board, ouput):
        height, width  = board.getSize()
        maxRow = height - 1
        boardData = board.getData() 
        for row in range(maxRow,-1,-1):
            line = ""
            for col in range(width):
                if boardData[row][col] > 0:
                    #line += str(boardData[row][col])
                    line += "X"
                else:
                    line += " "
            num = "{0:2}".format(row+1).replace(" ", "0")
            ouput.write("{0}|{1}|\n".format(num,line))
        ouput.write("--+{0}+\n".format("-" * width))
    
