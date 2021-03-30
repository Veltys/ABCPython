#!/bin/bash

# Preprocesamiento: variables
alg='ABC'

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

for (( i=funciones[0]; i<=funciones[1]; i++ )); do
	for (( j=dimensiones[0]; j<=dimensiones[1]; j=j+5 )); do
		# Procesamiento condicional a la no existencia del parámetro -r
		if \
			! ( \
				[ "$1" = '-r' ] || \
				( [ $# -eq 5 ] && [ "$5" = '-r' ] )
			)
		then
			# Procesamiento: ejecución del programa
			echo "Función $i, dimensión $j"

			./ABCAlgorithm.py -d "$j" -o "external_benchmark_$i"
		fi

		# Posprocesamiento: recopilación de resultados
		# Recogida de todos los archivos de salida
		archivos=($(ls ./Outputs/ResultByCycle/ | grep txt))

		# Preparación de la matriz de resultados
		declare -A res

		for (( k=0; k<30; k++ )); do
			# Coordenada de insercción en la matriz de resultados calculada debido al previsible mal ordenamiento de los archivos
			m=${archivos[$k]}

			m=(${m//./ })

			m=(${m[0]//-/ })

			m=${m[-1]}

			for (( l=0; l<16; l++ )); do
				# Número de línea a leer
				numLinea=$(awk "BEGIN {print int($j ^ ($l / 5 - 3) * 150000)}")

				linea=$(sed -n "$((numLinea - 1)) p" "./Outputs/ResultByCycle/${archivos[$k]}")

				# Algunas líneas podrían no existir, debido a los criterios de parada
				if ! [[ -z "$linea" ]]; then
					res[$l,$m]=$linea
				else
					# En tal caso, se copia el resultado de la línea anterior
					res[$l,$m]=${res[$((l - 1)),$m]}
				fi

				# Limpieza de caracteres no imprimibles no deseados que aparecen "because yes"
				res[$l,$m]=$(tr -dc '[[:print:]]' <<< "${res[$l,$m]}")
			done
		done

		if [ -f "${alg}_${i}_${j}.txt" ]; then
			truncate -s0 "${alg}_${i}_${j}.txt"
		fi

		for (( k=0; k<16; k++ )); do
			for (( l=0; l<30; l++ )); do
				echo -n "${res[$k,$l]}" >> "${alg}_${i}_${j}.txt"

				if [ "$l" -ne 29 ]; then
					echo -n ',' >> "${alg}_${i}_${j}.txt"
				fi
			done

			echo >> "${alg}_${i}_${j}.txt"

			# Borrado de resultados ya no necesarios
			rm -r ./Outputs
		done
	done
done
