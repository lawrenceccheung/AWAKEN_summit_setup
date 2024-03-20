#!/bin/sh

OUTFILE=/gpfs/drhouck/AWAKEN/JRSE_Precursor/newmesh/z0_0p03_newWD_turbine/T0_OpenFAST3p3_NREL2p8-127.bugfix/NREL-2p8-127.out

DATADIR=data/

grepOFcols() {
    OFfile=$1
    col1=$2
    col2=$3
    headers=`head -n7 $OFfile |tail -n1 |fmt -1 |nl`
    col1num=`echo "$headers" |grep "$col1" |awk '{print $1}'`
    col2num=`echo "$headers" |grep "$col2" |awk '{print $1}'`

    tail -n +7 $OFfile | awk -v col1num=$col1num -v col2num=$col2num '{print $col1num, $col2num}'
}


grepOFcols $OUTFILE Time GenPwr > $DATADIR/AMRWIND_turb_GenPwr.dat
grepOFcols $OUTFILE Time RotTorq > $DATADIR/AMRWIND_turb_RotTorq.dat
grepOFcols $OUTFILE Time RotThrust > $DATADIR/AMRWIND_turb_RotThrust.dat
grepOFcols $OUTFILE Time RotSpeed > $DATADIR/AMRWIND_turb_RotSpeed.dat
grepOFcols $OUTFILE Time Wind1VelX > $DATADIR/AMRWIND_turb_Wind1VelX.dat
