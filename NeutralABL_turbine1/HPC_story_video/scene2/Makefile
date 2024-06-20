# Set some definitions
EXE    = scene2.py
RENDER = ../renderwindfarm.py
NTURBS = 1 #1000
RPM    = 6.0
FPS    = 30

JSONDIR = jsondir
PNGDIR  = pngdir
LOGDIR  = logdir
MP4DIR  = mp4dir
OUTNAME = scene2

NTHREADS= 1

all: json

json:
	if [ ! -d $(JSONDIR) ]; then \
		mkdir $(JSONDIR);\
	fi
	python $(EXE) -n $(NTURBS) --fps $(FPS) --rpm $(RPM) --pngdir $(PNGDIR) --jsondir $(JSONDIR)


pngdir:
	if [ ! -d $(PNGDIR) ]; then \
		mkdir $(PNGDIR);\
	fi

%.json: FORCE pngdir
	export KNOB_MAX_WORKER_THREADS=$(NTHREADS)
	export OSPRAY_NUM_THREADS=$(NTHREADS)
	pvbatch $(RENDER) -v $@

mp4:
	if [ ! -d $(MP4DIR) ]; then \
		mkdir $(MP4DIR);\
	fi
	ffmpeg -framerate $(FPS) -pattern_type glob -i '$(PNGDIR)/*.png' -c:v libx264 -pix_fmt yuv420p $(MP4DIR)/$(OUTNAME).mp4


FORCE:

clean:
	rm -rf $(JSONDIR) $(PNGDIR)
