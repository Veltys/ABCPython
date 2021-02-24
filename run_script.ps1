#!/usr/bin/env pwsh

for($i = 1; $i -le 10; $i++) {
	Write-Output $i > func_num.txt

	for($j = 10; $j -le 20; $j += 5) {
		Write-Output "Ejecución $i, dimensión $j"

		.\ABCAlgorithm.py -d $j
	}
}

Remove-Item func_num.txt
