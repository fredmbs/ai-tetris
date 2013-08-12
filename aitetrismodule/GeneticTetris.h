#ifndef GENETIC_TETRIS_H
#define GENETIC_TETRIS_H
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
Genoma utilizado na otimiza��o
-------------------------------------------------------------------------
*/

// list of genes by traits used in genetic algorithm
#define     PILE_HEIGHT            0
#define     LANDING_HEIGHT         1
#define     ERODED_PIECES          2
#define     ERODED_ROWS            3
#define     ERODED_METRIC          4
#define     ROW_TRANSITIONS        5
#define     COLUMN_TRANSITIONS     6
#define     COLUMN_BURIEDHOLES     7
#define     COLUMN_WELLS           8
#define     NUM_GENES              9

#define     LINE_RANGE             5
#define     STATISTICS_RANGE       7
#define     STATISTIC_TETROCOUNTS  5
#define     STATISTIC_EVALUATIONS  6

typedef double GENOME[NUM_GENES];
typedef int STATISTICS[STATISTICS_RANGE];



long TetrisGame(int height, int width, GENOME gene, 
                char *sortedTetroTypes, int numTetroTypes,
                STATISTICS *clines);

#endif