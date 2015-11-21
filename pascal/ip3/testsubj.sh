#!/bin/bash

for i in {-50..750..50}

do
	echo IST10HzDi$i.mdl
#	qsub -N IST10HzDi$i -v I=$i jryr.sh
done
