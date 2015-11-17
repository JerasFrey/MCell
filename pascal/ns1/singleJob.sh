#!/bin/bash

#PBS -p 10
ulimit -l unlimited 

/apps/bin/mcell /home/nishant/ns/R_NST300msF100.mdl
