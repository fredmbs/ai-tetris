#ifndef UTILS_H
#define UTILS_H
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
Tipos e fun��es utilit�rias
-------------------------------------------------------------------------
*/


#ifdef DEBUG_LOG
#include "board.h"
#include <stdio.h>

void printBoard(FILE *hf, BOARD *board);
#endif

int loadSortedTetroTypes(char *fileName, 
                         char *sortedTetroTypes, 
                         int numTetroTypes);

#endif