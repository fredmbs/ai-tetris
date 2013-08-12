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
Funções utilitárias
-------------------------------------------------------------------------
*/

#include <stdio.h> 
#include "utils.h"

#ifdef DEBUG_LOG
void printBoard(FILE *hf, BOARD *board) {
    int width;
    int height;
    int x;
    int y;
    int line;

    width  = board->width;
    height = board->height;
    //fprintf(hf, "height = %d\n", height);
    //fprintf(hf, "width = %d\n", width);


    for (y = height - 1; y >= 0; y--) { // top-down
        line = board->line[y];
        fprintf(hf, "%2.2i|", y + 1);
        for (x = width - 1; x >= 0; x--)
        {
            if ((line >> x) & 1) {
                fprintf(hf, "X");
            } else {
                fprintf(hf, " ");
            }
        }
        //fprintf(hf, "|%d\n", line);
        fprintf(hf, "|\n");
    };
    fprintf(hf, "--+");
    for (x = 0; x < width; x++ ) {
        fprintf(hf, "-" );
    };
    fprintf(hf,"+\n");

}
#endif

int loadSortedTetroTypes(
    char *fileName, 
    char *sortedTetroTypes, 
    int numTetroTypes) 
{
    FILE *indata;
    int readCount = 0;
    char *in = sortedTetroTypes;

    indata = fopen(fileName, "r");
    if (!indata) 
        return -1;

    while ((readCount <= numTetroTypes) && !feof(indata)) {
        readCount += fscanf(indata, "%c", in++);
    }
    fclose(indata);

    return readCount;
}
