# -*- coding:utf-8 -*-
import pygame
import GUIDesigner
from Tetromino import Tetromino
from TetrisGame import TetrisGame, TetrisEvent 
from TetrisAI import TetrisAI
from AIThreadPlayer import AIThreadPlayer
from TetrisPlayer import TetrisPlayer
from StatisticPlayer import StatisticPlayer
#from CachedFilePlayer import CachedFilePlayer
#from TerminalPlayer import TerminalPlayer

class GUIPlayer(TetrisPlayer):
    
    REFRESH_BOARD     = pygame.USEREVENT + 1
    GAME_START        = pygame.USEREVENT + 2
    GAME_OVER         = pygame.USEREVENT + 3
    GRAVITY           = pygame.USEREVENT + 4
    NEXT_TETROMINO    = pygame.USEREVENT + 5
    REFRESH_STATISTIC = pygame.USEREVENT + 6
    
    
    def __init__(self):
        self.__drawing = False
        self.__running = False
        self.__aiPlayer = NotImplemented
        self.__statisticPlayer = StatisticPlayer()
        self.sp = self.__statisticPlayer
        self.__ai = NotImplemented
        self.__genomeId = "" 

    def bind(self, game):
        game.appendPlayer(self.__statisticPlayer)
        
    def unbind(self, game):
        game.removePlayer(self.__statisticPlayer)
        
    def configure(self, game):
        self.__game = game
        self.__board = game.getBoard()
        self.__tetromino = game.getTetromino()
        self.__tetrominoEvent = NotImplemented
        self.__nextTetrominoEvent = NotImplemented
        self.__boardEvent = NotImplemented
        self.__playing = False
        self.__ai = TetrisAI(self.__board, self.__tetromino)
        self.__genomeId = self.__ai.getGenome().getId()
        game.eventRegistry(self, [TetrisEvent.TETROMINO_START,
                                  TetrisEvent.TETROMINO_MOVE,
                                  TetrisEvent.BOARD_CHANGE], 
                           self.__refreshBoard)
        game.eventRegistry(self, [TetrisEvent.GAME_START], 
                           self.__gameStart)
        game.eventRegistry(self, [TetrisEvent.GAME_OVER], 
                           self.__gameOver)
        game.eventRegistry(self, [TetrisEvent.TETROMINO_NEXT], 
                           self.__regreshNextTetromino)

    def __refreshBoard(self, arg):
            self.__tetrominoEvent = self.__tetromino.getCopy()
            self.__boardEvent = self.__board.getCopy()
            pygame.event.clear(pygame.USEREVENT);
            pygame.event.post(pygame.event.Event(GUIPlayer.REFRESH_BOARD))
            
    def __gameStart(self, arg):
            pygame.event.clear(pygame.USEREVENT);
            pygame.event.post(pygame.event.Event(GUIPlayer.GAME_START))
            
    def __gameOver(self, arg):
            pygame.event.clear(pygame.USEREVENT);
            pygame.event.post(pygame.event.Event(GUIPlayer.GAME_OVER))
    
    def __regreshNextTetromino(self, arg):
            self.__nextTetrominoEvent = Tetromino(arg)
            pygame.event.clear(pygame.USEREVENT);
            pygame.event.post(pygame.event.Event(GUIPlayer.NEXT_TETROMINO))
        
    def aiSugest(self):
        dr, dx = self.__ai.play()
        for __ in xrange(abs(dr)):
            self.__game.rotationCcw()
        if dx >= 0:
            for __ in xrange(dx):
                self.__game.right()
        else:
            for __ in xrange(abs(dx)):
                self.__game.left()
        #self.__game.drop()
    
    def aiSwitchPlay(self):
        if self.__aiPlayer == NotImplemented:
            self.__aiPlayer = AIThreadPlayer()
            self.__aiPlayer.start()
            self.__game.appendPlayer(self.__aiPlayer)
            self.__genomeId = self.__aiPlayer.getId() 
        else:
            self.__game.removePlayer(self.__aiPlayer)
            self.__aiPlayer.stop()
            self.__aiPlayer = NotImplemented
            self.__genomeId = self.__ai.getGenome().getId() 

    def setGenome(self, genome, genomeId):
        TetrisOrganism.setDefaultGenome(genome, genomeId)
        if self.__ai != NotImplemented:
            self.__ai.getGenome().setGenome(genome, genomeId)
        if self.__aiPlayer != NotImplemented:
            self.__aiPlayer.getAI().getGenome().setGenome(genome, genomeId)
        self.__genomeId = genomeId
    
    def run(self, game):
        
        pygame.init()
        self.__game = game
        self.__game.play()

        # Definitions received from Player Class
        rows, cols = self.__board.getSize()
        self.__designer = GUIDesigner.GUIDesigner(cols, rows)
        self.__clock = pygame.time.Clock()
        #pygame.time.set_timer( pygame.USEREVENT+1, 800 )
        
        pygame.display.set_caption('-- Genetic Tetris --')
        self.__drawing = False
        self.__running = True
        try:
            while self.__running:
                self.__clock.tick(30)
                gravityOn = game.getGravityMode(); 
                pygame.display.flip()
                for event in pygame.event.get():
                    if self.__playing:
                        if event.type == GUIPlayer.REFRESH_BOARD:
                            self.__designer.drawBoard(self.__tetrominoEvent, 
                                                      self.__boardEvent)
                        elif event.type == GUIPlayer.NEXT_TETROMINO:
                            self.__designer.drawNetxTetromino(
                                       self.__nextTetrominoEvent)
                            self.__designer.drawStatistics(
                                       self.__statisticPlayer, 
                                       gravityOn, self.__genomeId)     
                        elif event.type == GUIPlayer.REFRESH_STATISTIC:
                            pass
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_DOWN:
                                self.__game.down()
                            elif event.key == pygame.K_UP:
                                self.__game.rotationCcw()
                            elif event.key == pygame.K_LEFT:
                                self.__game.left()
                            elif event.key == pygame.K_RIGHT:
                                self.__game.right()
                            elif event.key == pygame.K_SPACE:
                                self.__game.drop()
                            elif event.key == pygame.K_s:
                                self.aiSugest()
                            elif event.key == pygame.K_a:
                                self.aiSwitchPlay()
                            elif event.key == pygame.K_e:
                                self.__game.enforceGravity()
                            if event.key == pygame.K_o:
                                self.__game.over()
                            if event.key == pygame.K_g:
                                gravityOn = not gravityOn
                                game.setGravityMode(gravityOn)
                                self.__designer.drawStatistics(
                                       self.__statisticPlayer, 
                                       gravityOn, self.__genomeId)     
                            if event.key == pygame.K_1:
                                self.setGenome(TetrisGenomeExample.PD,
                                               TetrisGenomeExample.PD_ID)
                            if event.key == pygame.K_2:
                                self.setGenome(TetrisGenomeExample.PyEvolve9,
                                               TetrisGenomeExample.PyEvolve9_ID)
                            if event.key == pygame.K_3:
                                self.setGenome(TetrisGenomeExample.SZ,
                                               TetrisGenomeExample.SZ_ID)
                        elif event.type == GUIPlayer.GRAVITY:
                            if gravityOn:
                                self.__game.enforceGravity()
                                self.__designer.drawStatistics(
                                       self.__statisticPlayer, 
                                       gravityOn, self.__genomeId)     
                        elif event.type == GUIPlayer.GAME_OVER:
                            pygame.time.set_timer(GUIPlayer.GRAVITY, 0)
                            self.__playing = False
                            #if self.__aiPlayer != NotImplemented:
                            #    self.__aiPlayer.stop()
                            self.__designer.drawBoard(self.__tetrominoEvent, 
                                                      self.__boardEvent)
                            self.__designer.drawGameOver()
                            self.__designer.drawStatistics(
                                       self.__statisticPlayer, 
                                       gravityOn, self.__genomeId)     
                        elif event.type == pygame.QUIT:
                            self.__playing = False
                            self.__game.over()
                            self.__running = False
                    else:
                        if event.type == GUIPlayer.GAME_START:
                            self.__playing = True
                            pygame.time.set_timer(GUIPlayer.GRAVITY, 
                                        int(self.__game.getDonwDelay() * 1000))
                        elif event.type == pygame.K_t:
                            self.__playing = True
                        elif event.type == pygame.KEYUP:
                            if event.key == pygame.K_p:
                                self.__game.play()
                        elif event.type == pygame.QUIT:
                            self.__running = False                
        finally:
            if self.__aiPlayer != NotImplemented:
                self.__aiPlayer.stop()
                self.__game.removePlayer(self.__aiPlayer)
            self.__game.removePlayer(self)
            pygame.quit()

if __name__ == '__main__':
    playerGUI = GUIPlayer()
    #playerFile = FilePlayer("database/TetrisGame_sz.txt")
    #playerFile = CachedFilePlayer("database/TetrisGame.txt")
    #tp = TerminalPlayer(playerGUI.sp)
    from GeneticTetris import TetrisOrganism
    from TetrisGenomeExample import TetrisGenomeExample
    #TetrisOrganism.setDefaultGenome(TetrisGenomeExample.SZ)
    #playerFile.generateRandomSZGame(100000)
    #TetrisOrganism.setDefaultGenome(TetrisGenomeExample.PyEvolve9)
    TetrisOrganism.setDefaultGenome(TetrisGenomeExample.PD,
                                    TetrisGenomeExample.PD_ID)
    #playerFile.generateRandomGame(10000000)
    game = TetrisGame(20, 10)
    game.setGravityMode(False)
    game.appendPlayer(playerGUI)
    #game.appendPlayer(playerFile)
    #game.appendPlayer(tp)
    playerGUI.run(game)
    #game.removePlayer(tp)
    #game.removePlayer(playerFile)
    
    
    
    