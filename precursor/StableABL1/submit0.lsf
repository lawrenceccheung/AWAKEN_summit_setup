#!/bin/bash
# Begin LSF Directives
#BSUB -P CFD162
#BSUB -W 24:00
# #BSUB -w ended(2643916)
#BSUB -nnodes 1000
#BSUB -alloc_flags gpumps
# #BSUB -q debug
#BSUB -alloc_flags "gpudefault"
#BSUB -J turbs
#BSUB -o testlidar.%J
#BSUB -e testlidar.%J
#BSUB -u lcheung@sandia.gov
#BSUB -N
#BSUB -B

# Load the amr-wind modules
source /gpfs/alpine/cfd162/proj-shared/lcheung/spackbuilds/spack-manager.5/loadexawindrestart.sh

# # Get the latest restart dir
# unlink chkrestart
# chklast=`ls -1drt chk[0-9]*/ |tail -n1`
# ln -s $chklast chkrestart

CONFFILE=StableABL_precursor1.inp
jsrun -n 6000 -r6 -a 1 -g 1 -c 1 amr_wind $CONFFILE

