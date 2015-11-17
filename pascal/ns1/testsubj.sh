#!/bin/bash

ISI=("20" "40")

for i in "${ISI[@]}"
do
	qsub -N NSI${i}V40 -v I=$i jryr.sh
done
