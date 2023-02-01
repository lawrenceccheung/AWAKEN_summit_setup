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

OUTDIR=farmKP
NCFILE=/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing/KP_z090hh_64500.nc
OUTPNG=$OUTDIR/KPhh_{itime}.png
OUTMP4=KPhh.mp4
mkdir $OUTDIR
#python makemovie.py $NCFILE `seq 300 5 345` "$OUTPNG" --paramdict "{'title':'King Plains horiz. velocity'}" -v
#python makemovie.py $NCFILE `seq 350 5 395` "$OUTPNG" --paramdict "{'title':'King Plains horiz. velocity'}" -v
#python makemovie.py $NCFILE `seq 400 5 445` "$OUTPNG" --paramdict "{'title':'King Plains horiz. velocity'}" -v
#python makemovie.py $NCFILE `seq 450 5 495` "$OUTPNG" --paramdict "{'title':'King Plains horiz. velocity'}" -v
python makemovie.py $NCFILE `seq 500 5 545` "$OUTPNG" --paramdict "{'title':'King Plains horiz. velocity'}" -v
python makemovie.py $NCFILE `seq 550 5 595` "$OUTPNG" --paramdict "{'title':'King Plains horiz. velocity'}" -v
python makemovie.py $NCFILE `seq 600 5 645` "$OUTPNG" --paramdict "{'title':'King Plains horiz. velocity'}" -v
python makemovie.py $NCFILE `seq 650 5 695` "$OUTPNG" --paramdict "{'title':'King Plains horiz. velocity'}" -v
python makemovie.py $NCFILE `seq 700 5 745` "$OUTPNG" --paramdict "{'title':'King Plains horiz. velocity'}" -v
python makemovie.py $NCFILE `seq 750 5 795` "$OUTPNG" --paramdict "{'title':'King Plains horiz. velocity'}" -v
python makemovie.py $NCFILE `seq 800 5 845` "$OUTPNG" --paramdict "{'title':'King Plains horiz. velocity'}" -v
python makemovie.py $NCFILE `seq 850 5 895` "$OUTPNG" --paramdict "{'title':'King Plains horiz. velocity'}" -v

cd $OUTDIR
module load ffmpeg
ffmpeg -framerate 5 -pattern_type glob -i '*.png' -y $OUTMP4
