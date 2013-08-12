#!/usr/bin/python
# -*- coding:utf-8 -*-
# This is an aitetris of a distutils 'setup' script 
#
# USAGE: you probably want 'setup.py install' or 'python setup.py install'
#  - but execute 'setup.py --help' for all the details.
#=========================================================================
#/*                            
#UNI-BH - Centro Universit�rio de Belo Horizonte
#DCET   - Departamento de Ci�ncias Exatas e Tecnol�gicas
#-------------------------------------------------------------------------
#Ci�ncia da Computa��o
#IA - Intelig�ncia Artifical
#Professora - Ana Paula ladeira
#-------------------------------------------------------------------------
#Trabalho Pr�tico: Algor�tmos Gen�ticos - Otimiza��o do Tetris
#Alunos:  Frederico Martins Biber Sampaio
#         Guilherme Brand�o Biber Sampaio
#         Gustavo Pantuza Coelho Pinto
#-------------------------------------------------------------------------
# Arquivo de gera��o do m�dulo de simula��o do tetris
#-------------------------------------------------------------------------
#*/
#
from distutils.core import setup, Extension

aitetris_mod = Extension(
      'aitetris', 
      sources = ['aitetris.c', 'GeneticTetris.c', 'tetromino.c', 'board.c', 'utils.c'],
      extra_compile_args=['-fopenmp', '-O3'],
      extra_link_args=['-fopenmp', '-O3'],
)

setup(name='aitetris',
      version='1.0',
      description='Tetris game simulator',
      author='Frederico Sampaio',
      author_email='fredmbs@gmail.com',
      ext_modules = [aitetris_mod],
)
