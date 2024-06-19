#!/usr/bin/python
#

# Get the location where this script is being run
import sys, os
scriptpath = os.path.dirname(os.path.realpath(__file__))

import yaml
import json
import numpy as np
import argparse
from collections            import OrderedDict 

def maketurbdict(defaults, turblist, turboffset=[0.0, 0.0]):
    outdict={}
    outdict['defaults']=defaults
    turbdictlist=[]
    for iturb, turb in enumerate(turblist):
        turbname = 'T%i'%iturb
        turbxy = list(np.array(turb) + np.array(turboffset))
        turbdictlist.append({'name':turbname,'pos':turbxy})
    outdict['turbinelist']=turbdictlist
    return outdict

def makeSTLdict(name, stlfile, pos, drawtower=False, drawnacelle=False):
    outdict=OrderedDict()
    outdict['name'] = name
    outdict['turbfile'] = stlfile
    outdict['pos'] = pos
    outdict['yaw']         = 0.0
    outdict['azimuth']     = 0.0
    outdict['drawtower']   = drawtower
    outdict['drawnacelle'] = drawnacelle
    return outdict

def getazimuthal(t, rotorspeed, toffset=0.0):
    revpersec=rotorspeed/60.0
    degpersec=revpersec*360.0
    return degpersec*(t-toffset)

def rpm2omega(rpm):
    rad2deg = 180.0/np.pi
    return rpm*2*np.pi/60.0*rad2deg

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

def sampleplanedict(name, vtkfile, clip=None):
    sampledict = OrderedDict()
    sampledict['name'] = name
    sampledict['files'] = vtkfile
    if clip is not None:
        sampledict['clip'] = clip 
    return sampledict


baseyaml="""\
solidplanes:
  defaults:
    color:
    - 0.90
    - 0.90
    - 0.90
    representation: Surface
  planelist:
  - name: ground
    origin:
    - 0
    - 0
    - 0.0
    p1:
    - 10000.0
    - 0.0
    - 0.0
    p2:
    - 0.0
    - 10000.0
    - 0.0
# annotate2D:
#   textlist:
#   - name: Title
#     text: Test text
#     fontsize: 5
#     pos: [0.9, 0.9]

colorbar:
  defaults:
    var: velocity
#    colormap: Cool to Warm
    colormap: Blue Orange (divergent)
  properties:
    TitleFontSize: 4
    LabelFontSize: 4
    ScalarBarThickness: 5
    ScalarBarLength: 0.33
    AutoOrient: 0
    Orientation: Horizontal
  limits:
  - 3
  - 8.0
"""

# ==== Text defaults ====
textdefaults={'color':[0,0,0],
              'pos':[0.7, 0.9],
              'fontsize':12,
              'WindowLocation':'Any Location'}

# ==== Run commands ====
cmds="""
# find settings proxy
colorPalette = GetSettingsProxy('ColorPalette')
# Properties modified on colorPalette
colorPalette.BackgroundColorMode = 'Single Color'
colorPalette.Background = [0.16666666666666666, 0.6666666666666666, 1.0]
#colorPalette.BackgroundColorMode = 'Gradient'
#colorPalette.Background2 = [0.6666666666666666, 1.0, 1.0]
#colorPalette.Background1 = [0.0, 0.0, 0.0]
RenderAllViews()
"""


turboffset = [2000.0, 2560.0]
turbhub    = [2000, 2650, 90]

view={}
view['front1'] = {
    'CameraPosition':[1500, 2350, 60.0],
    'CameraFocalPoint':[2000, 2500, 100],
    'CameraViewUp':[0, 0, 1],
}
view['front1'] = {
    'CameraPosition':[1650, 2500, 45.0],
    'CameraFocalPoint':[2000, 2540, 80],
    'CameraViewUp':[0, 0, 1],
}

view['side1'] = {
    'CameraPosition':[2000, 1750, 60.0],
    'CameraFocalPoint':[2000, 2500, 100],
    'CameraViewUp':[0, 0, 1],
}

view['side2'] = {
    'CameraPosition':[3200, 1750, 60.0],
    'CameraFocalPoint':[2700, 2500, 100],
    'CameraViewUp':[0, 0, 1],
}

# View from above
view['above1'] = {
    'CameraPosition':[2700, 2500, 2000.0],
    'CameraFocalPoint':[3000, 2500, 100],
    'CameraViewUp':[1, 0, 0],
}

# View from above
view['above2'] = {
    'CameraPosition':[1000, 2500, 600.0],
    'CameraFocalPoint':[3000, 2500, 100],
    'CameraViewUp':[1, 0, 0],
}



# ========================================================================
#
# Main
#
# ========================================================================
if __name__ == "__main__":
    helpstring="""Generate input files for renderfarm.py
    """
    
    # Handle arguments
    parser     = argparse.ArgumentParser(description=helpstring)
    parser.add_argument(
        "outfile",
        help="output file",
        type=str,
    )
    parser.add_argument(
        '-t','--time',
        help="Time",
        type=float,
        required=False,
        default=0.0,
    )
    parser.add_argument(
        '-n','--nturbines',
        help="Number of turbines",
        type=int,
        required=False,
        default=-1,
    )
    parser.add_argument(
        '--view',
        help="View",
        type=str,
        required=False,
        default='front1',
    )
    parser.add_argument(
        '--hh',
        help="HH plane",
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '--sw',
        help="SW plane",
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '--rp',
        help="RP plane",
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '-o','--outputprefix',
        help="Output filename prefix",
        type=str,
        required=False,
        default='visualization',
    )

    # Load the options
    args      = parser.parse_args()
    outfile   = args.outfile
    time      = args.time
    Nturbs    = args.nturbines
    viewcam   = args.view
    outputprefix = args.outputprefix
    hh        = args.hh
    sw        = args.sw
    rp        = args.rp
    
    rpm       = 7.0

    basedir     = scriptpath
    basedict    = yaml.safe_load(baseyaml)
    turbxy      = np.loadtxt(basedir+'/KPcoordsXY.txt')
    azimuth     = getazimuthal(time, rpm)
    
    turbdefault = {'turbfile':basedir+'/STL/nrel_2p8_127_nospinnac.stl','yaw':270.0,'azimuth':azimuth, 'hubheight':90.0}
    basedict['turbines'] = maketurbdict(turbdefault, turbxy[:Nturbs], turboffset=turboffset)
    basedict['turbines']['turbinelist'].append(makeSTLdict('house', basedir+'/STL/Cottage_FREE.stl', [1900, 2400, 0.0]))
    basedict['turbines']['turbinelist'].append(makeSTLdict('tree', basedir+'/STL/tree01.stl',       [1950, 2400, 0.0]))

    # Sample planes
    clipdict={'name':'clip1', 'origin':turbhub, 'normal':[-1, 0, 0]}
    sampledictlist = []
    sampledictlist += [ sampleplanedict('RP', basedir+'/turbrp/plane_10/turbrp_20900.0.vtk', clip=None)      ] if args.rp else []
    sampledictlist += [ sampleplanedict('HH', basedir+'/turbhh/turbhh_20900.0.vtk',          clip=clipdict), ] if args.hh else []
    sampledictlist += [ sampleplanedict('SW', basedir+'/turbsw/turbsw_20900.0.vtk',          clip=clipdict), ] if args.sw else []
    
    basedict['sampleplanes'] = {'sampleplanelist':sampledictlist}
    
    basedict['renderview'] = {'properties':view[viewcam]}
    basedict['output']   = {'filename':outputprefix+'.png',
                            #'savestate':outputprefix+'.pvsm',
                            'imagesize':[1900, 1080]}
    basedict['annotate2D'] = {'defaults':textdefaults,
                              'textlist':[{'name':'TimeTitle',
                                           'text':"Time: %0.2f sec"%time}]}
    basedict['runcommands'] = {'execstring':cmds}
    with open(outfile, 'w') as fpo:
        json.dump(basedict, fpo, indent=2)
