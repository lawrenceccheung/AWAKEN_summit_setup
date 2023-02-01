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

OUTDIR=farmhh
NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing/farm_z90_64500.nc
OUTPNG=$OUTDIR/farmhh_{itime}.png
OUTMP4=farmhh.mp4
mkdir $OUTDIR
itimes=`seq 300 50 899`
dt=5
for i in $itimes; do
    istart=$i
    iend=$((istart+49))
    python makemovie.py $NCFILE `seq $istart $dt $iend` "$OUTPNG" --paramdict "{'title':'AWAKEN domain horiz. velocity'}" -v
    #python makemovie.py $NCFILE `seq 330 5 400` "$OUTPNG" --paramdict "{'title':'AWAKEN Domain'}" -v
done

cd $OUTDIR
module load ffmpeg
ffmpeg -framerate 5 -pattern_type glob -i '*.png' $OUTMP4
