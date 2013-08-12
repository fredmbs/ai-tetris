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
Tetris Simulador de alta performance para avaliação de orgnanismo (gene)
-------------------------------------------------------------------------
*/

#include <float.h>
#include <stdlib.h>
#include <limits.h>

#include "board.h"
#include "GeneticTetris.h"

long TetrisGame(int height, int width, GENOME gene, 
                char *sortedTetroTypes, int numTetroTypes,
                STATISTICS *clines) 
{

    int tetroType;
    TETROMINOS tetrominos;
    TETROMINO tetromino;
    BOARD board;
    int notGameOver;
    int tetroCount;
    int r;
    //
    BOARD  best_board;
    double best_evaluation;
    int    best_orientation;
    int    best_column;
    int    best_priority;
    int    best_board_rowsRemoved;
    //
    long score;
    STATISTICS local_clines;
    int moviments;
    int rowsScoringFactors[5];
    int spawRow, spawCol;
    int completedLine;
    int maxCol = width - 1;
    int orientation;
    //
    SHAPE shape;
    int shapeHeight;
    int col;
    int numColsPerMoviment;


    // pre-conditions: board limits verification
    if ((height > MAX_LINES) || (width > ((sizeof(int)*8) - 1))) {
        return -1;
    }

    configureTetro(tetrominos);

    // The board is represented as an array of integers, 
    // one integer for each row.
    board.height = height;
    board.width = width;
    for (r = 0; r < height; r++) {
        board.line[r] = 0;
    }

    rowsScoringFactors[0] = 0;
    rowsScoringFactors[1] = 40;
    rowsScoringFactors[2] = 100;
    rowsScoringFactors[3] = 3000;
    rowsScoringFactors[4] = 1200;
    moviments = 0;
    for (r = 0; r < LINE_RANGE; r++)
        local_clines[r] = 0;

    spawCol = (1 + (int)(width/2));
    spawRow = height - 2;
    score = 0;
    tetroCount = 0;
    completedLine = (1 << width) - 1;
    notGameOver = 1;
    while (notGameOver && (tetroCount < numTetroTypes)) {
        tetroType = sortedTetroTypes[tetroCount] - '0';
        tetroCount++;

        tetromino = tetrominos[tetroType];

        notGameOver = 0;
        best_orientation = 0;
        best_column = 0;
        best_evaluation = -DBL_MAX;
        best_priority = -INT_MAX;
        best_board = board;
        best_board_rowsRemoved = 0;

        // Evaluate all possible orientations
        for (orientation = 0; orientation < tetromino.orientations; orientation++) 
        {
            shape = tetromino.shape[orientation];
            shapeHeight = shape.height;
            numColsPerMoviment = width - shape.width;
            moviments += numColsPerMoviment;
            // Evaluate all possible columns
            #pragma omp parallel for 
            for (col = numColsPerMoviment; col >= 0; col--) 
            {
                int row;
                int placementRow;
                BOARD tboard;
                int pcol;
                int i, ii;
                LINE tline;
                LINE originalLine;
                LINE actualLine;
                double evaluation;
                int priority;
                int rowsRemoved, piecesRemoved;
                double landingHeight;
                int erodedPieceCellsMetric;
                int boardRowTransitions;
                int boardColTransitions;
                int boardBuriedHoles;
                int boardWells;
                int pileHeight;
                SHAPE tshape;
                int shift;

                // movePiece to the next column
                tshape = shape;
                shift = width - (col + shape.width);
                tshape.line[0] <<= shift;
                tshape.line[1] <<= shift;
                tshape.line[2] <<= shift;
                tshape.line[3] <<= shift;

                tboard = board;
                // Given a piece, return the row at which it should be placed.
                // Descend from top to find the highest row that will collide
                // with the our piece.
                for (row = height - shapeHeight; row >= 0; row--) {
                    // Check if piece collides with the cells of the current row.
                    // verifying by adding row to going up (represented by ii++) and 
                    // reducing height of tetromino (represented by i--)
                    ii = row;
                    for (i = shapeHeight - 1; i >= 0 ; i--) {
                        if (board.line[ii++] & tshape.line[i]){
                            // Found collision - place piece on row above.
                            placementRow = row + 1;
                            goto placementFound;
                        }
                    }
                }
                placementRow = 0;
                placementFound:

                // if not game over.
                if ((placementRow + shapeHeight) < height) 
                {
                    notGameOver = 1;
                    // -- Copy original board to test board 
                    // -- (removing completed lines)
                    // Add lines below the placement
                    for (i = 0; i < placementRow; i++) {
                        tboard.line[i] = board.line[i];
                    }
                    // Add lines between placement and top of the shape 
                    // testing completed lines  
                    // (do not copy completed line to test board)
                    originalLine = placementRow;
                    actualLine = placementRow;
                    // start erosion metrics
                    rowsRemoved = 0;
                    piecesRemoved = 0;
                    for (i = shapeHeight - 1; i >= 0 ; i--) {
                        tline = board.line[originalLine++] | tshape.line[i];
                        if (tline == completedLine) {
                            rowsRemoved++;
                            piecesRemoved += tshape.piecesPerLine[i];
                        } else {
                            tboard.line[actualLine++] = tline;
                        }
                    }
                    // Add original board remaining lines
                    while (originalLine < height) {
                        tboard.line[actualLine++] = board.line[originalLine++];
                    }
                    // Add blank lines at begining (removed lines)
                    while (actualLine < height) {
                         tboard.line[actualLine++] = 0;
                    }

                    // evaluete the movement 
                    landingHeight = placementRow + ((double)(shapeHeight - 1) / 2) + 1;
                    erodedPieceCellsMetric = (rowsRemoved * piecesRemoved);
                    boardRowTransitions = GetRowTransitions(&tboard, &pileHeight);
                    boardColTransitions = GetColumnTransitions(&tboard);
                    boardBuriedHoles = GetNumberOfHoles(&tboard);
                    boardWells = GetWellSums(&tboard);

                    evaluation = 
                        (gene[PILE_HEIGHT]        * pileHeight) +
                        (gene[LANDING_HEIGHT]     * landingHeight) +
                        (gene[ERODED_PIECES]      * piecesRemoved) +
                        (gene[ERODED_ROWS]        * rowsRemoved) +
                        (gene[ERODED_METRIC]      * erodedPieceCellsMetric) + 
                        (gene[ROW_TRANSITIONS]    * boardRowTransitions) + 
                        (gene[COLUMN_TRANSITIONS] * boardColTransitions) +
                        (gene[COLUMN_BURIEDHOLES] * boardBuriedHoles) +
                        (gene[COLUMN_WELLS]       * boardWells);

                    // 
                    pcol = col + tshape.deltaCol + 1;
                    if (pcol < spawCol)  {
                        priority = 10 + (100 * abs(pcol - spawCol)) - orientation; 
                    }  else {
                        priority = (100 * abs(pcol - spawCol)) - orientation; 
                    }

                    #pragma omp critical
                    {
                        if ((evaluation >  best_evaluation) ||
                           ((evaluation == best_evaluation) &&
                            (priority   >  best_priority))) 
                        {
                            best_board = tboard;
                            best_orientation = orientation; 
                            best_column = col; 
                            best_evaluation = evaluation;
                            best_priority = priority;
                            best_board_rowsRemoved = rowsRemoved;
                        }
                    }
                }
            }
        }
        score += rowsScoringFactors[best_board_rowsRemoved];
        local_clines[best_board_rowsRemoved] += 1;
        board = best_board;
    }

    for (r = 0; r < LINE_RANGE; r++)
        (*clines)[r] = local_clines[r];
    (*clines)[STATISTIC_TETROCOUNTS] = tetroCount;
    (*clines)[STATISTIC_EVALUATIONS] = moviments;

    return score;
};
