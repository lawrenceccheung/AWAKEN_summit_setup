# Set time definitions
TSTART = 16525.00
TEND   = 16625.00
DT     = 1.0

YAMLDIR = yamldir
PNGDIR  = pngdir
LOGDIR  = logdir
MP4DIR  = mp4dir
SCENENAME = scene3A

all: yaml png

yaml:
	if [ ! -d $(YAMLDIR) ]; then \
		mkdir $(YAMLDIR);\
	fi
	for t in `seq -w $(TSTART) $(DT) $(TEND)`; do python writescene1_attime.py $$t; done

#		pvbatch renderwindfarm.py -v $(YAMLDIR)/scene3A_$$t.yaml > $(LOGDIR)/out_$$t.log & 

png:
	if [ ! -d $(PNGDIR) ]; then \
		mkdir $(PNGDIR);\
	fi
	if [ ! -d $(LOGDIR) ]; then \
		mkdir $(LOGDIR);\
	fi
	for t in `seq -w $(TSTART) $(DT) $(TEND)`; do \
		nohup script -c "pvbatch renderwindfarm.py -v $(YAMLDIR)/$(SCENENAME)_$$t.yaml" -f $(LOGDIR)/out_$$t.log > /dev/null ;\
	done

mp4:
	if [ ! -d $(MP4DIR) ]; then \
		mkdir $(MP4DIR);\
	fi
	ffmpeg -framerate 10 -pattern_type glob -i '$(PNGDIR)/*.png' -c:v libx264 -pix_fmt yuv420p $(MP4DIR)/$(SCENENAME).mp4

clean:
	rm -rf $(YAMLDIR)/*.yaml
	rm -rf $(PNGDIR)/*.png
	rm -rf $(PNGDIR)/*.pvsm
	rm -rf $(LOGDIR)/*.log
