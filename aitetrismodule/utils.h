#ifndef UTILS_H
#define UTILS_H
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
Tipos e funções utilitárias
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