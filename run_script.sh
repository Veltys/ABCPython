#!/bin/bash

if [ $# -lt 2 ] || \
   [[ "$1" =~ '^[0-9]+$' ]] || [ "$1" -lt 1 ] || \
   [[ "$2" =~ '^[0-9]+$' ]] || [ "$2" -lt 1 ]
then
	funciones=(1 10 1)
	dimensiones=(10 20 5)
else
	funciones=($1 $2 1)

	if [ $# -lt 4 ] || \
	   [[ "$3" =~ '^[0-9]+$' ]] || [ "$3" -lt 5 ] || \
	   [[ "$4" =~ '^[0-9]+$' ]] || [ "$4" -lt 5 ]
	then
		dimensiones=(10 20 5)
	else
		dimensiones=($3 $4 5)
	fi
fi

for (( i=funciones[0]; i<=funciones[1]; i++ )); do
	for (( j=dimensiones[0]; j<=dimensiones[1]; j=j+5 )); do
		echo "Función $i, dimensión $j"

		./ABCAlgorithm.py -d "$j" -o "external_benchmark_$i"
	done
done
