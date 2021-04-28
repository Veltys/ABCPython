#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : run_script.py
# Description   : Runner for this algorithm
# Author        : Veltys
# Date          : 2021-04-28
# Version       : 1.0.0
# Usage         : python3 run_script.py
# Notes         : Use flag -h to see optional commands and help


import argparse
import linecache
import os
from shutil import rmtree
import sys

import numpy

import ABCAlgorithm


def parseClArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-fMin', type = int, default = 1, dest = 'fMin', choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], help = 'minimum function id for benchmark 2020, default: 1')
    parser.add_argument('-fMax', type = int, default = 10, dest = 'fMax', choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], help = 'maximum function id for benchmark 2020, default: 10; note: it has to be greater or equal to fMin')
    parser.add_argument('-fStep', type = int, default = 1, dest = 'fStep', choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], help = 'function id step for benchmark 2020, default: 1')
    parser.add_argument('-dMin', type = int, default = 10, dest = 'dMin', choices = [10, 15, 20], help = 'minimum dimension, default: 10')
    parser.add_argument('-dMax', type = int, default = 20, dest = 'dMax', choices = [10, 15, 20], help = 'maximum dimension, default: 20; note: it has to be greater or equal to dMin')
    parser.add_argument('-dStep', type = int, default = 5, dest = 'dStep', choices = [10, 15, 20], help = 'dimension step, default: 5')
    parser.add_argument('-e', '--execute', type = bool, default = True, dest = 'execute', help = 'make execution phase; default True')
    parser.add_argument('-p', '--postprocessing', type = bool, default = True, dest = 'postprocessing', help = 'make postprocessing phase; default True')

    args = parser.parse_args(argv)

    return args


def guardar(alg, funcion, dimensiones, res):
    fileName = f'{alg}_{funcion}_{dimensiones}.txt'

    try:
        out = open(fileName, 'w')

    except IOError:
        print(f"Error de apertura del archivo <{fileName}>")
        print(f"ERROR: imposible abrir el archivo <{fileName}>", file = sys.stderr)

        exit(os.EX_OSFILE) # @UndefinedVariable

    else:
        for i in range(16):
            for j in range(30):
                out.write(str(res[i][j]))

                if j != 29:
                    out.write(',')

            # out.write(os.linesep)
            out.write("\n")

        out.close()


def posprocesar(dimensiones):
    # Recogida de todos los archivos de salida
    archivos = [ name for name in os.listdir(f".{os.sep}Outputs{os.sep}ResultByCycle") ]

    # Preparación de la matriz de resultados
    res = numpy.zeros((16, 30))

    for i in range(30):
        # Coordenada de insercción en la matriz de resultados calculada debido al previsible mal ordenamiento de los archivos
        k = int(archivos[i].split('.')[0].split('-')[-1])

        for j in range(16):
            # Número de línea a leer
            numLinea = int(round((dimensiones ** (j / 5 - 3)) * 150000, 0))

            elemento = linecache.getline(f".{os.sep}Outputs{os.sep}ResultByCycle{os.sep}{archivos[i]}", numLinea)

            # Algunas líneas podrían no existir, debido a los criterios de parada
            if elemento != '':
                res[j][k] = float(elemento)
            else:
                # En tal caso, se copia el resultado de la línea anterior
                res[j][k] = res[j - 1][k]

    rmtree('.' + os.sep + 'Outputs')

    return res


def main(argv):
    # Preprocesamiento: variables

    alg = 'ABC'

    args = parseClArgs(argv)

    for i in range(args.fMin - args.fStep, args.fMax, args.fStep):
        for j in range(args.dMin - args.dStep, args.dMax, args.dStep):
            if(args.execute):
                # Procesamiento: ejecución del programa
                print(f'Función {i + args.fStep}, dimensión {j + args.dStep}')

                ABCAlgorithm.main(['-d', str(j + args.dStep), '-o', 'external_benchmark_' + str(i + args.fStep)])

            if(args.postprocessing):
                # Posprocesamiento: recopilación de resultados
                guardar(alg, i + args.fStep, j + args.dStep, posprocesar(j + args.dStep))


if __name__ == '__main__':
    main(sys.argv[1:])
