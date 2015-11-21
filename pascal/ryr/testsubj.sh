#!/bin/bash

for a in {-50..750..50}

do
	echo RP20V160Dr$a.mdl
#	qsub -N RP20V160Dr$a -v I=$a jryr.sh
done
