# Set some definitions
EXE    = testrender.py
RENDER = ../renderwindfarm.py
NTURBS = -1
RPM    = 6.0
FPS    = 30

JSONDIR = jsondir
PNGDIR  = pngdir
LOGDIR  = logdir

all: json png

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
	pvbatch $(RENDER) -v $@

FORCE:

clean:
	rm -rf $(JSONDIR) $(PNGDIR)
