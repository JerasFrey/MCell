#!/bin/bash

#PBS -p 1023
ulimit -l unlimited

python /home/subhadra/pascal/model/nishants_scripts/dataProcessParallel.py $v
