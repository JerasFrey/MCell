#!/bin/bash

#PBS -p -1
#PBS -J 1-800:1
ulimit -l unlimited

/apps/bin/mcell /home/subhadra/pascal/model/ryr/RP20V90Dr${I}.mdl -seed ${PBS_ARRAY_INDEX}
