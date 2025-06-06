#!/bin/sh

RUNDIR=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/
SUFFIX=_OpenFAST3p3_NREL2p8-127.bugfix

# Note you can which column has which var using this command:
#   head -n 7 2019-WTW-4641-KP_OpenFAST3p3_NREL2p8-127.bugfix/NREL-2p8-127.T85.out |tail -n1 |fmt -1

alldirs=`ls -1d ${RUNDIR}/*${SUFFIX}`
for d in $alldirs; do
    outfile=`ls -1 $d/*.out |tail -n1`
    newoutfile=`basename $outfile`
    ofdir=`basename $d`
    # Create the corresponding directory
    echo $ofdir/$newoutfile
    mkdir $ofdir
    # Extract the power
    awk '{print $1,$1359}' $outfile > $ofdir/$newoutfile
done
