#ifndef BOARD_H
#define BOARD_H
/*                            
UNI-BH - Centro Universitário de Belo Horizonte
DCET   - Departamento de Ciências Exatas e Tecnológicas
-------------------------------------------------------------------------
Ciência da Computação
IA - Inteligência Artifical
Professora - Ana Paula ladeira
-------------------------------------------------------------------------
Trabalho Prático: Algorítmos Genéticos - Otimização do Tetris
Alunos:  Frederico Martins Biber Sampaio
         Guilherme Brandão Biber Sampaio
         Gustavo Pantuza Coelho Pinto
-------------------------------------------------------------------------
Tipos e funções de manipulação do tabuleiro
-------------------------------------------------------------------------
*/

#include "tetromino.h"

#define MAX_LINES 32

typedef struct {
        int orientation, 
            column,
            landingHeight,
            rowsRemoved,
            gameOver;
        SHAPE shape;
    } MOVEMENT;

typedef struct {
        int  height, 
             width;
        int line[MAX_LINES];
    } BOARD; 


int GetWellSums(BOARD *board);
int GetColumnTransitions(BOARD *board);
int GetNumberOfHoles(BOARD *board);
int GetRowTransitions(BOARD *board, int *pileHeight);

#endif