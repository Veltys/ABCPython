#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import linecache
import os
import re
from shutil import rmtree
import sys

import numpy

import ABCAlgorithm


def guardar(alg, funcion, dimensiones, res):
    try:
        out = open(alg + '_' + str(funcion) + '_' + str(dimensiones) + '.txt', 'w')

    except IOError:
        print('Error de apertura del archivo <' + alg + '_' + str(funcion) + '_' + str(dimensiones) + '.txt>')
        print('ERROR: imposible abrir el archivo <' + alg + '_' + str(funcion) + '_' + str(dimensiones) + '.txt>', file = sys.stderr)

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


def preprocesar(argv):
    if \
        len(argv) < 2 or \
        (not(re.match(r"[0-9]+", argv[0])) or int(argv[0]) < 1) or \
        (not(re.match(r"[0-9]+", argv[1])) or int(argv[1]) < 1):
        funciones = [ 1, 10, 1]
        dimensiones = [10, 20, 5]
    else:
        funciones = [int(argv[0]), int(argv[1]), 1]

        if \
            len(argv) < 4 or \
            (not(re.match(r"[0-9]+", argv[2])) or int(argv[2]) < 5) or \
            (not(re.match(r"[0-9]+", argv[3])) or int(argv[3]) < 5):
            dimensiones = [10, 20, 5]
        else:
            dimensiones = [int(argv[2]), int(argv[3]), 5]

    return (funciones, dimensiones)


def posprocesar(dimensiones):
    # Recogida de todos los archivos de salida
    archivos = [ name for name in os.listdir('.' + os.sep + 'Outputs' + os.sep + 'ResultByCycle') ]

    # Preparación de la matriz de resultados
    res = numpy.zeros((16, 30))

    for i in range(30):
        # Coordenada de insercción en la matriz de resultados calculada debido al previsible mal ordenamiento de los archivos
        k = int(archivos[i].split('.')[0].split('-')[-1])

        for j in range(16):
            # Número de línea a leer
            numLinea = int(round((dimensiones ** (j / 5 - 3)) * 150000, 0))

            elemento = linecache.getline('.' + os.sep + 'Outputs' + os.sep + 'ResultByCycle' + os.sep + archivos[i], numLinea)

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

    (funciones, dimensiones) = preprocesar(argv)

    for i in range(funciones[0] - funciones[2], funciones[1], funciones[2]):
        for j in range(dimensiones[0] - dimensiones[2], dimensiones[1], dimensiones[2]):
            # Procesamiento condicional a la no existencia del parámetro -r

            if \
                not(\
                    (len(argv) == 1 and argv[0] == '-r') or \
                    (len(argv) == 5 and argv[4] == '-r') \
                ):
                # Procesamiento: ejecución del programa
                print('Función ' + str(i + funciones[2]) + ' dimensión ' + str(j + dimensiones[2]))

                ABCAlgorithm.main(['-d', str(j + dimensiones[2]), '-o', 'external_benchmark_' + str(i + funciones[2])])

            # Posprocesamiento: recopilación de resultados
            guardar(alg, i + funciones[2], j + dimensiones[2], posprocesar(j + dimensiones[2]))

if __name__ == '__main__':
    main(sys.argv[1:])
