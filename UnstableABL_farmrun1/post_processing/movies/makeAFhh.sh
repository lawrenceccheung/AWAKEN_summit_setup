#!/bin/sh
#

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

OUTDIR=farmAF
NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing/AF_z080hh_64500.nc
OUTPNG=$OUTDIR/AFhh_{itime}.png
OUTMP4=AFhh.mp4
mkdir $OUTDIR
itimes=`seq 450 50 899`
dt=5
for i in $itimes; do
    istart=$i
    iend=$((istart+49))
    python makemovie.py $NCFILE `seq $istart $dt $iend` "$OUTPNG" --paramdict "{'title':'Armadillo Flats horiz. velocity'}" -v
done

cd $OUTDIR
module load ffmpeg
ffmpeg -framerate 5 -pattern_type glob -i '*.png' -y $OUTMP4
