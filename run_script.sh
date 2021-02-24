#!/bin/bash

for (( i=1; i<=10; i++ )); do
	echo $i > func_num.txt

	for j in {10..20..5}; do
		echo "Ejecución $i, dimensión $j"

		./ABCAlgorithm.py -d $j
	done
done

rm func_num.txt
