#!/usr/bin/env pwsh

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

for($i = $funciones[0]; $i -le $funciones[1]; $i += $funciones[2]) {
	for($j = $dimensiones[0]; $j -le $dimensiones[1]; $j += $dimensiones[2]) {
		Write-Output "Función $i, dimensión $j"

		.\ABCAlgorithm.py -d $j -o external_benchmark_$i
	}
}
