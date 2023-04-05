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

def loadPickle(picklefname):
    pfile = open(picklefname, 'rb')
    db   = pickle.load(pfile)
    x    = db['x']
    y    = db['y']
    z    = db['z']
    vx   = db['vx']
    vy   = db['vy']
    vz   = db['vz']
    time = db['time']
    pfile.close()
    return x, y, z, vx, vy, vz, time

def avgfield(v, mintime, maxtime):
    avgv = None
    iavg = 0
    for itime, vfield in v.items():
        if (mintime<=itime) and (itime<=maxtime):
            iavg += 1
            if avgv is None:
                avgv = vfield
            else:
                avgv += vfield
    #print(iavg)
    return avgv/float(iavg)

fileprefix = 'DATA_Summit_unstable_bananas1_'
wturbdir='/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/post_processing'
noturbdir='/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/UnstableABL1_farmrun1_noturbs/post_processing'
meandir = '/ccs/home/lcheung/cfd162/lcheung/AWAKEN_summit_setup/UnstableABL_farmrun1/post_processing/'

tavg1 = 300
tavg2 = 960
itime = 900

farmlist = [{'title':'AWAKEN domain', 'figsize':(8,4),
             'pklfile':fileprefix+'farm_z90_%s_mean_%i_%i.pkl', 
             'ncfile':'farm_z90_64500.nc',
             'noturb':'means/farm_z90_mean_noturb.pkl',
             'wturb':'means/farm_z90_mean_wturb.pkl'},
            {'title':'King Plains', 'figsize':(8,3),
             'pklfile':fileprefix+'KP_z90_%s_mean_%i_%i.pkl', 
             'ncfile':'KP_z090hh_64500.nc',
             'noturb':'means/KP_z90_mean_noturb.pkl',
             'wturb':'means/KP_z90_mean_wturb.pkl'},
            {'title':'Thunder Ranch', 'figsize':(8,2.5),
             'pklfile':fileprefix+'TR_z90_%s_mean_%i_%i.pkl', 
             'ncfile':'TR_z090hh_64500.nc',
             'noturb':'means/TR_z90_mean_noturb.pkl',
             'wturb':'means/TR_z90_mean_wturb.pkl'},
            
            # {'title':'Armadillo Flats', 'figsize':(8,3.25),
            #  'ncfile':'AF_z080hh_64500.nc',
            #  'noturb':'means/AF_z80_mean_noturb.pkl',
            #  'wturb':'means/AF_z80_mean_wturb.pkl'},
            # {'title':'Chisholm View', 'figsize':(8,2.5),
            #  'ncfile':'CV_z080hh_64500.nc',
            #  'noturb':'means/CV_z80_mean_noturb.pkl',
            #  'wturb':'means/CV_z80_mean_wturb.pkl'},
            # {'title':'Breckinridge', 'figsize':(8,2.5),
            #  'ncfile':'BR_z080hh_64500.nc', 
            #  'noturb':'means/BR_z80_mean_noturb.pkl',
            #  'wturb':'means/BR_z80_mean_wturb.pkl'},
          ]


for case in farmlist:
    print(case['title'])
    # ==== do the wturb case === 
    xm, ym, zm, vx, vy, vz, time = loadPickle(meandir+'/'+case['wturb'])
    vx_avg_wt = avgfield(vx, tavg1, tavg2)
    vy_avg_wt = avgfield(vy, tavg1, tavg2)
    vz_avg_wt = avgfield(vz, tavg1, tavg2)

    # Create a fresh db dictionary
    db = {}
    db['x'] = xm
    db['y'] = ym
    db['z'] = zm        
    db['vx'] = vx_avg_wt
    db['vy'] = vy_avg_wt
    db['vz'] = vz_avg_wt

    # Write out the picklefile
    pklfilename = case['pklfile']%('wturb', tavg1, tavg2)
    dbfile = open(pklfilename, 'wb')
    pickle.dump(db, dbfile, protocol=2)   # Note to use protocol=2 for maximum compatibility
    dbfile.close()

    # ==== do the noturb case === 
    xm, ym, zm, vx, vy, vz, time = loadPickle(meandir+'/'+case['noturb'])
    vx_avg_nt = avgfield(vx, tavg1, tavg2)
    vy_avg_nt = avgfield(vy, tavg1, tavg2)
    vz_avg_nt = avgfield(vz, tavg1, tavg2)

    # Create a fresh db dictionary
    db = {}
    db['x'] = xm
    db['y'] = ym
    db['z'] = zm        
    db['vx'] = vx_avg_nt
    db['vy'] = vy_avg_nt
    db['vz'] = vz_avg_nt

    # Write out the picklefile
    pklfilename = case['pklfile']%('noturb', tavg1, tavg2)
    dbfile = open(pklfilename, 'wb')
    pickle.dump(db, dbfile, protocol=2)   # Note to use protocol=2 for maximum compatibility
    dbfile.close()

    
