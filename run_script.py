#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    @file:           run_script.py
    @brief:          Runner for this algorithm

    @author:         Rafael Carlos Méndez Rodríguez (i82meror)
    @date:           2021-06-25
    @version:        1.1.3
    @usage:          python3 run_script.py
    @note:           Use flag -h to see optional commands and help
'''


import argparse
import errno
import linecache
import os
from shutil import rmtree
import sys

import numpy

import ABCAlgorithm


def parseClArgs(argv):
    '''! Procesa los argumentos pasados al programa
    
        @param argv:    Vector de argumentos
    
        @return:        Argumentos procesados
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-fMin', type = int, default = 1, dest = 'fMin', choices = range(1, 11), help = 'minimum function id for benchmark 2020 (default: 1)')
    parser.add_argument('-fMax', type = int, default = 10, dest = 'fMax', choices = range(1, 11), help = 'maximum function id for benchmark 2020; have to be greater or equal to fMin (default: 10)')
    parser.add_argument('-fStep', type = int, default = 1, dest = 'fStep', choices = range(1, 11), help = 'function id step for benchmark 2020 (default: 1)')
    parser.add_argument('-dMin', type = int, default = 10, dest = 'dMin', choices = range(10, 21, 5), help = 'minimum dimension (default: 10)')
    parser.add_argument('-dMax', type = int, default = 20, dest = 'dMax', choices = range(10, 21, 5), help = 'maximum dimension; have to be greater or equal to dMin (default: 20)')
    parser.add_argument('-dStep', type = int, default = 5, dest = 'dStep', choices = range(5, 11, 5), help = 'dimension step (default: 5)')

    if (sys.version_info[0] > 3) or (sys.version_info[0] == 3 and sys.version_info[1] >= 8): # argparse.BooleanOptionalAction was introduced on Python 3.8, but Raspberry Pi OS Python is stuck on 3.7 and that's makes things a bit harder
        parser.add_argument('-e', '--execute', default = True, dest = 'execute', action = argparse.BooleanOptionalAction, help = 'make execution phase')
        parser.add_argument('-p', '--postprocessing', default = True, dest = 'postprocessing', action = argparse.BooleanOptionalAction, help = 'make postprocessing phase')
    else:
        parser.add_argument('-e', '--execute', type = bool, default = True, dest = 'execute', help = 'make execution phase (default: True)')
        parser.add_argument('-p', '--postprocessing', type = bool, default = True, dest = 'postprocessing', help = 'make postprocessing phase (default True)')


    args = parser.parse_args(argv)

    return args


def guardar(alg, funcion, dimensiones, res):
    '''! Guarda los datos ya procesados en el archivo correspondiente en formato CSV
    
        @param alg:            Nombre del algoritmo procesado
        @param funcion:        Número de función procesada
        @param dimensiones:    Número de dimensiones procesadas
        @param res:            Resultados procesados
    '''

    fileName = f'{alg}_{funcion}_{dimensiones}.txt'

    try:
        out = open(fileName, 'w')

    except IOError:
        print(f"Error de apertura del archivo <{fileName}>")
        print(f"ERROR: imposible abrir el archivo <{fileName}>", file = sys.stderr)

        sys.exit(errno.ENOENT)

    else:
        for i in range(16):
            for j in range(30):
                out.write(str(res[i][j]).replace('.',','))

                if j != 29:
                    out.write(';')

            # out.write(os.linesep)
            out.write("\n")

        out.close()


def posprocesar(dimensiones):
    '''! Lee los resultados en el formato que la metaheurística los arroja y los almacena en memoria
    
        @param dimensiones:    Número de dimensiones procesadas

        @return:               Resultados procesados
    '''

    # Recogida de todos los archivos de salida
    archivos = [ name for name in os.listdir(f".{os.sep}Outputs{os.sep}ResultByCycle") ]

    # Preparación de la matriz de resultados
    res = numpy.zeros((16, 30))

    for i in range(30):
        # Coordenada de inserción en la matriz de resultados calculada debido al previsible mal ordenamiento de los archivos
        k = int(archivos[i].split('.')[0].split('-')[-1])

        for j in range(16):
            # Número de línea a leer
            numLinea = int(round((dimensiones ** (j / 5 - 3)) * 150000, 0))

            try: # Algunas líneas podrían no existir, debido a los criterios de parada
                elemento = linecache.getline(f".{os.sep}Outputs{os.sep}ResultByCycle{os.sep}{archivos[i]}", numLinea)

                res[j][k] = elemento

            except IndexError: # En tal caso, se copia el resultado de la línea anterior
                res[j][k] = res[j - 1][k]

            except ValueError:
                res[j][k] = res[j - 1][k]

            else:
                pass


    rmtree(f'.{os.sep}Outputs')

    return res


def main(argv):
    '''! Ejecuta la metaheurística, procesa sus resultados y genera el archivo con la tabla de resultados final
    
        @param argv:    Argumentos del programa

        @return:        Código de retorno
    '''

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
