#!/usr/bin/env pwsh

# Preprocesamiento: variables
if(
	($args[0] -eq "" -or !($args[0] -match '^\d+$') -or $args[0] -lt 1) -or
	($args[1] -eq "" -or !($args[1] -match '^\d+$') -or $args[1] -lt 1)
) {
	$funciones		= @( 1, 10, 1)
	$dimensiones	= @(10, 20, 5)
}
else {
	$funciones		= @($args[0], $args[1], 1)

	if(
		($args[2] -eq "" -or !($args[1] -match '^\d+$') -or $args[2] -lt 5) -or
		($args[3] -eq "" -or !($args[3] -match '^\d+$') -or $args[3] -lt 5)
	) {
		$dimensiones	= @(10, 20, 5)
	}
	else {
		$dimensiones	= @($args[2], $args[3], 5)
	}
}

# Procesamiento: ejecución del programa

for($i = $funciones[0]; $i -le $funciones[1]; $i += $funciones[2]) {
	for($j = $dimensiones[0]; $j -le $dimensiones[1]; $j += $dimensiones[2]) {
		Write-Output "Función $i, dimensión $j"

		.\ABCAlgorithm.py -d $j -o external_benchmark_$i
	}
}


# Posprocesamiento: recopilación de resultados
# Recogida de todos los archivos de salida
$archivos = Get-ChildItem -Path .\Outputs\ResultByCycle -Filter *.txt

# Iteración de todas las dimensiones
for($i = $dimensiones[0]; $i -le $dimensiones[1]; $i += $dimensiones[2]) {
	# Preparación de la matriz de resultados
	[System.Collections.ArrayList]$res = @()

	for($j = 0; $j -le 15; $j++) {
		$null = $res.Add(@(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))
	}

	# Desplazamiento dimensional
	$offset = ($i - $dimensiones[0]) / $dimensiones[2]


	for($j = 0; $j -le 29; $j++) {
		for($k = 0; $k -le 15; $k++) {
			# Número de línea a leer
			$numLinea = [Math]::Round([Math]::Pow($i, $k / 5 - 3) * 150000)

			# Coordenada de insercción en la matriz de resultados calculada debido al previsible mal ordenamiento de los archivos
            $l = $archivos[$j].Name.Split('.')[0].Split('-')[-1]

            $linea = Get-Content $archivos[$offset + $j].FullName | Select -Index ($numLinea - 1)

			# Algunas líneas podrían no existir, debido a los criterios de parada
            if($linea -match '^[-]?[0-9.]+$') {
				$res[$k][$l] = $linea
			}
			else {
				# En tal caso, se copia el resultado de la línea anterior
				$res[$k][$l] = $res[$k - 1][$l]
			}
		}
	}

	$out = '';

	for($j = 0; $j -le 15; $j++) {
		for($k = 0; $k -le 29; $k++) {
			$out += $res[$j][$k]

			 if($k -ne 29) {
			 	$out += ';'
		 	}
		}

		$out += [Environment]::NewLine
	}

	$out | Out-File "t1_d$i.csv"
}
