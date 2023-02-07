#!/usr/bin/env python

# Add any possible locations of amr-wind-frontend here
amrwindfedirs = ['../',
                 '/ccs/proj/cfd162/lcheung/amrwind-frontend/']
import sys, os, shutil
for x in amrwindfedirs: sys.path.insert(1, x)

# Important header information
import postprolib as pp

# Load the libraries
import postproamrwindsample as ppsample
import numpy             as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import xarray as xr
import argparse
import pickle

extractvar = lambda xrds, var, i : xrds[var][i,:].data.reshape(tuple(xrds.attrs['ijk_dims'][::-1]))

def makePKL(ncfile, itimevec, pklfile, vxvar='velocityx', vyvar='velocityy', vzvar='velocityz',
            verbose=0, overwrite=False):
    # If pklfile exists, load it
    if os.path.isfile(pklfile) and (not overwrite):
        pfile = open(pklfile, 'rb')
        db   = pickle.load(pfile)
        xm   = db['x']
        ym   = db['y']
        zm   = db['z']
        vx   = db['vx']
        vy   = db['vy']
        vz   = db['vz']        
        time = db['time']
        pfile.close()
    else:
        # Create a fresh db dictionary
        db = {}
        db['vx'] = {}
        db['vy'] = {}
        db['vz'] = {}
        db['time'] = []
    # Now load the ncfile data
    groups=ppsample.getGroups(ppsample.loadDataset(ncfile))
    with xr.open_dataset(ncfile, group=groups[0]) as ds:
        xm = ds['coordinates'].data[:,0].reshape(tuple(ds.attrs['ijk_dims'][1::-1]))
        ym = ds['coordinates'].data[:,1].reshape(tuple(ds.attrs['ijk_dims'][1::-1]))
        zm = ds['coordinates'].data[:,2].reshape(tuple(ds.attrs['ijk_dims'][1::-1]))
        dtime=xr.open_dataset(ncfile)
        ds = ds.assign_coords(coords={'xm':(['x','y'], xm),
                                      'ym':(['x','y'], ym),
                                      'time':dtime['time'],
                                     })
        dtime.close()
        db['x'] = xm
        db['y'] = ym
        db['z'] = zm        
        for itime in itimevec:
            if verbose>0:
                print("Saving step "+repr(itime))
            db['time'].append(itime)
            vx = extractvar(ds, vxvar, itime)
            vy = extractvar(ds, vyvar, itime)
            vz = extractvar(ds, vzvar, itime)
            db['vx'][itime] = vx
            db['vy'][itime] = vy
            db['vz'][itime] = vz
            
    # Write out the picklefile
    dbfile = open(pklfile, 'wb')
    pickle.dump(db, dbfile, protocol=2)
    dbfile.close()

    return


def makePKLinflow(ncfile, itimevec, pklfile, vxvar='velocityx', vyvar='velocityy', vzvar='velocityz',
                  verbose=0, overwrite=False):
    # If pklfile exists, load it
    if os.path.isfile(pklfile) and (not overwrite):
        pfile = open(pklfile, 'rb')
        db   = pickle.load(pfile)
        xm   = db['x']
        ym   = db['y']
        zm   = db['z']
        vx   = db['vx']
        vy   = db['vy']
        vz   = db['vz']        
        time = db['time']
        pfile.close()
    else:
        # Create a fresh db dictionary
        db = {}
        db['vx'] = {}
        db['vy'] = {}
        db['vz'] = {}
        db['time'] = []
    # Now load the ncfile data
    groups=ppsample.getGroups(ppsample.loadDataset(ncfile))
    with xr.open_dataset(ncfile, group=groups[0]) as ds:
        xm = ds['coordinates'].data[:,0].reshape(tuple(ds.attrs['ijk_dims'][::-1]))
        ym = ds['coordinates'].data[:,1].reshape(tuple(ds.attrs['ijk_dims'][::-1]))
        zm = ds['coordinates'].data[:,2].reshape(tuple(ds.attrs['ijk_dims'][::-1]))
        dtime=xr.open_dataset(ncfile)
        #ds = ds.assign_coords(coords={'xm':(['x','y'], xm),
        #                              'ym':(['x','y'], ym),
        #                              'time':dtime['time'],
        #                             })
        dtime.close()
        db['x'] = xm
        db['y'] = ym
        db['z'] = zm        
        for itime in itimevec:
            if verbose>0:
                print("Saving step "+repr(itime))
            db['time'].append(itime)
            vx = extractvar(ds, vxvar, itime)
            vy = extractvar(ds, vyvar, itime)
            vz = extractvar(ds, vzvar, itime)
            db['vx'][itime] = vx
            db['vy'][itime] = vy
            db['vz'][itime] = vz
            
    # Write out the picklefile
    dbfile = open(pklfile, 'wb')
    pickle.dump(db, dbfile, protocol=2)
    dbfile.close()

    return

# ========================================================================
#
# Main
#
# ========================================================================
if __name__ == "__main__":
    helpstring = """Create a movie
    """
    # Handle arguments
    parser     = argparse.ArgumentParser(description=helpstring)
    parser.add_argument(
        "ncfile",
        help="NetCDF file",
        type=str,
    )
    parser.add_argument(
        'itime',
        help="time index",
        nargs='+',
        type=int,
    )
    parser.add_argument(
        'outfile',
        help="Output file",
        type=str,
    )
    parser.add_argument(
        '--vxvar',
        help="Velocity x variable name",
        type=str,
        default='velocityx'
    )
    parser.add_argument(
        '--vyvar',
        help="Velocity y variable name",
        type=str,
        default='velocityy'
    )
    parser.add_argument(
        '--vzvar',
        help="Velocity z variable name",
        type=str,
        default='velocityz'
    )
    parser.add_argument(
        '--overwrite',
        help="Overwrite existing pkl file",
        default=False,
        action='store_true')
    parser.add_argument(
        '--inflow',
        help="Process inflow planes",
        default=False,
        action='store_true')
    parser.add_argument('-v', '--verbose', 
                        action='count', 
                        help="Verbosity level (multiple levels allowed)",
                        default=0)

    # Load the options
    args      = parser.parse_args()
    ncfile    = args.ncfile
    itime     = args.itime
    outfile   = args.outfile
    vxvar     = args.vxvar
    vyvar     = args.vyvar
    vzvar     = args.vzvar
    overwrite = args.overwrite
    inflow    = args.inflow
    verbose   = args.verbose
    
    if verbose>0:
        print('ncfile    = '+ncfile)
        print('itime     = '+repr(itime))
        print('outfile   = '+outfile)        
        print('vxvar     = '+vxvar)        
        print('vyvar     = '+vyvar)        
        print('vzvar     = '+vzvar)
        print('inflow    = '+repr(inflow))
        print('overwrite = '+repr(overwrite))

    if inflow:
        makePKLinflow(ncfile, itime, outfile, vxvar=vxvar, vyvar=vyvar, vzvar=vzvar,
                      overwrite=overwrite, verbose=verbose)
    else:
        makePKL(ncfile, itime, outfile, vxvar=vxvar, vyvar=vyvar, vzvar=vzvar,
                overwrite=overwrite, verbose=verbose)
