#!/bin/bash

#PBS -p -1
#PBS -J 1-10000:1
#PBS -o /home/nishant/errout/^array_index^.o
#PBS -e /home/nishant/errout/^array_index^.e 
ulimit -l unlimited 

/apps/bin/mcell /home/nishant/ns/R_RSI${I}.mdl -seed ${PBS_ARRAY_INDEX}
