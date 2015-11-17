#!/bin/bash

#PBS -p 1023
#PBS -J 1-500:1
ulimit -l unlimited 

/apps/bin/mcell /home/nishant/irs/IRS_15_20hz_${I}.mdl -seed ${PBS_ARRAY_INDEX}
