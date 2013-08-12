#ifndef PIECE_H
#define PIECE_H
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
Tipos e funções de manipulação de tetrominos
-------------------------------------------------------------------------
*/

/**
 * Defines the shapes and dimensions of the tetrominoes.
 */
#define TETRO_COUNT  8
#define TETRO_RANGE  7

typedef long int LINE;

typedef struct {
        LINE line[4];
        int piecesPerLine[4];
        int height;
        int width;
        int orientation;
        int deltaRow;
        int deltaCol;
    } SHAPE;

typedef struct {
        SHAPE shape[4];
        int orientations;
    } TETROMINO;

typedef TETROMINO TETROMINOS[TETRO_COUNT];

void configureTetro(TETROMINOS tetro);

#endif