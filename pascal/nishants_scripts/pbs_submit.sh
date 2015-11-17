#!/bin/bash

a=($(ls /storage/subhadra/pascal/output/IP3_100/))
for item in ${a[*]}
do 
	echo $item
	qsub -v v=$item pbs_analysis.sh
done
