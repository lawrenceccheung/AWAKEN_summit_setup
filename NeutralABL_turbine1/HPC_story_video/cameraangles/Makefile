# Set some definitions
EXE    = ../KPfarm.py
RENDER = ../renderwindfarm.py
NTURBS = 1000

all: json png

json:
	python $(EXE) front1.json -t 1.0 -n $(NTURBS) --view front1 -o front1 --sw
	python $(EXE) side1.json -t 1.0  -n $(NTURBS) --view side1 -o side1 --sw
	python $(EXE) side2.json -t 1.0  -n $(NTURBS) --view side2 -o side2 --sw
	python $(EXE) above1.json -t 1.0 -n 86 --view above1 -o above1 --hh --rp
	python $(EXE) above2.json -t 1.0 -n 86 --view above2 -o above2 --hh --rp


png:
	pvbatch $(RENDER) -j front1.json  -v
	pvbatch $(RENDER) -j side1.json  -v
	pvbatch $(RENDER) -j side2.json  -v
	pvbatch $(RENDER) -j above1.json  -v
	pvbatch $(RENDER) -j above2.json  -v


