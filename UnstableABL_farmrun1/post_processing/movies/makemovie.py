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

extractvar = lambda xrds, var, i : xrds[var][i,:].data.reshape(tuple(xrds.attrs['ijk_dims'][::-1]))

def setfigtextsize(ax, fsize):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label, ax.yaxis.get_offset_text()] + ax.get_xticklabels() + ax.get_yticklabels() ):
        item.set_fontsize(fsize)
        
def makeHHpng(ncfile, itimevec, savefile, paramdict, verbose=0):
    groups=ppsample.getGroups(ppsample.loadDataset(ncfile))
    with xr.open_dataset(ncfile, group=groups[0]) as ds:
        xm = ds['coordinates'].data[:,0].reshape(tuple(ds.attrs['ijk_dims'][1::-1]))
        ym = ds['coordinates'].data[:,1].reshape(tuple(ds.attrs['ijk_dims'][1::-1]))
        dtime=xr.open_dataset(ncfile)
        ds = ds.assign_coords(coords={'xm':(['x','y'], xm),
                                      'ym':(['x','y'], ym),
                                      'time':dtime['time'],
                                     })
        dtime.close()

        for itime in itimevec:
            # Create a figure
            fig, ax = plt.subplots(1,1,figsize=paramdict['figsize'], dpi=125)
            vy = extractvar(ds, 'velocityy', itime)
            vx = extractvar(ds, 'velocityx', itime)
            vh = np.sqrt(vx**2 + vy**2)
        
            c=ax.contourf(ds['xm'], ds['ym'], vh[0,:,:], levels=np.linspace(6,12,101), cmap='coolwarm')
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            cbar=fig.colorbar(c, ax=ax, cax=cax)
            cbar.ax.tick_params(labelsize=8)
            ax.set_aspect('equal')
            #ax.set_xlim([630000, 670000])
            setfigtextsize(ax, 8)        
            ax.get_ylim()
            ax.set_title(paramdict['title']+' Time: %0.1f'%ds['time'][itime], fontsize =8)
            ax.set_xlabel('UTM Easting [m]')
            ax.set_ylabel('UTM Northing [m]')
            savefilename=savefile.format(itime=itime, time=ds['time'][itime])
            if verbose>0:
                print(savefilename)
            plt.savefig(savefilename)
    return

# ========================================================================
#
# Main
#
# ========================================================================
if __name__ == "__main__":

    defaultdict = {'figsize':(8,6), 'title':''}
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
        '--paramdict',
        help="Parameter dict (defaults: %s)"%repr(defaultdict),
        type=str,
        required=False,
        default="{}",
    )
    parser.add_argument('-v', '--verbose', 
                        action='count', 
                        help="Verbosity level (multiple levels allowed)",
                        default=0)

    # Load the options
    args      = parser.parse_args()
    ncfile    = args.ncfile
    itime     = args.itime
    outfile   = args.outfile
    verbose   = args.verbose
    indict    = eval(args.paramdict)
    defaultdict.update(indict)
    if verbose>0:
        print('ncfile    = '+ncfile)
        print('itime     = '+repr(itime))
        print('outfile   = '+outfile)        
        print('paramdict = '+repr(defaultdict))

    makeHHpng(ncfile, itime, outfile, defaultdict, verbose=verbose)
