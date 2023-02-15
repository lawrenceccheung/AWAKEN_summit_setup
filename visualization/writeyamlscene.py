#!/usr/bin/env python
#
import numpy as np
import pandas as pd
import sys, os, csv
import re
import shlex
from collections            import OrderedDict 

# Load ruamel or pyyaml as needed
try:
    import ruamel.yaml as yaml
    print("# Loaded ruamel.yaml")
    useruamel=True
    loaderkwargs = {'Loader':yaml.RoundTripLoader}
    dumperkwargs = {'Dumper':yaml.RoundTripDumper, 'indent':2, 'default_flow_style':False} # 'block_seq_indent':2, 'line_break':0, 'explicit_start':True, 
    #dumperkwargs = {'default_flow_style':False }

except:
    import yaml as yaml
    print("# Loaded yaml")
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

# =====================================
# Set some simulation globals
time       = 16425.0
turbhh     = 90.0
maxturbs   = 5
defaultyaw = 175.0
outfilename= 'test.yaml'
summitcsv  = 'UnstableABL_farmrun_turbines.csv'
planedir   = 'KPturbs/'
planedirSW = 'KPturbsSW/'

# =====================================

# Construct a normal wind direction vector
theta = (270-defaultyaw)*np.pi/180.0
winddir = [np.cos(theta), np.sin(theta), 0.0]

yamldict = OrderedDict()

# Write the turbine defaults
turbdefaults = OrderedDict()
turbdefaults['turbfile']  = '/ascldap/users/lcheung/GPFS/AWAKEN/testmovie/turbine.stl'
turbdefaults['hubheight'] = turbhh
turbdefaults['yaw']       = defaultyaw
turbdefaults['azimuth']   = 0.0

yamldict['turbines'] = OrderedDict()
yamldict['turbines']['defaults'] = comseq(turbdefaults)


# Load the data from the database of all turbines
allturbsdf = pd.read_csv(summitcsv, low_memory=False)

# Get just the King Plains turbines
subset = [] 
for x in allturbsdf.iterrows():
    if x[1]['# name'].endswith('-KP'):
        subset.append(x[1])
subsetdf = pd.DataFrame(subset[:])

turblist = [] 
sampleplanelist = []
# Set up the turblist
for turb in subsetdf.iterrows():
    name = turb[1]['# name']
    pos  = [turb[1][' x'], turb[1][' y']]
    azimuth = 0.0
    turbspec = OrderedDict()
    turbspec['name'] = name
    turbspec['pos']  = pos
    turbspec['azimuth'] = azimuth
    turblist.append(comseq(turbspec))

    # Add the HH sampling planes
    samplespec = OrderedDict()
    samplespec['name'] = name+'_HHplane'
    samplespec['files'] = planedir+'T'+name+'_KPturbhh_%0.1f.vtk'%time
    # Set the clipping parameters
    clipspec         = OrderedDict()
    clipspec['name'] = samplespec['name']+'_clip1'
    turborigin = np.array([pos[0], pos[1], turbhh])
    cliporigin = turborigin + 25.0*np.array(winddir)
    clipspec['origin'] = [float(x) for x in cliporigin]
    clipspec['normal'] = [-float(x) for x in winddir]
    samplespec['clip'] = comseq(clipspec)
    sampleplanelist.append(comseq(samplespec))

    # Add the SW sampling planes
    samplespec = OrderedDict()
    samplespec['name'] = name+'_SWplane'
    samplespec['files'] = planedirSW+'T'+name+'_KPsw_%0.1f.vtk'%time
    # Set the clipping parameters
    clipspec         = OrderedDict()
    clipspec['name'] = samplespec['name']+'_clip2'
    turborigin = np.array([pos[0], pos[1], turbhh])
    cliporigin = turborigin + 25.0*np.array(winddir)
    clipspec['origin'] = [float(x) for x in cliporigin]
    clipspec['normal'] = [-float(x) for x in winddir]
    samplespec['clip'] = comseq(clipspec)
    sampleplanelist.append(comseq(samplespec))

    if len(turblist)>maxturbs: break

yamldict['turbines']['turbinelist'] = comseq(turblist)

yamldict['sampleplanes'] = OrderedDict()
yamldict['sampleplanes']['sampleplanelist'] = comseq(sampleplanelist)

# ==== write a ground plane ==== 
yamldict['solidplanes'] = OrderedDict()
yamldict['solidplanes']['defaults'] = {'color':[0.8, 0.75, 0.75]}
groundorig = np.array([653106.1017967543, 4023617.986548658, 0])
v1         = np.array([-1220.1803984672154, 13946.725773284437, 0])
v2         = np.array([-24904.867452293638, -2178.893568691456 , 0])
groundp1   = np.array(groundorig) + v1
groundp2   = np.array(groundorig) + v2
solidplanelist = []
planespec = OrderedDict()
planespec['name'] = 'ground'
planespec['origin'] = [float(x) for x in groundorig]
planespec['p1']     = [float(x) for x in groundp1]
planespec['p2']     = [float(x) for x in groundp2]
solidplanelist.append(comseq(planespec))
yamldict['solidplanes']['planelist'] = solidplanelist

# ==== Output section ====
yamldict['output'] = OrderedDict()
yamldict['output']['filename']  = 'test.png'
yamldict['output']['imagesize'] = [1080,600]


# ========= write the yaml file ==========
#outfilename = 'sys.stdout'
outfile=sys.stdout if outfilename.strip()=='sys.stdout' else open(outfilename, 'w')

yaml.dump(comseq(yamldict), outfile, **dumperkwargs)

