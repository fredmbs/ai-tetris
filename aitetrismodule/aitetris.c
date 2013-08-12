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
Módulo Python
-------------------------------------------------------------------------
*/

#include "utils.h"
#include "GeneticTetris.h"

#ifndef DEBUG
    #include "Python.h"
#else
    #include <stdio.h> 
    #include <stdlib.h>
    #ifdef WIN32
        #include <windows.h>
        #define DEFAULT_GAME "C:\\dev\\IA\\GeneticTeris\\database\\TetrisGame.txt"
    #else
        #define DEFAULT_GAME "TetrisGame.txt"
    #endif
    #define DEFAULT_TETRO_COUNT 10000000
#endif

#ifndef DEBUG

static PyObject *aiplay(PyObject *self, PyObject *args)
{
    char *strArg = NULL;
    long score = 0;
    STATISTICS lines;
    int height, weigth, tetroCount;
    GENOME chromosome;

    PyObject *genome;
    PyObject *gene;
    long length;
    int i;

    if (!PyArg_ParseTuple(args, "iiOsi", &height, &weigth, 
                          &genome, &strArg, &tetroCount)) {
        PyErr_BadArgument();
        return NULL;
    }

    if (!PyList_Check(genome)) {
        PyErr_SetString(PyExc_TypeError,"Third argument must to be a list");
        return NULL;
    }

    if (strArg == NULL) {
        PyErr_SetString(PyExc_TypeError,"Fourth argument must to be a tetromino sequence string");
        return NULL;
    }

    if ((length = PyList_Size(genome)) != NUM_GENES) {
        PyErr_SetString(PyExc_TypeError,"Number of genes in chromosome is invalid");
        return NULL;
    }

    for (i = 0; i < length; i++) {
        if (!(gene = PyList_GetItem(genome, i))) {
            PyErr_SetString(PyExc_TypeError,"Chromosome invalid format");
            return NULL;
        }

        if (PyFloat_Check(gene)) {
            chromosome[i] = PyFloat_AsDouble(gene);
            continue;
        }

        if (PyInt_Check(gene)) {
            chromosome[i] = (double)PyInt_AsLong(gene);
            continue;
        }

        PyErr_SetString(PyExc_TypeError,"Chromosome must contain int or float types");
        return NULL;
    }
    score = TetrisGame(height, weigth, chromosome, strArg, tetroCount, &lines);
    return Py_BuildValue("l", score);
}

static PyObject *aiplay_lines(PyObject *self, PyObject *args)
{
    char *strArg = NULL;
    long score = 0;
    STATISTICS lines;
    int height, weigth, tetroCount;
    GENOME chromosome;

    PyObject *genome;
    PyObject *gene;
    long length;
    int i;

    PyObject* result;

    if (!PyArg_ParseTuple(args, "iiOsi", &height, &weigth, 
                          &genome, &strArg, &tetroCount)) {
        PyErr_BadArgument();
        return NULL;
    }

    if (!PyList_Check(genome)) {
        PyErr_SetString(PyExc_TypeError,"Third argument must to be a list");
        return NULL;
    }

    if (strArg == NULL) {
        PyErr_SetString(PyExc_TypeError,"Fourth argument must to be a tetromino sequence string");
        return NULL;
    }

    if ((length = PyList_Size(genome)) != NUM_GENES) {
        PyErr_SetString(PyExc_TypeError,"Number of genes in chromosome is invalid");
        return NULL;
    }

    for (i = 0; i < length; i++) {
        if (!(gene = PyList_GetItem(genome, i))) {
            PyErr_SetString(PyExc_TypeError,"Chromosome invalid format");
            return NULL;
        }

        if (PyFloat_Check(gene)) {
            chromosome[i] = PyFloat_AsDouble(gene);
            continue;
        }

        if (PyInt_Check(gene)) {
            chromosome[i] = (double)PyInt_AsLong(gene);
            continue;
        }

        PyErr_SetString(PyExc_TypeError,"Chromosome must contain int or float types");
        return NULL;
    }
    score = TetrisGame(height, weigth, chromosome, strArg, tetroCount, &lines);
    
    result = PyTuple_New(8);
    PyTuple_SET_ITEM(result, 0, Py_BuildValue("i", lines[0]));
    PyTuple_SET_ITEM(result, 1, Py_BuildValue("i", lines[1]));
    PyTuple_SET_ITEM(result, 2, Py_BuildValue("i", lines[2]));
    PyTuple_SET_ITEM(result, 3, Py_BuildValue("i", lines[3]));
    PyTuple_SET_ITEM(result, 4, Py_BuildValue("i", lines[4]));
    PyTuple_SET_ITEM(result, 5, Py_BuildValue("i", lines[5]));
    PyTuple_SET_ITEM(result, 6, Py_BuildValue("i", lines[6]));
    PyTuple_SET_ITEM(result, 7, Py_BuildValue("l", score));

    return result;
}

static PyObject *
aiplay_file(PyObject *self, PyObject *args)
{
    char *strArg = NULL;
    char *sortedTetroTypes;
    long score = 0;
    STATISTICS lines;
    int height, weigth, tetroCount;
    GENOME chromosome;
    PyObject *result = NULL;

    PyObject *genome;
    PyObject *gene;
    long length;
    int i;

    if (!PyArg_ParseTuple(args, "iiOsi", &height, &weigth, 
                          &genome, &strArg, &tetroCount)) {
        PyErr_BadArgument();
        return NULL;
    }

    if (!PyList_Check(genome)) {
        PyErr_SetString(PyExc_TypeError,"Third argument must to be a list");
        return NULL;
    }

    if (strArg == NULL) {
        PyErr_SetString(PyExc_TypeError,"Fourth argument must to be a file name string");
        return NULL;
    }

    if ((length = PyList_Size(genome)) != NUM_GENES) {
        PyErr_SetString(PyExc_TypeError,"Number of genes in chromosome is invalid");
        return NULL;
    }

    for (i = 0; i < length; i++) {
        if (!(gene = PyList_GetItem(genome, i))) {
            PyErr_SetString(PyExc_TypeError,"Chromosome invalid format");
            return NULL;
        }

        if (PyFloat_Check(gene)) {
            chromosome[i] = PyFloat_AsDouble(gene);
            continue;
        }

        if (PyInt_Check(gene)) {
            chromosome[i] = (double)PyInt_AsLong(gene);
            continue;
        }

        PyErr_SetString(PyExc_TypeError,"Chromosome must contain int or float types");
        return NULL;
    }

    sortedTetroTypes = (char *)PyMem_Malloc(tetroCount);
    tetroCount = loadSortedTetroTypes(strArg, sortedTetroTypes, tetroCount);
    if (tetroCount < 0) {
        PyErr_SetString(PyExc_IOError,"Game file reading problem");
    } 
    else {
        score = TetrisGame(height, weigth, chromosome, 
                           sortedTetroTypes, tetroCount, &lines);
        result = Py_BuildValue("l", score);
    }
    PyMem_Free(sortedTetroTypes);
    return result;
    
}

static PyMethodDef aitetris_methods[] = {
    {"play", aiplay, METH_VARARGS, "Play game. Returns score."},
    {"play_lines", aiplay_lines, METH_VARARGS, "Play game. Returns line removed and score in tuple."},
    {"play_file", aiplay_file, METH_VARARGS, "Play game stored in file. Returns score."},
    {NULL, NULL}
};

PyMODINIT_FUNC
initaitetris(void)
{
    Py_InitModule("aitetris", aitetris_methods);
}

#else

int main(int argc, const char* argv[]) {

#ifdef WIN32
    __int64 ctr1 = 0, ctr2 = 0, freq = 0;
    double elapsedTime;
#endif

    int i;
    long score;
    GENOME chromosome;
    char *sortedTetroTypes;
    char *fileName;
    int tetroCount = DEFAULT_TETRO_COUNT;
    int height = 20;
    int weigth = 10;



    for (i =0; i < NUM_GENES; i++)
        chromosome[i] = 0.0;

    /*
    // PierreDellacherie
    chromosome[LANDING_HEIGHT]     = -1.0;
    chromosome[ERODED_METRIC]      = +1.0;
    chromosome[ROW_TRANSITIONS]    = -1.0;
    chromosome[COLUMN_TRANSITIONS] = -1.0;
    chromosome[COLUMN_BURIEDHOLES] = -4.0;
    chromosome[COLUMN_WELLS]       = -1.0;
    */

    chromosome[PILE_HEIGHT]        = -0.6903200846016033;
    chromosome[LANDING_HEIGHT]     = -48.397173471721274;
    chromosome[ERODED_PIECES]      = +29.57801575198271;
    chromosome[ERODED_ROWS]        = +4.947969428674859;
    chromosome[ERODED_METRIC]      = +0.9258831965633374;
    chromosome[ROW_TRANSITIONS]    = -24.337463194268338;
    chromosome[COLUMN_TRANSITIONS] = -72.90931022325682;
    chromosome[COLUMN_BURIEDHOLES] = -93.26927285333721;
    chromosome[COLUMN_WELLS]       = -38.827245269520624;

#ifdef WIN32

    if (QueryPerformanceCounter((LARGE_INTEGER *)&ctr1)!= 0)
    {
#endif
        if (argc == 1) {
            fileName = DEFAULT_GAME;
        } else {
            fileName = (char *)argv[1];
        }
        sortedTetroTypes = (char *)malloc(tetroCount);
        tetroCount = loadSortedTetroTypes(fileName, 
                                          sortedTetroTypes, 
                                          tetroCount);
        if (tetroCount < 0) {
            free(sortedTetroTypes);
            printf("ERROR: Game file reading problem = %s\n", fileName);
            return 1;
        } 

        score = TetrisGame(height, weigth, chromosome, 
                           sortedTetroTypes, tetroCount);
        free(sortedTetroTypes);
        printf("Score : %Li \n",score);

#ifdef WIN32
        // Finish timing the code.
        QueryPerformanceCounter((LARGE_INTEGER *)&ctr2);

        printf("Start Value: %Ld\n",ctr1);
        printf("End Value  : %Ld\n",ctr2);
        QueryPerformanceFrequency((LARGE_INTEGER *)&freq);

        printf("QueryPerformanceCounter minimum resolution: 1/%Ld Seconds.\n",freq);
        elapsedTime = ((ctr2 - ctr1) * (1.0 / freq));
        printf("Time: %Lf seconds.\n", elapsedTime);
    }
    else
    {
        DWORD dwError = GetLastError();
        printf("Error value = %u\n",dwError);
    }
#endif
    return 0;
}

#endif
