#!/bin/sh

conda_start() {
    # >>> conda initialize >>>
    # !! Contents within this block are managed by 'conda init' !!
    __conda_setup="$('/sw/summit/python/3.8/anaconda3/2020.07-rhel8/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
    if [ $? -eq 0 ]; then
	eval "$__conda_setup"
    else
	if [ -f "/sw/summit/python/3.8/anaconda3/2020.07-rhel8/etc/profile.d/conda.sh" ]; then
            . "/sw/summit/python/3.8/anaconda3/2020.07-rhel8/etc/profile.d/conda.sh"
	else
            export PATH="/sw/summit/python/3.8/anaconda3/2020.07-rhel8/bin:$PATH"
	fi
    fi
    unset __conda_setup
    # <<< conda initialize <<<

}

conda_start
conda activate ~/cfd162/lcheung/condaenv/python1

NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing/KPturbhh_64500.nc
PYEXE=~/cfd162/lcheung/amrwind-frontend/utilities/convertSampleNC2VTK.py
GROUP=2019-WTW-4713-KP_KPturbhh
OUTDIR=/ccs/home/lcheung/projwork/lcheung/AWAKEN/UnstableABL_farmrun1/post_processing/vtk/farm_KP
OUTFILE="${OUTDIR}/T${GROUP}_{time}.vtk"
TIME=`seq 16425 17280` #`seq 16425 16435`
KPLANE=0
#python $PYEXE -g $GROUP -t $TIME -k $KPLANE --jordering -v $NCFILE -o $OUTFILE


NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing/farm_z90_64500.nc
GROUP=Farm_hh90
OUTDIR=/ccs/home/lcheung/projwork/lcheung/AWAKEN/UnstableABL_farmrun1/post_processing/vtk/farm_z90
OUTFILE="${OUTDIR}/T${GROUP}_{time}.vtk"
python $PYEXE -g $GROUP -t $TIME -k $KPLANE --jordering -v $NCFILE -o $OUTFILE

NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing/KP_z090hh_64500.nc
GROUP=Farm_KP090
OUTDIR=/ccs/home/lcheung/projwork/lcheung/AWAKEN/UnstableABL_farmrun1/post_processing/vtk/farm_KP
OUTFILE="${OUTDIR}/T${GROUP}_{time}.vtk"
python $PYEXE -g $GROUP -t $TIME -k $KPLANE --jordering -v $NCFILE -o $OUTFILE

NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing/KPsw_64500.nc
GROUP=2019-WTW-4713-KP_KPsw
OUTFILE="T${GROUP}_{time}.vtk"
#python $PYEXE -g $GROUP -t $TIME -k $KPLANE --jordering -v $NCFILE -o $OUTFILE

NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing/CV_z080hh_64500.nc
GROUP=Farm_CV080
OUTDIR=/ccs/home/lcheung/projwork/lcheung/AWAKEN/UnstableABL_farmrun1/post_processing/vtk/farm_CV
OUTFILE="${OUTDIR}/T${GROUP}_{time}.vtk"
python $PYEXE -g $GROUP -t $TIME -k $KPLANE --jordering -v $NCFILE -o $OUTFILE

NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing/BR_z080hh_64500.nc
GROUP=Farm_BR080
OUTDIR=/ccs/home/lcheung/projwork/lcheung/AWAKEN/UnstableABL_farmrun1/post_processing/vtk/farm_BR
OUTFILE="${OUTDIR}/T${GROUP}_{time}.vtk"
python $PYEXE -g $GROUP -t $TIME -k $KPLANE --jordering -v $NCFILE -o $OUTFILE

NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing/TR_z090hh_64500.nc
GROUP=Farm_TR090
OUTDIR=/ccs/home/lcheung/projwork/lcheung/AWAKEN/UnstableABL_farmrun1/post_processing/vtk/farm_TR
OUTFILE="${OUTDIR}/T${GROUP}_{time}.vtk"
python $PYEXE -g $GROUP -t $TIME -k $KPLANE --jordering -v $NCFILE -o $OUTFILE

NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing/AF_z080hh_64500.nc
GROUP=Farm_AF080
OUTDIR=/ccs/home/lcheung/projwork/lcheung/AWAKEN/UnstableABL_farmrun1/post_processing/vtk/farm_AF
OUTFILE="${OUTDIR}/T${GROUP}_{time}.vtk"
python $PYEXE -g $GROUP -t $TIME -k $KPLANE --jordering -v $NCFILE -o $OUTFILE

