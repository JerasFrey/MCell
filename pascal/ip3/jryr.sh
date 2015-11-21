#!/bin/bash

#PBS -p -300
#PBS -J 1-1000:1
ulimit -l unlimited

/apps/bin/mcell /home/subhadra/pascal/model/ip3/IST10HzDi${I}.mdl -seed ${PBS_ARRAY_INDEX}
