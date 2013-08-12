#ifndef BOARD_H
#define BOARD_H
/*                            
UNI-BH - Centro Universit�rio de Belo Horizonte
DCET   - Departamento de Ci�ncias Exatas e Tecnol�gicas
-------------------------------------------------------------------------
Ci�ncia da Computa��o
IA - Intelig�ncia Artifical
Professora - Ana Paula ladeira
-------------------------------------------------------------------------
Trabalho Pr�tico: Algor�tmos Gen�ticos - Otimiza��o do Tetris
Alunos:  Frederico Martins Biber Sampaio
         Guilherme Brand�o Biber Sampaio
         Gustavo Pantuza Coelho Pinto
-------------------------------------------------------------------------
Tipos e fun��es de manipula��o do tabuleiro
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