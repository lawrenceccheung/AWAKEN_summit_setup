#!/usr/bin/python
#

# Add any possible locations of amr-wind-frontend here
rootdirs = ['../',
            ]
import sys, os, shutil
for x in rootdirs: sys.path.insert(1, x)

import KPfarm as KP
import yaml
import json
import numpy as np
import argparse
from collections            import OrderedDict 

# Get the location where this script is being run
scriptpath = os.path.dirname(os.path.realpath(__file__))


# ========================================================================
#
# Main
#
# ========================================================================

helpstring="""Generate input files for renderfarm.py"""
# Handle arguments
parser     = argparse.ArgumentParser(description=helpstring)
parser.add_argument(
    '-n','--nturbines',
    help="Number of turbines",
    type=int,
    required=False,
    default=100,
)
parser.add_argument(
    '--rpm',
    help="Rotor speed",
    type=float,
    required=False,
    default=6.0,
)
parser.add_argument(
    '--fps',
    help="Frames per second",
    type=float,
    required=False,
    default=30.0,
)
parser.add_argument(
    '--jsondir',
    help="json directory",
    type=str,
    required=False,
    default='jsondir',
)
parser.add_argument(
    '--pngdir',
    help="png directory",
    type=str,
    required=False,
    default='pngdir',
)
parser.add_argument(
    '--SurfRep',
    help="Set surface representation",
    default=None,
    required=False
)

# Load the options
args      = parser.parse_args()
Nturbs    = args.nturbines

rpm       = args.rpm
fps       = args.fps
jsondir   = args.jsondir
pngdir    = args.pngdir
surfrep   = args.SurfRep

basedir     = os.path.dirname(scriptpath)
turbxy      = np.loadtxt(basedir+'/KPcoordsXY.txt')
t1          = 20960.0
t2          = 20970.0
dt          = 1.0/fps
tvec        = np.arange(t1, t2+1.0e-6, dt)
jsonfile    = jsondir+'/frame_%0.2f.json'
pngprefix   = pngdir+'/frame_%0.2f'

for t in tvec:
    print('TIME = %0.2f'%t)
    azimuth     = KP.getazimuthal(t, rpm, toffset=t1)
    view        = KP.interpdict(t, t1, t2, KP.view['above2'], KP.view['endside1'])

    basedict    = yaml.safe_load(KP.baseyaml)

    # Add turbine
    turbdefault = {'turbfile':basedir+'/STL/nrel_2p8_127_nospinnac.stl','yaw':270.0,'azimuth':azimuth, 'hubheight':90.0}
    basedict['turbines'] = KP.maketurbdict(turbdefault, turbxy[:Nturbs], turboffset=KP.turboffset)
    # Set last two turbines to zero azimuth
    if Nturbs>len(turbxy)-2:
        basedict['turbines']['turbinelist'][-1]['azimuth'] = 0.0
        basedict['turbines']['turbinelist'][-2]['azimuth'] = 0.0
    # Add house and tree
    basedict['turbines']['turbinelist'].append(KP.makeSTLdict('house', basedir+'/STL/Cottage_FREE.stl', [1900, 2400, 0.0]))
    basedict['turbines']['turbinelist'].append(KP.makeSTLdict('tree', basedir+'/STL/tree01.stl',       [1950, 2400, 0.0]))

    # Add sampling planes
    clipdict={'name':'clip1', 'origin':KP.turbhub, 'normal':[-1, 0, 0]}
    if surfrep:
        displayprop = {'Representation':surfrep}
    else:
        displayprop = None
    
    sampledictlist =  [ KP.sampleplanedict('SW', basedir+'/turbsw/turbsw_%0.1f.vtk'%round(t), clip=clipdict,      displayprop=displayprop) ]
    sampledictlist += [ KP.sampleplanedict('HH', basedir+'/turbhh/turbhh_%0.1f.vtk'%round(t),   clip=clipdict,     displayprop=displayprop) ]
    sampledictlist += [ KP.sampleplanedict('RP', basedir+'/turbrp/plane_10/turbrp_%0.1f.vtk'%round(t), clip=None, displayprop=displayprop) ] 

    basedict['sampleplanes'] = {'sampleplanelist':sampledictlist}

    # Annotation
    basedict['annotate2D'] = {'defaults':KP.textdefaults,
                              'textlist':[{'name':'TimeTitle',
                                           'text':"Time: %0.2f sec"%t}]}

    # Write out png and json
    basedict['renderview'] = {'properties':view}
    basedict['output']   = {'filename':pngprefix%t+'.png',
                            #'savestate':outputprefix+'.pvsm',
                            'imagesize':[1900, 1080]}
    basedict['runcommands'] = {'execstring':KP.cmds}    
    with open(jsonfile%t, 'w') as fpo:
        json.dump(basedict, fpo, indent=2)
