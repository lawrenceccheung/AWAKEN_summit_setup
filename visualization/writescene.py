#!/usr/bin/env python
import json
import sys
import copy
import numpy as np
from collections            import OrderedDict
import argparse

# Load ruamel or pyyaml as needed
try:
    import ruamel.yaml as yaml
    #print("# Loaded ruamel.yaml")
    useruamel=True
    loaderkwargs = {'Loader':yaml.RoundTripLoader}
    dumperkwargs = {'Dumper':yaml.RoundTripDumper, 'indent':2, 'default_flow_style':False} # 'block_seq_indent':2, 'line_break':0, 'explicit_start':True, 
    #dumperkwargs = {'default_flow_style':False }

except:
    import yaml as yaml
    #print("# Loaded yaml")
    useruamel=False
    loaderkwargs = {}
    dumperkwargs = {'default_flow_style':False }

if useruamel:
    from ruamel.yaml.comments import CommentedMap 
    def comseq(d):
        """
        Convert OrderedDict to CommentedMap
        """
        if isinstance(d, OrderedDict):
            cs = CommentedMap()
            for k, v in d.items():
                cs[k] = comseq(v)
            return cs
        return d

# Helper functions to get defaults from a dictionary
getdictval = lambda d, k, default: default[k] if k not in d else d[k]
ndarr2list = lambda arr: [float(x) for x in arr]
rpm2deg    = lambda t, rpm: t*rpm/60.0*360

testpath   = lambda t: np.array([t*50, 0, 0])

helpstring = 'write json files for rendering'
# Handle arguments
parser     = argparse.ArgumentParser(description=helpstring)
parser.add_argument(
    "-i",
    "--inputyaml",
    help="Input yaml",
    type=str,
    required=True
)

parser.add_argument(
    "-o",
    "--outputjson",
    help="Output json",
    type=str,
    required=True
)
parser.add_argument(
    "--outputpng",
    help="Output png",
    type=str,
    default='',
    required=False,
)
parser.add_argument(
    "-t",
    help="Time",
    type=float,
    default=0.0,
    required=False,
)

# Load the options
args      = parser.parse_args()
in_file   = args.inputyaml
out_file  = args.outputjson
out_png   = args.outputpng
time      = args.t

#in_file  = sys.argv[1]
#out_file = sys.argv[2]

# Load the scene inputs
with open(in_file) as fpi:
    sceneparams = yaml.load(fpi, Loader=yaml.Loader)

turbrpm = sceneparams['turbinerpm'] if 'turbinerpm' in sceneparams else 0.0
outdict = copy.deepcopy(sceneparams['basetemplate'])
turblist = []

# Load in any UDF functions
if 'pythonudf' in sceneparams:
    for f in sceneparams['pythonudf']:
        for k, g in f.items(): exec(g)
    #print(sceneparams['pythonudf'])

# ==== Add turbine rotors ====
for iturb, xy in enumerate(sceneparams['farmxy']):
    turbdict = {}
    turbdict['name'] = 'Turb'+repr(iturb)
    turbdict['pos']  = comseq(xy)
    turbdict['azimuth'] = rpm2deg(time, turbrpm)  
    turblist.append(turbdict)

# ==== Add turbine floaters ====
if 'floatermesh' in sceneparams:
    floatermesh = sceneparams['floatermesh']
    float_offset = [0, 5, 0]
    for iturb, xy in enumerate(sceneparams['farmxy']):
        floatdict = {}
        xyz = np.array(xy)
        xyz.resize(3)
        #print(xy, xyz.resize(3))
        floatdict['name'] = 'Turb'+repr(iturb)+'_float'
        floatdict['pos']  = ndarr2list(xyz + np.array(float_offset))
        floatdict['turbfile'] = floatermesh
        floatdict['drawtower']   = False
        floatdict['drawnacelle'] = False
        floatdict['scale']       = sceneparams['floaterscale']
        if 'floatercolor' in sceneparams:
            floatdict['colordict'] = sceneparams['floatercolor']
        turblist.append(floatdict)

# ==== Add moving objects ====
if 'movingobjects' in sceneparams:
    for obj in sceneparams['movingobjects']:
        objbase = copy.deepcopy(obj)
        objbase['drawtower']   = False
        objbase['drawnacelle'] = False        
        xyzlist = objbase.pop('xyzlist', None)
        funcname = objbase.pop('trajectoryfunc', None)
        for ixyz, xyz in enumerate(xyzlist):
            turbobj = copy.deepcopy(objbase)
            turbobj['name'] = turbobj['name']+repr(ixyz)
            if funcname is not None:
                trajfunc = globals()[funcname]
                delta_xyz = trajfunc(time)
            else:
                delta_xyz = np.array([0,0,0])
            turbobj['pos'] = ndarr2list(np.array(xyz) + delta_xyz)
            turblist.append(turbobj)
            
# Add to the turbine list
outdict['turbines']['turbinelist'] = turblist

# Change renderview if necessary
renderprop = outdict['renderview']['properties']
if isinstance(renderprop['CameraPosition'], str):
    renderprop['CameraPosition'] = ndarr2list(globals()[renderprop['CameraPosition']](time))
if isinstance(renderprop['CameraFocalPoint'], str):
    renderprop['CameraFocalPoint'] = ndarr2list(globals()[renderprop['CameraFocalPoint']](time))
if isinstance(renderprop['CameraViewUp'], str):
    renderprop['CameraViewUp'] = ndarr2list(globals()[renderprop['CameraViewUp']](time))


# Change the output names
outfname = outdict['output']['filename']
if len(out_png)>0:
    outdict['output']['filename'] = out_png
else:
    outdict['output']['filename'] = outfname.format(time=time)

# ========= write the yaml file ==========
# outfilename = 'sys.stdout'
# outfile=sys.stdout if outfilename.strip()=='sys.stdout' else open(outfilename, 'w')
# yaml.dump(comseq(outdict), outfile, **dumperkwargs)

#print(outdict)
with open(out_file, 'w') as fpo:
    json.dump(outdict, fpo, indent=2)
