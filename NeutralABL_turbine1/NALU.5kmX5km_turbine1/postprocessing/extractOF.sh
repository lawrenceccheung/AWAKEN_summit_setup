#!/bin/sh

OUTFILE=/pscratch/mlblayl/AWAKEN/Neutral_Turbine_Yaw/OpenFAST_000/NREL-2p8-127.T1.out

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


grepOFcols $OUTFILE Time GenPwr > $DATADIR/NALUWIND_turb_GenPwr.dat
grepOFcols $OUTFILE Time RotTorq > $DATADIR/NALUWIND_turb_RotTorq.dat
grepOFcols $OUTFILE Time RotThrust > $DATADIR/NALUWIND_turb_RotThrust.dat
grepOFcols $OUTFILE Time RotSpeed > $DATADIR/NALUWIND_turb_RotSpeed.dat
grepOFcols $OUTFILE Time Wind1VelX > $DATADIR/NALUWIND_turb_Wind1VelX.dat
