#ifndef PIECE_H
#define PIECE_H
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
Tipos e fun��es de manipula��o de tetrominos
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