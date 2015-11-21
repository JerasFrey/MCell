#!/bin/bash

#PBS -p -1
#PBS -J 1-1000:1
ulimit -l unlimited

/apps/bin/mcell /home/subhadra/pascal/model/ip3/IS100Di${I}.mdl -seed ${PBS_ARRAY_INDEX}
