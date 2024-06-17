#!/bin/sh
#

source ~/.bash_profile
conda_andes
conda activate /gpfs/alpine2/cli187/world-shared/lcheung/condaenv/andesconda1
times=`seq 20500 21000`
EXE=~/cfd162/lcheung/amrwind-frontend/utilities/convertSampleNC2VTK.py

#OUTDIR=turbhh
#NCFILE=~/frontier.proj-shared/lcheung/AWAKEN/Neutral/5kmX5km_turbine1.gooddensity/post_processing/turbhh_41000.nc
#mkdir $OUTDIR
#$EXE $NCFILE -v -g T0_turbhh -k 0 -t $times --jordering -o $OUTDIR/"turbhh_{time}.vtk"

# OUTDIR=turbsw
# NCFILE=~/frontier.proj-shared/lcheung/AWAKEN/Neutral/5kmX5km_turbine1.gooddensity/post_processing/turbsw_41000.nc
# mkdir $OUTDIR
# $EXE $NCFILE -v -g T0_sw -k 0 -t $times --jordering -o $OUTDIR/"turbsw_{time}.vtk"

kvec=`seq 0 10`
for kplane in $kvec; do
    #kplane=10
    OUTDIR=turbrp/plane_${kplane}
    NCFILE=~/frontier.proj-shared/lcheung/AWAKEN/Neutral/5kmX5km_turbine1.gooddensity/post_processing/rotor_41000.nc
    mkdir -p $OUTDIR
    $EXE $NCFILE -v -g T0_rotor -k $kplane -t $times --jordering -o $OUTDIR/"turbrp_{time}.vtk"
done
