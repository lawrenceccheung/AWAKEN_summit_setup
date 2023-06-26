#!/usr/bin/env python
#
import numpy as np
import pandas as pd
import sys, os, csv
import re
import shlex
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

def getazimuthal(t, rotorspeed, toffset=0.0):
    revpersec=rotorspeed/60.0
    degpersec=revpersec*360.0
    return degpersec*(t-toffset)

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

def interpdict(t, t1, t2, dict1, dict2, holdendpoints=True):
    if t<t1 and holdendpoints: return dict1
    if t>t2 and holdendpoints: return dict2
    outputdict  = {}
    handlearray = lambda x: np.array(x) if isinstance(x, list) else x
    def convertarray(x):
        if isinstance(x, np.ndarray):
            return [float(y) for y in x ]
        else:
            return x

    for k,g in dict1.items():
        d1 = handlearray(dict1[k])
        d2 = handlearray(dict2[k])
        x  = (d2-d1)/(t2-t1)*(t-t1) + d1
        outputdict[k] = convertarray(x)
    return outputdict

title="Write scene yaml"
parser = argparse.ArgumentParser(description=title)
parser.add_argument('inputtime')

# Load the options
args      = parser.parse_args()
inputtime = float(args.inputtime)


# =====================================
# Set some simulation globals
tstart     = 16425.0
time       = float(np.floor(inputtime))
turbhh     = 90.0
maxturbs   = 100
defaultyaw = 175.0
rotorspeed = 12.0
allturbazi = getazimuthal(inputtime, rotorspeed, toffset=tstart)
outfilename= 'yamldir/scene3A_%0.2f.yaml'%inputtime
outpng     = 'pngdir/scene3A_%0.2f.png'%inputtime
outpvsm    = 'pngdir/scene3A_%0.2f.pvsm'%inputtime
summitcsv  = '../../lcheung/awaken.github/SummitRuns/AWAKEN_summit_setup/UnstableABL_farmrun1/UnstableABL_farmrun_turbines.csv' 
planedir   = '/ascldap/users/lcheung/GPFS/AWAKEN/fancymovies/vtkfiles/KP_turbhh/' #'../KP_turbine_vtk/KPturbs/'
planedirSW = '/ascldap/users/lcheung/GPFS/AWAKEN/fancymovies/vtkfiles/KP_turbSW/' #'../KP_turbine_vtk/KPturbsSW/'
planedirfarm = '/ascldap/users/lcheung/GPFS/AWAKEN/fancymovies/vtkfiles/farm_KP/' # /ascldap/users/lcheung/GPFS/AWAKEN/fancymovies/vtkfiles/farm_KP/' #'../samplefiles'
plotHH     = False
plotSW     = True
addturbs   = True
plotfarmHH = True
t1         = 16550.0   # Start of zoom
t2         = 16600.0   # End of zoom
# =====================================
view1 = {
    'CameraPosition': [632000.0, 4030000.0, 24000.0],
    'CameraFocalPoint': [632000.0, 4030000.0, 85.0],
    'CameraViewUp': [0, 1, 0],
#    'CameraViewAngle': 0.05477534500859669,
    'CameraParallelScale':184.53145
}
view2 = {
    'CameraPosition':  [632000, 4027500, 750.0],
    'CameraFocalPoint':[632000, 4030000, 20.0],
    'CameraViewUp':[-0.015831871495391725, 0.14554974560510944, 0.9892242533415977],
    'CameraParallelScale':184.53144999999495,
}
# view2 = {
#     'CameraPosition':[631193.9982428647, 4006708.2968544867, 3486.5129507579463],
#     'CameraFocalPoint':[632000, 4030000, 20.0],
#     'CameraViewUp':[-0.015831871495391725, 0.14554974560510944, 0.9892242533415977],
#     'CameraParallelScale':184.53144999999495,
# }

# Construct a normal wind direction vector
theta   = (270-defaultyaw)*np.pi/180.0
winddir = [np.cos(theta), np.sin(theta), 0.0]

yamldict = OrderedDict()

# Write the turbine defaults
turbdefaults = OrderedDict()
turbdefaults['turbfile']  = '/hpc_projects/AWAKEN/turbines/NREL-2.8-127_Surface/nrel_2p8_127_nospinnac.stl'
turbdefaults['hubheight'] = turbhh
turbdefaults['yaw']       = defaultyaw
turbdefaults['azimuth']   = allturbazi

if addturbs:
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
    azimuth = allturbazi
    if addturbs:
        turbspec = OrderedDict()
        turbspec['name'] = name
        turbspec['pos']  = pos
        turbspec['azimuth'] = azimuth
        turblist.append(comseq(turbspec))

    # Add the HH sampling planes
    if plotHH:
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
    if plotSW:
        samplespec = OrderedDict()
        samplespec['name'] = name+'_SWplane'
        samplespec['files'] = planedirSW+'T'+name+'_KPsw_%0.1f.vtk'%time
        # Set the clipping parameters
        clipspec         = OrderedDict()
        clipspec['name'] = samplespec['name']+'_clip2'
        turborigin = np.array([pos[0], pos[1], turbhh])
        cliporigin = turborigin + 75.0*np.array(winddir)
        clipspec['origin'] = [float(x) for x in cliporigin]
        clipspec['normal'] = [-float(x) for x in winddir]
        samplespec['clip'] = comseq(clipspec)
        sampleplanelist.append(comseq(samplespec))

    if len(turblist)>maxturbs: break

if addturbs:
    yamldict['turbines']['turbinelist'] = comseq(turblist)

if plotfarmHH:
    samplespec = OrderedDict()
    samplespec['name'] = 'Farm_KPplane'
    samplespec['files'] = planedirfarm+'/TFarm_KP090_%0.1f.vtk'%time
    sampleplanelist.append(comseq(samplespec))

yamldict['sampleplanes'] = OrderedDict()
yamldict['sampleplanes']['sampleplanelist'] = comseq(sampleplanelist)

# ==== write a ground plane ==== 
yamldict['solidplanes'] = OrderedDict()
yamldict['solidplanes']['defaults'] = {'color':[0.4, 0.475, 0.4],
                                       'representation':'Surface'}
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

# ==== Rendering view ====
renderview = OrderedDict()
renderprop = interpdict(inputtime, t1, t2, view1, view2)
renderview['properties'] = comseq(renderprop)
yamldict['renderview'] = comseq(renderview)

# ==== Colorbar ====
colorbar = OrderedDict()
colorbar['defaults']   = comseq({'var':'velocity',
                                 'colormap':'Blue Orange (divergent)',
                             })
colorbar['properties'] = comseq({'TitleFontSize':4,
                                 'LabelFontSize':4,
                                 'ScalarBarThickness':5,
                                 'ScalarBarLength': 0.33,
                                 'AutoOrient':0,
                                 'Orientation':'Horizontal'
                             })
colorbar['limits'] = [4, 14.0]
yamldict['colorbar'] = comseq(colorbar)

# ==== Run commands ====
cmds="""
# find settings proxy
colorPalette = GetSettingsProxy('ColorPalette')
# Properties modified on colorPalette
colorPalette.BackgroundColorMode = 'Gradient'
colorPalette.Background2 = [0.6666666666666666, 1.0, 1.0]
#colorPalette.Background1 = [0.0, 0.0, 0.0]
RenderAllViews()
"""

# ==== Output section ====
yamldict['runcommands'] = OrderedDict()
yamldict['runcommands']['execstring'] = cmds


# ==== Output section ====
yamldict['output'] = OrderedDict()
yamldict['output']['filename']  = outpng #'test.png'
yamldict['output']['imagesize'] = [1900,1200]
#yamldict['output']['savestate'] = outpvsm


# ========= write the yaml file ==========
#outfilename = 'sys.stdout'
outfile=sys.stdout if outfilename.strip()=='sys.stdout' else open(outfilename, 'w')
print('writing '+outfilename)
yaml.dump(comseq(yamldict), outfile, **dumperkwargs)

