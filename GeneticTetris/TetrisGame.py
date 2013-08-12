# -*- coding:utf-8 -*-

#import random, 
import random
import time
from TetrisBoard import TetrisBoard
from TetrominoBoardControl import TetrominoBoardControl
from Tetromino import Tetromino 

class TetrisCommand:
    
    NONE      = 0
    START     = 1
    MOVE      = 2
    TERMINATE = 3
    RANGE     = 4

class TetrisEvent:

    NONE              = 0
    GAME_START        = 1
    GAME_OVER         = 2
    GAME_GRAVITY      = 3
    TETROMINO_NEXT    = 4
    TETROMINO_START   = 5
    TETROMINO_MOVE    = 6
    TETROMINO_BLOCKED = 7
    TETROMINO_GRAVITY = 8
    BOARD_CHANGE      = 9
    RANGE             = 10

class TetrisMove:
    
    NONE            = 0
    DOWN            = 1
    LEFT            = 2
    RIGHT           = 3
    ROTATION_CCW    = 4
    ROTATION_CW     = 5
    DROP            = 6
    RANGE           = 7 

class TetrisGame:
    '''
    Main class of this Tetris implementation
    
    Only the game flows are controlled in this class. It comunicate with 
    the GUI controller, GUI observer, trigger changes to the game board and
    make call to get Tetrominos states.
    
    Parameters:
    
        width  : width to initiate the game board
        height : height to initiate the game board
        
    '''
    
    osTimer = time.clock
    
    def __init__(self, height = 22, width = 10, name = "Random"):
        """ """
        self.__name = name
        self.__height = max(6, height)
        self.__width = max(6, width)
        self.__gravityMode = True
        self.__players = []
        self.__initEventCtrl()
        self.__configure()
        
    def __initEventCtrl(self):
        self.__events = [{} for __ in xrange(TetrisEvent.RANGE)]

    def __configure(self):
        self.__configuring = True
        self.__countLines = 0
        self.__playing = False
        self.__downTime = TetrisGame.osTimer()
        self.__downDelay = 2 #0.5
        self.resetDice()
        #self.__statistics = TetrisStatistics()
        self.__tetromino = Tetromino()
        self.__board = TetrisBoard(self.__height, self.__width)
        self.__tbc = TetrominoBoardControl(self.__board, self.__tetromino)
        
        # call players at reverse order (first to append -> last to call)
        self.__players.reverse()
        [player.configure(self) for player in self.__players]
        self.__players.reverse()
        self.__configuring = False

    def __goodLuck(self):
        return random.randint(1,7)

    def getName(self):
        return self.__name
    
    def setName(self, name):
        self.__name = name
    
    def getLines(self):
        return self.__countLines
    
    def isPlaying(self):
        return self.__playing
        
    def getBoardSize(self):
        ''' Getter method for the board size '''
        return self.__height, self.__width  

    def isOver(self):
        return not self.__playing
        
    def setDownDelay(self, seconds):
        self.__downDelay = seconds
        self.__notifyPlayers(TetrisEvent.GAME_GRAVITY, self.__downDelay)
        
    def getGravityMode(self):
        return  self.__gravityMode

    def setGravityMode(self, mode):
        if mode != self.__gravityMode:
            self.__downTime = TetrisGame.osTimer()
            self.__gravityMode = mode
            if self.__gravityMode:
                self.__notifyPlayers(TetrisEvent.GAME_GRAVITY, self.__downDelay)
            else:
                self.__notifyPlayers(TetrisEvent.GAME_GRAVITY, 0)
    
    def getDice(self):
        return self.__getNextTetraminoType
        
    def setDice(self, getter):
        self.__getNextTetraminoType = getter
        
    def resetDice(self):
        self.__getNextTetraminoType = self.__goodLuck
        
    def changeSize(self, height, width):
        if not self.__playing:
            self.__height = height
            self.__width = width
            self.__configure()
       
    def getBoard(self):
        return self.__board
    
    def getTetromino(self):
        return self.__tetromino

    def getDonwDelay(self):
        return self.__downDelay
    
    def getIsConfiguring(self):
        return self.__configuring
    
    def appendPlayer(self, player):
        """ Add a player to the game """
        #if (not self.__configuring) and (not (player in self.__players)):
        if (not (player in self.__players)):
            self.__players.append(player)
            player.bind(self)
            if self.__playing:
                player.configure(self)
                self.__notifyPlayer(player, TetrisEvent.TETROMINO_NEXT, 
                                    self.__nextTetroType)
                self.__notifyPlayer(player, TetrisEvent.TETROMINO_START, 
                                    self.__nextTetroType)
                self.__notifyPlayer(player, TetrisEvent.BOARD_CHANGE, [])

    def removePlayer(self, player):
        """ Remove a player to the game """
        #if (not self.__configuring) and (player in self.__players):
        if (player in self.__players):
            self.__players.remove(player)
            for event in self.__events:
                if player in event:
                    del event[player]
            player.unbind(self)

    def eventRegistry(self, player, events, notifier = NotImplemented):
        for event in events:
            if (notifier != NotImplemented) and (player in self.__players):
                self.__events[event][player] = notifier
            elif (player in self.__events[event]):
                del self.__events[event][player]
        
    def __notifyPlayers(self, event, arg):
        [notifier(arg) for notifier in self.__events[event].viewvalues()]

    def __notifyPlayer(self, player, event, arg):
        if (player in self.__events[event]):
            self.__events[event][player](arg)
        
    def play(self):
        """ Starts the game """
        self.__configure()
        self.__countLines = 0
        self.__playing = True
        self.__notifyPlayers(TetrisEvent.GAME_START, 0)
        self.__nextTetroType = self.__getNextTetraminoType()
        self.__nextTetromino()

    def over(self):
        """ Ends the game """
        self.__playing = False
        self.__notifyPlayers(TetrisEvent.GAME_OVER, 
                             self.__tetromino.getType())

    def __nextTetromino(self):
        tetroType = self.__nextTetroType
        if tetroType == 0:
            self.over()
        else:
            self.__nextTetroType = self.__getNextTetraminoType()
            self.__notifyPlayers(TetrisEvent.TETROMINO_NEXT, 
                                 self.__nextTetroType)
            self.__downTime = TetrisGame.osTimer()
            fits = self.__tbc.newTetromino(tetroType)
            self.__notifyPlayers(TetrisEvent.TETROMINO_START, 
                                 tetroType)
            if not fits:
                self.over()
            
    def down(self):
        if self.__tbc.down():
            self.__downTime = TetrisGame.osTimer()
            self.__notifyPlayers(TetrisEvent.TETROMINO_MOVE, 
                                TetrisMove.DOWN)
        else:
            self.drop()
        
    def right(self):
        if self.__tbc.right():
            self.__notifyPlayers(TetrisEvent.TETROMINO_MOVE, 
                                TetrisMove.RIGHT)
        else:
            self.__notifyPlayers(TetrisEvent.TETROMINO_BLOCKED, 
                                TetrisMove.ROTATION_CW)
        
    def left(self):
        if self.__tbc.left():
            self.__notifyPlayers(TetrisEvent.TETROMINO_MOVE, 
                                TetrisMove.LEFT)
        else:
            self.__notifyPlayers(TetrisEvent.TETROMINO_BLOCKED, 
                                TetrisMove.ROTATION_CW)
        
    def rotationCcw(self):
        if self.__tbc.rotationCcw():
            self.__notifyPlayers(TetrisEvent.TETROMINO_MOVE, 
                                TetrisMove.ROTATION_CCW)
        else:
            self.__notifyPlayers(TetrisEvent.TETROMINO_BLOCKED, 
                                TetrisMove.ROTATION_CW)

    def rotationCw(self):
        if self.__tbc.rotationCw():
            self.__notifyPlayers(TetrisEvent.TETROMINO_MOVE, 
                                TetrisMove.ROTATION_CW)
        else:
            self.__notifyPlayers(TetrisEvent.TETROMINO_BLOCKED, 
                                TetrisMove.ROTATION_CW)

    def drop(self):
        if self.__tbc.drop():
            self.__notifyPlayers(TetrisEvent.TETROMINO_MOVE, 
                                 TetrisMove.DROP)
            rows, count = self.__board.eliminateRows()
            self.__countLines += count
            self.__notifyPlayers(TetrisEvent.BOARD_CHANGE, rows)
            self.__nextTetromino()
        else:
            self.over()
            
    def enforceGravity(self):
        if self.__gravityMode:
            now = TetrisGame.osTimer()
            downMoves = int((now - self.__downTime) / self.__downDelay)
            if downMoves > 0:
                self.__notifyPlayers(TetrisEvent.TETROMINO_GRAVITY, downMoves)
                for __ in xrange(downMoves):
                    if self.__tbc.down():
                        self.__downTime += self.__downDelay
                        self.__notifyPlayers(TetrisEvent.TETROMINO_MOVE, 
                                         TetrisMove.DOWN)
                    else:
                        self.drop()
                        break
      
