# -*- coding:utf-8 -*-
import pygame

class GUIDesigner():
    
    def __init__(self, numColumns, numRows):
        pygame.font.init()
        self.__fontSize = 15
        self.__statisticFont = pygame.font.SysFont("Fixed, Monospace, Courier",
                                                   size=self.__fontSize,
                                                   bold=True)
        self.__statisticLine = 0
        self.setColors()
        self.setGameDimensions(numColumns, numRows)
        self.setScreen()
        self.setSurfaces()
        self.fill()
        self.blitTitleSurface()
        
    def setColors(self):
        self.__colors = {
            'cyan'      : pygame.Color(0, 183, 235),
            'yellow'    : pygame.Color(255,255,0),
            'magent'    : pygame.Color(255,20,147),
            'orange'    : pygame.Color(255,165,0),
            'red'       : pygame.Color(255, 0, 0),
            'blue'      : pygame.Color(0, 0, 255),
            'green'     : pygame.Color(0, 255, 0),
            'gray'      : pygame.Color(105,105,105),
            'black'     :  pygame.Color(0,0,0)
            
        }    
        self.__tetroColors = [ self.__colors['gray'],
                               self.__colors['cyan'],
                               self.__colors['yellow'],
                               self.__colors['magent'],
                               self.__colors['orange'],
                               self.__colors['red'],
                               self.__colors['blue'],
                               self.__colors['green']
                            ]

            
    def blitTitleSurface(self):
        self.__font = pygame.font.Font(pygame.font.get_default_font(), 14)
        title_label=self.__font.render('Genetic Tetris 0.2', 1, (100,100,255))
        self.blitOnSurface(self.__titleSurface, title_label, 80, 8)
        self.blitOnScreen(self.__titleSurface,self.__tetrisX , 0)
        
    def setGameDimensions(self, numColumns, numRows):
        # Screen resolution
        self.__xSize, self.__ySize = (800, 600)
        # Tetris resolution
        self.__tetrisX, self.__tetrisY = (self.__xSize - 300, self.__ySize)
        # User board division definition
        self.__numColumns, self.__numRows = (numColumns, numRows)
        # Graphic board dimensblitTitleSurface      
        self.__GUIDx = self.__tetrisX / self.__numColumns
        self.__GUIDy = self.__tetrisY / self.__numRows
        #######################################################################
        self.__GUIDx = self.__GUIDy = min(self.__GUIDx, self.__GUIDy)
        #######################################################################
        # lower square dimension
        self.__squaresX = max(self.__GUIDx, self.__GUIDy)
        self.__squaresY = min(self.__GUIDx, self.__GUIDy)
        # higher and lower padding
        self.__minPadding, self.__maxPadding = (1,5)
        # Game global Padding
        #self.__paddingX = min(self.__maxPadding,max(self.__minPadding, 
        #                    int(self.__squaresX / 15)))
        #self.__paddingY = min(self.__maxPadding,max(self.__minPadding, 
        #                    int(self.__squaresY / 15)))
        self.__paddingX = self.__paddingY = 1
        #######################################################################
        self.__paddingX = self.__paddingY = min(self.__paddingX, self.__paddingY)
        self.__gameWidth = self.__GUIDx * numColumns - self.__paddingX
        self.__gameHeight = self.__GUIDy * numRows - self.__paddingY
        self.__gameX = (self.__tetrisX - self.__gameWidth)/2 
        self.__gameY = (self.__tetrisY - self.__gameHeight)/2
        #######################################################################
        # Smaller block dimension considering its padding
        self.__blockDimensionX = self.__squaresX - self.__paddingX
        self.__blockDimensionY = self.__squaresY - self.__paddingY
        
    
    def getScreen(self):
        return self.__screen
    def getTetrisSurface(self):
        return self.__tetrisSurface
    def getColor(self, color):
        return self.__colors[color]

        
    def getSquaresX(self):
        return self.__squaresX
    def getSquaresY(self):
        return self.__squaresY
    
    def getBlockDimensionX(self):
        return self.__blockDimensionX 
    def getBlockDimensionY(self):
        return self.__blockDimensionY
 
       
    def setScreen(self):
        # set the screen base surface
        self.__screen = pygame.display.set_mode((self.__xSize,self.__ySize))
    
    def setSurfaces(self):
        self.__tetrisSurface = pygame.Surface(
                                    (self.__gameWidth, self.__gameHeight))
        self.__titleSurface = pygame.Surface((300, 30))
        self.__nextTetrominoSurface = pygame.Surface((300, 120))
        self.__scoreSurface = pygame.Surface((300,450))
      
    def fill(self):
        #self.__tetrisSurface.fill(self.__colors['gray'])
        self.__titleSurface.fill(self.__colors['orange'])
        self.__nextTetrominoSurface.fill(self.__colors['blue'])
        self.__scoreSurface.fill(self.__colors['yellow'])
    
    def fillSurface(self, surface, color):
        surface.fill(self.__colors[color])
        
    def blitOnScreen(self, surface, xPos=0, Ypos=0):
        self.__screen.blit(surface, (xPos,Ypos))
    
    def blitOnSurface(self, surface, element, xPos, yPos):
        surface.blit(element, (xPos, yPos))

    def drawStatisticsLine(self, line):
        label = self.__statisticFont.render(line, 1, (0,0,0))
        self.__scoreSurface.blit(label, (10, self.__statisticLine))
        self.__statisticLine += (self.__fontSize + 2)
    
    def drawStatistics(self, stat, gravity, genome):
        self.__statisticLine = 6
        self.__scoreSurface.fill(self.__colors['yellow'])
        self.drawStatisticsLine("Game   :" + str(stat.id))
        self.drawStatisticsLine("Score  :" + str(stat.score))
        self.drawStatisticsLine("AIScore:" + str(stat.aiScore))
        self.drawStatisticsLine("Genome :" + genome)
        self.drawStatisticsLine("Level  :" + str(stat.level))
        self.drawStatisticsLine("Tretominoes  :" + str(stat.tetromino))
        maxT = max(stat.tetroCount) 
        for i in xrange(1,len(stat.tetroCount)):
            deltaT = maxT - stat.tetroCount[i]
            self.drawStatisticsLine("   [" + str(i) + \
                                    "]:" + str(stat.tetroCount[i]) + \
                                    " (" + str(deltaT) + ")")
        erodedRows = 0
        for i in xrange(1,5):
            erodedRows += stat.erodedRows[i] 
        self.drawStatisticsLine("Eroded rows  :" + str(erodedRows)) 
        for i in xrange(len(stat.erodedRows)):
            self.drawStatisticsLine("   [" + str(i) + \
                                    "]:" + str(stat.erodedRows[i]))
        self.drawStatisticsLine("Time spent   :" + str(stat.sumTime)) 
        self.drawStatisticsLine("Average time :" + str(stat.sumTime / stat.tetromino))
        self.drawStatisticsLine("Blocked moves:" + str(stat.blockedMoves))
        self.drawStatisticsLine("Gravity moves:" + str(stat.attractions))
        if gravity:
            gravityMode = "ON"
        else: 
            gravityMode = "OFF"
        self.drawStatisticsLine("Gravity mode :" + gravityMode)
        self.drawStatisticsLine("Gravity delay:" + str(stat.downDelay))
        self.__screen.blit(self.__scoreSurface, (self.__tetrisX , 150))

    def drawNetxTetromino(self, tetromino):
        # Draw tetromino drop preview
        tetroType = tetromino.getType()
        shapePreview = tetromino.getShape()
        self.__nextTetrominoSurface.fill(self.__colors['gray'])
        for shape in shapePreview:
            rect = pygame.Rect(120 - (30 * shape[1]), 30 - (30 * shape[0]), 
                               29, 29);
            pygame.draw.rect(self.__nextTetrominoSurface, 
                             self.__tetroColors[tetroType], rect)
        #self.blitOnScreen(self.__tetrisSurface)
        self.__screen.blit(self.__nextTetrominoSurface,
                           (self.__tetrisX , 30))
            
    def drawGameOver(self):
        self.__nextTetrominoSurface.fill(self.__colors['gray'])
        self.__font = pygame.font.Font(pygame.font.get_default_font(), 30)
        over_label=self.__font.render('Game Over!', 1, self.__colors['red'])
        self.blitOnSurface(self.__nextTetrominoSurface, over_label, 70, 45)
        self.blitOnScreen(self.__nextTetrominoSurface,self.__tetrisX , 30)
        
    def drawBoard(self, tetromino, board):
        
        tetroType = tetromino.getType()
        tetroShapeInBoard = tetromino.getShapeAt()
        boardData = board.getData()
        
        self.__tetrisSurface.fill(self.__colors['gray'])
        
        # Draw board
        for row in xrange(self.__numRows):
            reversedRow = (-(row + 1)%self.__numRows)
            for col in xrange(self.__numColumns):
                tetro = boardData[row][col]
                if  tetro != 0:
                    rect = pygame.Rect(self.__squaresX * col,
                                       self.__squaresY * reversedRow, 
                                       self.__blockDimensionX,
                                       self.__blockDimensionY);
                    pygame.draw.rect(self.__tetrisSurface, 
                                      self.__tetroColors[tetro], rect)
        
        # Draw tetromino
        for shape in tetroShapeInBoard:
            reverserRow = -(shape[0] + 1)%self.__numRows
            rect = pygame.Rect(self.__squaresX * shape[1],
                               self.__squaresY * reverserRow, 
                               self.__blockDimensionX,
                               self.__blockDimensionY);
            pygame.draw.rect(self.__tetrisSurface, 
                              self.__tetroColors[tetroType], rect)

        # Draw grid            
        for row in xrange(1,self.__numRows):
            y = (self.__squaresY * row) - 1
            pygame.draw.line(self.__tetrisSurface, self.__colors['black'],
                             (0, y), (self.__gameWidth, y))
        for col in xrange(1,self.__numColumns):
            x = (self.__squaresX * col) - 1
            pygame.draw.line(self.__tetrisSurface, self.__colors['black'],
                             (x, 0), (x, self.__gameHeight))
            
        # Draw tetromino drop preview
        shapeDropPreview = board.getShapeDropPreview(tetromino)
        for shape in shapeDropPreview:
            reverserRow = -(shape[0] + 1)%self.__numRows
            rect = pygame.Rect(self.__squaresX * shape[1],
                               self.__squaresY * reverserRow, 
                               self.__blockDimensionX,
                               self.__blockDimensionY);
            pygame.draw.rect(self.__tetrisSurface, 
                              self.__tetroColors[tetroType], rect, 1)
            
        #self.blitOnScreen(self.__tetrisSurface)
        self.__screen.blit(self.__tetrisSurface,
                           (self.__gameX, self.__gameY))

    #def drawAll(self, tetromino, board, nextTetro, stat, gravity, genome):
    #    self.drawBoard(tetromino, board)
    #    self.drawNetxTetromino(nextTetro)
    #    self.drawStatistics(stat, gravity, genome)
        