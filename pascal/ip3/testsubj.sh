#!/bin/bash

for i in {-400..-75..25}

do
	echo IS100Di$i.mdl
#	qsub -N IS100Di$i -v I=$i jryr.sh
done
