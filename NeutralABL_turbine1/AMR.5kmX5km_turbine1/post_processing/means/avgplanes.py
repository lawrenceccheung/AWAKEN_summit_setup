#!/usr/bin/env python                                                                                                                                                                                            

amrwindfedirs = ['/projects/wind_uq/lcheung/amrwind-frontend/',
                 '/ccs/proj/cfd162/lcheung/amrwind-frontend/']
import sys, os, shutil
for x in amrwindfedirs: sys.path.insert(1, x)

# Important header information                                                                                                                                                                                     
# Load the libraries                                                                                                                                                                                               
import numpy             as np
import postproamrwindsample_xarray as ppsamplexr


# Run through and average
rundir       = '/lustre/orion/cfd162/proj-shared/lcheung/AWAKEN/Neutral/5kmX5km_turbine1/post_processing/'
timerange    = [20886.5, 20886.5+600]
varnames     = ['velocityx','velocityy','velocityz', 'tke']

# Get the means of the plane
ncfile  = 'sampling_41000.nc'
outfile = 'sampling_avg.pkl'
ds      = ppsamplexr.ReynoldsStress_PlaneXR(rundir+'/'+ncfile, timerange, varnames=varnames,
                                            savepklfile=outfile,
                                            verbose=True, includeattr=True)

ncfile  = 'turbhh_41000.nc'
outfile = 'turbhh_avg.pkl'
ds      = ppsamplexr.ReynoldsStress_PlaneXR(rundir+'/'+ncfile, timerange, varnames=varnames,
                                            savepklfile=outfile,
                                            verbose=True, includeattr=True)

ncfile  = 'turbsw_41000.nc'
outfile = 'turbsw_avg.pkl'
ds      = ppsamplexr.ReynoldsStress_PlaneXR(rundir+'/'+ncfile, timerange, varnames=varnames,
                                            savepklfile=outfile,
                                            verbose=True, includeattr=True)

ncfile  = 'turbswA_41000.nc'
outfile = 'turbswA_avg.pkl'
ds      = ppsamplexr.ReynoldsStress_PlaneXR(rundir+'/'+ncfile, timerange, varnames=varnames,
                                            savepklfile=outfile,
                                            verbose=True, includeattr=True)

ncfile  = 'turbswB_41000.nc'
outfile = 'turbswB_avg.pkl'
ds      = ppsamplexr.ReynoldsStress_PlaneXR(rundir+'/'+ncfile, timerange, varnames=varnames,
                                            savepklfile=outfile,
                                            verbose=True, includeattr=True)

ncfile  = 'wakesw_41000.nc'
outfile = 'wakesw_avg.pkl'
ds      = ppsamplexr.ReynoldsStress_PlaneXR(rundir+'/'+ncfile, timerange, varnames=varnames,
                                            savepklfile=outfile,
                                            verbose=True, includeattr=True)

ncfile  = 'rotor_41000.nc'
outfile = 'rotor_avg.pkl'
ds      = ppsamplexr.ReynoldsStress_PlaneXR(rundir+'/'+ncfile, timerange, varnames=varnames,
                                            savepklfile=outfile,
                                            verbose=True, includeattr=True)
