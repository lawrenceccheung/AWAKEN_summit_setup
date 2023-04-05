# Load the amrwind-frontend module
# Add any possible locations of amr-wind-frontend here
amrwindfedirs = ['../',
                 '/ccs/proj/cfd162/lcheung/amrwind-frontend/']
import sys, os, shutil
for x in amrwindfedirs: sys.path.insert(1, x)

# Load the libraries
import postproamrwindsample as ppsample
import numpy             as np
import xarray as xr
import pickle
import pandas as pd

extractvar = lambda xrds, var, i : xrds[var][i,:].data.reshape(tuple(xrds.attrs['ijk_dims'][::-1]))

fileprefix = 'DATA_Summit_unstable_bananas1_'
wturbdir='/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing'
noturbdir='/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/UnstableABL1_farmrun1_noturbs/post_processing'
itime = 900

filelist = [
    {'pklfile':fileprefix+'farm_z90_wturb_inst_900.pkl',  'ncfile':'farm_z90_64500.nc',  'rundir':wturbdir},
    {'pklfile':fileprefix+'farm_z90_noturb_inst_900.pkl', 'ncfile':'farm_z90_64500.nc',  'rundir':noturbdir},
    {'pklfile':fileprefix+'KP_z90_wturb_inst_900.pkl',    'ncfile':'KP_z090hh_64500.nc', 'rundir':wturbdir},
    {'pklfile':fileprefix+'KP_z90_noturb_inst_900.pkl',   'ncfile':'KP_z090hh_64500.nc', 'rundir':noturbdir},
    {'pklfile':fileprefix+'TR_z90_wturb_inst_900.pkl',    'ncfile':'TR_z090hh_64500.nc', 'rundir':wturbdir},
    {'pklfile':fileprefix+'TR_z90_noturb_inst_900.pkl',   'ncfile':'TR_z090hh_64500.nc', 'rundir':noturbdir},
    ]

for case in filelist:
    ncfile = case['ncfile']
    rundir = case['rundir']
    pklfile = case['pklfile']

    print(pklfile)
    groups=ppsample.getGroups(ppsample.loadDataset(rundir+'/'+ncfile))
    with xr.open_dataset(rundir+'/'+ncfile, group=groups[0]) as ds:
        xm = ds['coordinates'].data[:,0].reshape(tuple(ds.attrs['ijk_dims'][1::-1]))
        ym = ds['coordinates'].data[:,1].reshape(tuple(ds.attrs['ijk_dims'][1::-1]))
        zm = ds['coordinates'].data[:,2].reshape(tuple(ds.attrs['ijk_dims'][1::-1]))
        dtime=xr.open_dataset(rundir+'/'+ncfile)
        ds = ds.assign_coords(coords={'xm':(['x','y'], xm),
                                      'ym':(['x','y'], ym),
                                      'time':dtime['time'],
        })
        dtime.close()
        vz = extractvar(ds, 'velocityz', itime)
        vy = extractvar(ds, 'velocityy', itime)
        vx = extractvar(ds, 'velocityx', itime)
        vh = np.sqrt(vx**2 + vy**2)
    
        # Create a fresh db dictionary
        db = {}
        db['x'] = xm
        db['y'] = ym
        db['z'] = zm        
        db['vx'] = vx
        db['vy'] = vy
        db['vz'] = vz

        # Write out the picklefile
        dbfile = open(pklfile, 'wb')
        pickle.dump(db, dbfile, protocol=2)
        dbfile.close()

