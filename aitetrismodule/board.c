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
Análise do tabuleiro do Jogo Tetris
-------------------------------------------------------------------------
*/

#include "board.h"

int GetRowTransitions(BOARD *board, int *pileHeight) {
    int maxCol = board->width - 1;
    int maxRow = board->height - 1;
    int transitions = 0;
    int last_bit = 1;
    int rowData, row, col;
    int bit = 0;
    int pHeight = 0;

    for (row = maxRow; row >= 0; --row) {
        rowData = board->line[row];
        if (rowData) pHeight++;
        for (col = maxCol; col >= 0; --col) {
            bit = (rowData >> col) & 1;
      
            if (bit != last_bit) {
                ++transitions;
            }

            last_bit = bit;
        }

        if (bit == 0) {
            ++transitions;
        }
        last_bit = 1;
    }
    *pileHeight = pHeight;
    return transitions;
}

int GetColumnTransitions(BOARD *board) {
    int maxCol = board->width - 1;
    int maxRow = board->height - 1;
    int transitions = 0;
    int last_bit = 1;
    int row, col;
    int bit;

    for (col = maxCol; col >= 0; --col) {
        for (row = 0; row <= maxRow; ++row) {
            bit = (board->line[row] >> col) & 1;
      
            if (bit != last_bit) {
                ++transitions;
            }

            last_bit = bit;
        }

        last_bit = 1;
    }
  
    return transitions;
}

int GetNumberOfHoles(BOARD *board) {
    int maxCol = board->width - 1;
    int maxRow = board->height - 1;
    int holes = 0;
    int row_holes = 0x0000;
    int previous_row = board->line[maxRow];
    int row, col;

    for (row = maxRow - 1; row >= 0; --row) {
        row_holes = (~board->line[row]) & (previous_row | row_holes);

        if (row_holes) {
            for (col = maxCol; col >= 0; --col) {
                holes += ((row_holes >> col) & 1);
            }
        }

        previous_row = board->line[row];
  }

  return holes;
}

int GetWellSums(BOARD *board) {
    int maxCol = board->width - 1;
    int maxRow = board->height - 1;
    int well_sums = 0;
    int rowData, row, col;
    int rowBelow;

    for (col = maxCol - 1; col > 0; --col) {
        for (row = maxRow; row >= 0; --row) {
            rowData = board->line[row];
            if ((!((rowData >>  col)      & 1)) && 
                  ((rowData >> (col - 1)) & 1) &&
                  ((rowData >> (col + 1)) & 1)) {
            // Found well cell, count it + the number of empty cells below it.

                ++well_sums;
                for (rowBelow = row - 1; rowBelow >= 0; --rowBelow) {
                    if (!((board->line[rowBelow] >> col) & 1)) {
                        ++well_sums;
                    } else {
                        break;
                    }
                }
            }
        }
    }

    for (row = maxRow; row >= 0; --row) {
        rowData = board->line[row];
        if ((!(rowData        & 1)) && 
              ((rowData >> 1) & 1)) {
            // Found well cell, count it + the number of empty cells below it.

            ++well_sums;
            for (rowBelow = row - 1; rowBelow >= 0; --rowBelow) {
                if (!(board->line[rowBelow] & 1)) {
                    ++well_sums;
                } else {
                    break;
                }
            }
        }
    }

    for (row = maxRow; row >= 0; --row) {
        rowData = board->line[row];
        if ((!((rowData >>  maxCol     ) & 1)) && 
              ((rowData >> (maxCol - 1)) & 1)) {
            // Found well cell, count it + the number of empty cells below it.

            ++well_sums;
            for (rowBelow = row - 1; rowBelow >= 0; --rowBelow) {
                if (!((board->line[rowBelow] >> maxCol) & 1)) {
                    ++well_sums;
                } else {
                    break;
                }
            }
        }
    }

    return well_sums;
}