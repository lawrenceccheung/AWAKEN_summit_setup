import os
import pandas as pd
from netCDF4 import Dataset
import numpy as np

def getTurbSubset(csvfile, suffix):
    # Load the data from the database of all turbines
    allturbsdf = pd.read_csv(csvfile, low_memory=False)
    # Get just the King Plains turbines
    subset = [] 
    for x in allturbsdf.iterrows():
        if x[1]['# name'].endswith(suffix):
            subset.append(x[1])
    subsetdf = pd.DataFrame(subset[:])
    return subsetdf

getturbnames = lambda df: [x[1]['# name'] for x in df.iterrows()]

# Start the AMR-Wind case
setupdir     = '/ccs/proj/cfd162/lcheung/AWAKEN_summit_setup/UnstableABL_farmrun1/'
rundir       = '/gpfs/alpine/cfd162/scratch/lcheung/AWAKEN/testturbs/'
turbdir      = rundir+'/post_processing/actuator64500/'
summitcsv    = 'UnstableABL_farmrun_turbines.csv'

outdir       = 'NCturbpower/'

genefficiency = 0.90
scale         = 1000

farmlist = [{'title':'Thunder Ranch',   'suffix':'-TR'},
            {'title':'Chisholm View',   'suffix':'-CV'},
            {'title':'Armadillo Flats', 'suffix':'-AF'},
            {'title':'Breckinridge',    'suffix':'-BR'},
           ]

for farm in farmlist:
    print('Pulling data for '+farm['title'])
    turblist = getturbnames(getTurbSubset(setupdir+'/'+summitcsv,
                                          farm['suffix']))
    for turb in turblist:
        ncfile = turbdir+'/'+turb+'.nc'
        ncdat  = Dataset(ncfile, 'r')
        time   = ncdat[turb]['time'][:]
        power  = ncdat[turb]['power'][:]
        # Normalize and reset to start at t=0
        time   = time-time[0]
        power  = power/scale*genefficiency
        savedat = np.vstack((time, power)).transpose()
        savefile = outdir+'{turb}/{turb}.out'.format(turb=turb)
        print(savefile)
        # make a directory if necessary
        dirpath = os.path.dirname(savefile)
        try:
            os.makedirs(dirpath)
        except:
            pass
        np.savetxt(savefile, savedat)
