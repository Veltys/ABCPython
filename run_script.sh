#!/bin/bash

# Preprocesamiento: variables
if [ $# -lt 2 ] || \
   [[ ! $1 == ?(-)+([0-9]) ]] || [ "$1" -lt 1 ] || \
   [[ ! $2 == ?(-)+([0-9]) ]] || [ "$2" -lt 1 ]
then
	funciones=(1 10 1)
	dimensiones=(10 20 5)
else
	funciones=($1 $2 1)

	if [ $# -lt 4 ] || \
	   [[ ! $3 == ?(-)+([0-9]) ]] || [ "$3" -lt 5 ] || \
	   [[ ! $4 == ?(-)+([0-9]) ]] || [ "$4" -lt 5 ]
	then
		dimensiones=(10 20 5)
	else
		dimensiones=($3 $4 5)
	fi
fi

# Procesamiento condicional a la no existencia del parámetro -r
if \
	! ( \
		[ "$1" = '-r' ] || \
		( [ $# -eq 5 ] && [ "$5" = '-r' ] )
	)
then
# Procesamiento: ejecución del programa
	for (( i=funciones[0]; i<=funciones[1]; i++ )); do
		for (( j=dimensiones[0]; j<=dimensiones[1]; j=j+5 )); do
			echo "Función $i, dimensión $j"

			./ABCAlgorithm.py -d "$j" -o "external_benchmark_$i"
		done
	done
fi

# Posprocesamiento: recopilación de resultados
# Recogida de todos los archivos de salida
archivos=($(ls ./Outputs/ResultByCycle/ | grep txt))

# Iteración de todas las dimensiones
for (( i=dimensiones[0]; i<=dimensiones[1]; i+=dimensiones[2] )); do
	# Preparación de la matriz de resultados
	declare -A res

	# Desplazamiento dimensional
	offset=$(((i - dimensiones[0]) / dimensiones[2]))

	for (( j=0; j<30; j++ )); do
		# Coordenada de insercción en la matriz de resultados calculada debido al previsible mal ordenamiento de los archivos
		l=${archivos[$j]}

		l=(${l//./ })

		l=(${l[0]//-/ })

		l=${l[-1]}

		for (( k=0; k<16; k++ )); do
			# Número de línea a leer
			numLinea=$(awk "BEGIN {print int($i ^ ($k / 5 - 3) * 150000)}")

			linea=$(sed "$((numLinea - 1))q;d" ./Outputs/ResultByCycle/"${archivos[$((offset + j))]}")

			# Algunas líneas podrían no existir, debido a los criterios de parada
			if ! [[ -z "$linea" ]]; then
				res[$k,$l]=$linea
			else
				# En tal caso, se copia el resultado de la línea anterior
				res[$k,$l]=${res[$((k - 1)),$l]}
			fi

			# Limpieza de caracteres no imprimibles no deseados que aparecen "because yes"
			res[$k,$l]=$(tr -dc '[[:print:]]' <<< "${res[$k,$l]}")
		done
	done

	if [ -f "t1_d$i.csv" ]; then
		truncate -s0 "t1_d$i.csv"
	fi

	for (( j=0; j<16; j++ )); do
		for (( k=0; k<30; k++ )); do
			echo -n "${res[$j,$k]}" >> "t1_d$i.csv"

			if [ "$k" -ne 29 ]; then
				echo -n ',' >> "t1_d$i.csv"
			fi
		done

		echo >> "t1_d$i.csv"
	done
done
