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
Montagem dos tetrominos
-------------------------------------------------------------------------
*/

/**
 * Defines the shapes and dimensions of the tetrominoes.
 */
#include "tetromino.h"

void configureTetro(TETROMINOS tetro) {

        // NULL tetromino
        tetro[0].orientations = 0;

        // O
        tetro[1].orientations = 1;
        // 0 degrees
        tetro[1].shape[0].line[0] = 3; // 11
        tetro[1].shape[0].line[1] = 3; // 11
        tetro[1].shape[0].line[2] = 0; // 00
        tetro[1].shape[0].line[3] = 0; // 00
        tetro[1].shape[0].piecesPerLine[0] = 2; 
        tetro[1].shape[0].piecesPerLine[1] = 2; 
        tetro[1].shape[0].piecesPerLine[2] = 0; 
        tetro[1].shape[0].piecesPerLine[3] = 0; 
        tetro[1].shape[0].height = 2;
        tetro[1].shape[0].width = 2;
        tetro[1].shape[0].deltaRow = 1;
        tetro[1].shape[0].deltaCol = 1;

        // I
        tetro[2].orientations = 2;
        // 0 & 180 degrees
        tetro[2].shape[0].line[0] = 15; // 1111
        tetro[2].shape[0].line[1] = 0;  // 000
        tetro[2].shape[0].line[2] = 0;  // 000
        tetro[2].shape[0].line[3] = 0;  // 000
        tetro[2].shape[0].piecesPerLine[0] = 4; 
        tetro[2].shape[0].piecesPerLine[1] = 0; 
        tetro[2].shape[0].piecesPerLine[2] = 0; 
        tetro[2].shape[0].piecesPerLine[3] = 0; 
        tetro[2].shape[0].height = 1;
        tetro[2].shape[0].width = 4;
        tetro[2].shape[0].deltaRow = 0;
        tetro[2].shape[0].deltaCol = 2;
        // 90 & 270 degrees
        tetro[2].shape[1].line[0] = 1; // 1
        tetro[2].shape[1].line[1] = 1; // 1
        tetro[2].shape[1].line[2] = 1; // 1
        tetro[2].shape[1].line[3] = 1; // 1
        tetro[2].shape[1].piecesPerLine[0] = 1; 
        tetro[2].shape[1].piecesPerLine[1] = 1; 
        tetro[2].shape[1].piecesPerLine[2] = 1; 
        tetro[2].shape[1].piecesPerLine[3] = 1; 
        tetro[2].shape[1].height = 4;
        tetro[2].shape[1].width = 1;
        tetro[2].shape[1].deltaRow = 2;
        tetro[2].shape[1].deltaCol = 0;

        // S
        tetro[3].orientations = 2;
        // 0 & 180 degrees
        tetro[3].shape[0].line[0] = 3;  // 011
        tetro[3].shape[0].line[1] = 6;  // 110
        tetro[3].shape[0].line[2] = 0;  // 000
        tetro[3].shape[0].line[3] = 0;  // 000
        tetro[3].shape[0].piecesPerLine[0] = 2; 
        tetro[3].shape[0].piecesPerLine[1] = 2; 
        tetro[3].shape[0].piecesPerLine[2] = 0; 
        tetro[3].shape[0].piecesPerLine[3] = 0; 
        tetro[3].shape[0].height = 2;
        tetro[3].shape[0].width = 3;
        tetro[3].shape[0].deltaRow = 1;
        tetro[3].shape[0].deltaCol = 1;
        // 90 & 270 degrees
        tetro[3].shape[1].line[0] = 2; // 10
        tetro[3].shape[1].line[1] = 3; // 11
        tetro[3].shape[1].line[2] = 1; // 01
        tetro[3].shape[1].line[3] = 0; // 00
        tetro[3].shape[1].piecesPerLine[0] = 1; 
        tetro[3].shape[1].piecesPerLine[1] = 2; 
        tetro[3].shape[1].piecesPerLine[2] = 1; 
        tetro[3].shape[1].piecesPerLine[3] = 0; 
        tetro[3].shape[1].height = 3;
        tetro[3].shape[1].width = 2;
        tetro[3].shape[1].deltaRow = 1;
        tetro[3].shape[1].deltaCol = 0;


        // Z
        tetro[4].orientations = 2;
        // 0 & 180 degrees
        tetro[4].shape[0].line[0] = 6;  // 110
        tetro[4].shape[0].line[1] = 3;  // 011
        tetro[4].shape[0].line[2] = 0;  // 000
        tetro[4].shape[0].line[3] = 0;  // 000
        tetro[4].shape[0].piecesPerLine[0] = 2; 
        tetro[4].shape[0].piecesPerLine[1] = 2; 
        tetro[4].shape[0].piecesPerLine[2] = 0; 
        tetro[4].shape[0].piecesPerLine[3] = 0; 
        tetro[4].shape[0].height = 2;
        tetro[4].shape[0].width = 3;
        tetro[4].shape[0].deltaRow = 1;
        tetro[4].shape[0].deltaCol = 1;
        // 90 & 270 degrees
        tetro[4].shape[1].line[0] = 1; // 01
        tetro[4].shape[1].line[1] = 3; // 11
        tetro[4].shape[1].line[2] = 2; // 10
        tetro[4].shape[1].line[3] = 0; // 00
        tetro[4].shape[1].piecesPerLine[0] = 1; 
        tetro[4].shape[1].piecesPerLine[1] = 2; 
        tetro[4].shape[1].piecesPerLine[2] = 1; 
        tetro[4].shape[1].piecesPerLine[3] = 0; 
        tetro[4].shape[1].height = 3;
        tetro[4].shape[1].width = 2;
        tetro[4].shape[1].deltaRow = 1;
        tetro[4].shape[1].deltaCol = 0;

        
        // L
        tetro[5].orientations = 4;
        // 0 degrees
        tetro[5].shape[0].line[0] = 7;  // 111
        tetro[5].shape[0].line[1] = 4;  // 100
        tetro[5].shape[0].line[2] = 0;  // 000
        tetro[5].shape[0].line[3] = 0;  // 000
        tetro[5].shape[0].piecesPerLine[0] = 3; 
        tetro[5].shape[0].piecesPerLine[1] = 1; 
        tetro[5].shape[0].piecesPerLine[2] = 0; 
        tetro[5].shape[0].piecesPerLine[3] = 0; 
        tetro[5].shape[0].height = 2;
        tetro[5].shape[0].width = 3;
        tetro[5].shape[0].deltaRow = 1;
        tetro[5].shape[0].deltaCol = 1;
        // 90 degrees
        tetro[5].shape[1].line[0] = 2; // 10
        tetro[5].shape[1].line[1] = 2; // 10
        tetro[5].shape[1].line[2] = 3; // 11
        tetro[5].shape[1].line[3] = 0; // 00
        tetro[5].shape[1].piecesPerLine[0] = 1; 
        tetro[5].shape[1].piecesPerLine[1] = 1; 
        tetro[5].shape[1].piecesPerLine[2] = 2; 
        tetro[5].shape[1].piecesPerLine[3] = 0; 
        tetro[5].shape[1].height = 3;
        tetro[5].shape[1].width = 2;
        tetro[5].shape[1].deltaRow = 1;
        tetro[5].shape[1].deltaCol = 0;

        // 180 degrees
        tetro[5].shape[2].line[0] = 1;  // 001
        tetro[5].shape[2].line[1] = 7;  // 111
        tetro[5].shape[2].line[2] = 0;  // 000
        tetro[5].shape[2].line[3] = 0;  // 000
        tetro[5].shape[2].piecesPerLine[0] = 1; 
        tetro[5].shape[2].piecesPerLine[1] = 3; 
        tetro[5].shape[2].piecesPerLine[2] = 0; 
        tetro[5].shape[2].piecesPerLine[3] = 0; 
        tetro[5].shape[2].height = 2;
        tetro[5].shape[2].width = 3;
        tetro[5].shape[2].deltaRow = 0;
        tetro[5].shape[2].deltaCol = 1;
        // 270 degrees
        tetro[5].shape[3].line[0] = 3; // 11
        tetro[5].shape[3].line[1] = 1; // 01
        tetro[5].shape[3].line[2] = 1; // 01
        tetro[5].shape[3].line[3] = 0; // 00
        tetro[5].shape[3].piecesPerLine[0] = 2; 
        tetro[5].shape[3].piecesPerLine[1] = 1; 
        tetro[5].shape[3].piecesPerLine[2] = 1; 
        tetro[5].shape[3].piecesPerLine[3] = 0; 
        tetro[5].shape[3].height = 3;
        tetro[5].shape[3].width = 2;
        tetro[5].shape[3].deltaRow = 1;
        tetro[5].shape[3].deltaCol = 1;

        // J
        tetro[6].orientations = 4;
        // 0 degrees
        tetro[6].shape[0].line[0] = 7;  // 111
        tetro[6].shape[0].line[1] = 1;  // 001
        tetro[6].shape[0].line[2] = 0;  // 000
        tetro[6].shape[0].line[3] = 0;  // 000
        tetro[6].shape[0].piecesPerLine[0] = 3; 
        tetro[6].shape[0].piecesPerLine[1] = 1; 
        tetro[6].shape[0].piecesPerLine[2] = 0; 
        tetro[6].shape[0].piecesPerLine[3] = 0; 
        tetro[6].shape[0].height = 2;
        tetro[6].shape[0].width = 3;
        tetro[6].shape[0].deltaRow = 1;
        tetro[6].shape[0].deltaCol = 1;
        // 90 degrees
        tetro[6].shape[1].line[0] = 3; // 11
        tetro[6].shape[1].line[1] = 2; // 10
        tetro[6].shape[1].line[2] = 2; // 10
        tetro[6].shape[1].line[3] = 0; // 00
        tetro[6].shape[1].piecesPerLine[0] = 2; 
        tetro[6].shape[1].piecesPerLine[1] = 1; 
        tetro[6].shape[1].piecesPerLine[2] = 1; 
        tetro[6].shape[1].piecesPerLine[3] = 0; 
        tetro[6].shape[1].height = 3;
        tetro[6].shape[1].width = 2;
        tetro[6].shape[1].deltaRow = 1;
        tetro[6].shape[1].deltaCol = 0;

        // 180 degrees
        tetro[6].shape[2].line[0] = 4;  // 100
        tetro[6].shape[2].line[1] = 7;  // 111
        tetro[6].shape[2].line[2] = 0;  // 000
        tetro[6].shape[2].line[3] = 0;  // 000
        tetro[6].shape[2].piecesPerLine[0] = 1; 
        tetro[6].shape[2].piecesPerLine[1] = 3; 
        tetro[6].shape[2].piecesPerLine[2] = 0; 
        tetro[6].shape[2].piecesPerLine[3] = 0; 
        tetro[6].shape[2].height = 2;
        tetro[6].shape[2].width = 3;
        tetro[6].shape[2].deltaRow = 0;
        tetro[6].shape[2].deltaCol = 1;
        // 270 degrees
        tetro[6].shape[3].line[0] = 1; // 01
        tetro[6].shape[3].line[1] = 1; // 01
        tetro[6].shape[3].line[2] = 3; // 11
        tetro[6].shape[3].line[3] = 0; // 00
        tetro[6].shape[3].piecesPerLine[0] = 1; 
        tetro[6].shape[3].piecesPerLine[1] = 1; 
        tetro[6].shape[3].piecesPerLine[2] = 2; 
        tetro[6].shape[3].piecesPerLine[3] = 0; 
        tetro[6].shape[3].height = 3;
        tetro[6].shape[3].width = 2;
        tetro[6].shape[3].deltaRow = 1;
        tetro[6].shape[3].deltaCol = 1;


        // T
        tetro[7].orientations = 4;
        // 0 degrees
        tetro[7].shape[0].line[0] = 7;  // 111
        tetro[7].shape[0].line[1] = 2;  // 010
        tetro[7].shape[0].line[2] = 0;  // 000
        tetro[7].shape[0].line[3] = 0;  // 000
        tetro[7].shape[0].piecesPerLine[0] = 3; 
        tetro[7].shape[0].piecesPerLine[1] = 1; 
        tetro[7].shape[0].piecesPerLine[2] = 0; 
        tetro[7].shape[0].piecesPerLine[3] = 0; 
        tetro[7].shape[0].height = 2;
        tetro[7].shape[0].width = 3;
        tetro[7].shape[0].deltaRow = 1;
        tetro[7].shape[0].deltaCol = 1;
        // 90 degrees
        tetro[7].shape[1].line[0] = 2; // 10
        tetro[7].shape[1].line[1] = 3; // 11
        tetro[7].shape[1].line[2] = 2; // 10
        tetro[7].shape[1].line[3] = 0; // 00
        tetro[7].shape[1].piecesPerLine[0] = 1; 
        tetro[7].shape[1].piecesPerLine[1] = 2; 
        tetro[7].shape[1].piecesPerLine[2] = 1; 
        tetro[7].shape[1].piecesPerLine[3] = 0; 
        tetro[7].shape[1].height = 3;
        tetro[7].shape[1].width = 2;
        tetro[7].shape[1].deltaRow = 1;
        tetro[7].shape[1].deltaCol = 0;
        // 180 degrees
        tetro[7].shape[2].line[0] = 2;  // 010
        tetro[7].shape[2].line[1] = 7;  // 111
        tetro[7].shape[2].line[2] = 0;  // 000
        tetro[7].shape[2].line[3] = 0;  // 000
        tetro[7].shape[2].piecesPerLine[0] = 1; 
        tetro[7].shape[2].piecesPerLine[1] = 3; 
        tetro[7].shape[2].piecesPerLine[2] = 0; 
        tetro[7].shape[2].piecesPerLine[3] = 0; 
        tetro[7].shape[2].height = 2;
        tetro[7].shape[2].width = 3;
        tetro[7].shape[2].deltaRow = 0;
        tetro[7].shape[2].deltaCol = 1;
        // 270 degrees
        tetro[7].shape[3].line[0] = 1; // 01
        tetro[7].shape[3].line[1] = 3; // 11
        tetro[7].shape[3].line[2] = 1; // 01
        tetro[7].shape[3].line[3] = 0; // 00
        tetro[7].shape[3].piecesPerLine[0] = 1; 
        tetro[7].shape[3].piecesPerLine[1] = 2; 
        tetro[7].shape[3].piecesPerLine[2] = 1; 
        tetro[7].shape[3].piecesPerLine[3] = 0; 
        tetro[7].shape[3].height = 3;
        tetro[7].shape[3].width = 2;
        tetro[7].shape[3].deltaRow = 1;
        tetro[7].shape[3].deltaCol = 1;
        
}

