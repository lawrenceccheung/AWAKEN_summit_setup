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

FARM=CV
# === Do the with turbine case ===
NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing/${FARM}_sideplane1_64500.nc
OUTFILE=${FARM}_sideplane1_mean_wturb.pkl
ISTART=360
DT=60
IEND=1010
VXVAR=velocity_meanx
VYVAR=velocity_meany
VZVAR=velocity_meanz
# Run the script
python assemblepkl.py $NCFILE `seq $ISTART $DT $IEND` $OUTFILE --vxvar $VXVAR --vyvar $VYVAR --vzvar $VZVAR --overwrite --inflow -v

NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing/${FARM}_sideplane2_64500.nc
OUTFILE=${FARM}_sideplane2_mean_wturb.pkl
python assemblepkl.py $NCFILE `seq $ISTART $DT $IEND` $OUTFILE --vxvar $VXVAR --vyvar $VYVAR --vzvar $VZVAR --overwrite --inflow -v

# === Do the no turbine case ===
NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/UnstableABL1_farmrun1_noturbs/post_processing/${FARM}_sideplane1_64500.nc
OUTFILE=${FARM}_sideplane1_mean_noturb.pkl
# Run the script
python assemblepkl.py $NCFILE `seq $ISTART $DT $IEND` $OUTFILE --vxvar $VXVAR --vyvar $VYVAR --vzvar $VZVAR --overwrite --inflow -v

NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/UnstableABL1_farmrun1_noturbs/post_processing/${FARM}_sideplane2_64500.nc
OUTFILE=${FARM}_sideplane2_mean_noturb.pkl
# Run the script
python assemblepkl.py $NCFILE `seq $ISTART $DT $IEND` $OUTFILE --vxvar $VXVAR --vyvar $VYVAR --vzvar $VZVAR --overwrite --inflow -v