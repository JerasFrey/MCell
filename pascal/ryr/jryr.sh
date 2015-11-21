#!/bin/bash

#PBS -p -1
#PBS -J 1-1000:1
ulimit -l unlimited

/apps/bin/mcell /home/subhadra/pascal/model/ryr/RP20V160Dr${I}.mdl -seed ${PBS_ARRAY_INDEX}
