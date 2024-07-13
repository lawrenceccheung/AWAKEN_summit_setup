# Set some definitions
EXE    = scene5.py
RENDER = ../renderwindfarm.py
NTURBS = 88
RPM    = 6.0
FPS    = 30

JSONDIR = jsondir
PNGDIR  = pngdir
JSONDIR2= jsondirwire
PNGDIR2 = pngdirwire
LOGDIR  = logdir
MP4DIR  = mp4dir
OUTNAME = testrender

NTHREADS= 1

all: json

json:
	if [ ! -d $(JSONDIR) ]; then \
		mkdir $(JSONDIR);\
	fi
	python $(EXE) -n $(NTURBS) --fps $(FPS) --rpm $(RPM) --pngdir $(PNGDIR) --jsondir $(JSONDIR)
	if [ ! -d $(JSONDIR2) ]; then \
		mkdir $(JSONDIR2);\
	fi
	python $(EXE) -n $(NTURBS) --fps $(FPS) --rpm $(RPM) --pngdir $(PNGDIR2) --jsondir $(JSONDIR2) --SurfRep Wireframe


pngdir:
	if [ ! -d $(PNGDIR) ]; then \
		mkdir $(PNGDIR);\
	fi
	if [ ! -d $(PNGDIR2) ]; then \
		mkdir $(PNGDIR2);\
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
	rm -rf $(JSONDIR) $(PNGDIR) $(JSONDIR2) $(PNGDIR2)
