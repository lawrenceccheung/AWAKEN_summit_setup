#!/usr/bin/env python
#


# Load the libraries
import matplotlib.pyplot as plt
import postproamrwindsample as ppsample
import numpy             as np
from matplotlib import cm
import re
import pickle
import os, sys

# Also ignore warnings
import warnings
warnings.filterwarnings('ignore')

# See https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def progress(count, total, suffix=''):
    """
    print out a progressbar
    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()

def getPlaneSampleVarAtTime(ncdat, group, var, itime, kplane):
    Nijk    = ncdat[group].ijk_dims
    allpts  = ncdat[group].variables['coordinates']
    vardat  = ncdat[group].variables[var]
    axis1   = ncdat[group].axis1
    axis2   = ncdat[group].axis2

    N1      = Nijk[0]
    N2      = Nijk[1]
    vmesh   = np.zeros((N1,N2))
    totalN  = N1*N2

    for j in range(N2):
        for i in range(N1):
            progress(i + j*N1, totalN)
            ipt = i + j*N1 + kplane*N1*N2
            v   = vardat[itime, ipt]
            vmesh[i,j] = v
    return vmesh

def getPlaneGrid(ncdat, group, itime, kplane):
    Nijk    = ncdat[group].ijk_dims
    allpts  = ncdat[group].variables['coordinates']
    #vardat  = ncdat[group].variables[var]
    axis1   = ncdat[group].axis1
    axis2   = ncdat[group].axis2

    N1      = Nijk[0]
    N2      = Nijk[1]
    xmesh   = np.zeros((N1,N2))
    ymesh   = np.zeros((N1,N2))
    zmesh   = np.zeros((N1,N2))
    #vmesh   = np.zeros((N1,N2))

    # Set up the s directions
    ds1     = np.linalg.norm(axis1)/(N1-1)
    ds2     = np.linalg.norm(axis2)/(N2-1)
    s1mesh  = np.zeros((N1,N2))
    s2mesh  = np.zeros((N1,N2))

    totalN  = N1*N2

    for j in range(N2):
        for i in range(N1):
            progress(i + j*N1, totalN)
            ipt = i + j*N1 + kplane*N1*N2
            x   = allpts[ipt,0]
            y   = allpts[ipt,1]
            z   = allpts[ipt,2]
            #v   = vardat[itime, ipt]
            xmesh[i,j] = x
            ymesh[i,j] = y
            zmesh[i,j] = z
            #vmesh[i,j] = v

            s1  = i*ds1
            s2  = j*ds2
            s1mesh[i,j] = s1
            s2mesh[i,j] = s2
    return xmesh, ymesh, zmesh, s1mesh, s2mesh

def loadSaveVelPickleOld(ncdat, group, itime, kplane, picklefname,
                      vvars=['velocityx', 'velocityy']):
    time = np.array(ncdat['time'])[itime]
    print('Time = '+repr(time))
    x,y,z,s1,s2,vx = ppsample.getPlaneSampleAtTime(ncdat, group, vvars[0],
                                                   itime, kplane)
    x,y,z,s1,s2,vy = ppsample.getPlaneSampleAtTime(ncdat, group, vvars[1],
                                                   itime, kplane)
    db = {}
    db['x'] = x
    db['y'] = y
    db['z'] = z
    db['vx'] = vx
    db['vy'] = vy
    db['time'] = time
    dbfile = open(picklefname, 'wb')
    pickle.dump(db, dbfile, protocol=2)
    dbfile.close()
    print("Saved "+picklefname)
    return x, y, z, vx, vy, time

def loadSaveVelPickle(ncdat, group, itime, kplane, picklefname,
                      vvars=['velocityx', 'velocityy']):
    time = np.array(ncdat['time'])[itime]
    print('Time = '+repr(time))
    x,y,z,s1,s2 = getPlaneGrid(ncdat, group, itime, kplane)
    print("\nLoading "+vvars[0])
    vx = getPlaneSampleVarAtTime(ncdat, group, vvars[0], itime, kplane)
    print("\nLoading "+vvars[1])
    vy = getPlaneSampleVarAtTime(ncdat, group, vvars[1], itime, kplane)
    #x,y,z,s1,s2,vx = getPlaneSampleAtTime2(ncdat, group, vvars[0],
    #                                       itime, kplane)
    #x,y,z,s1,s2,vy = getPlaneSampleAtTime2(ncdat, group, vvars[1],
    #                                       itime, kplane)
    db = {}
    db['x'] = x
    db['y'] = y
    db['z'] = z
    db['vx'] = vx
    db['vy'] = vy
    db['time'] = time
    dbfile = open(picklefname, 'wb')
    pickle.dump(db, dbfile, protocol=2)
    dbfile.close()
    print("\nSaved "+picklefname)
    return x, y, z, vx, vy, time

def loadPickle(picklefname):
    pfile = open(picklefname, 'rb')
    db   = pickle.load(pfile)
    x    = db['x']
    y    = db['y']
    z    = db['z']
    vx   = db['vx']
    vy   = db['vy']
    time = db['time']
    pfile.close()
    return x, y, z, vx, vy, time

def plotVh(x, y, vx, vy, itime, fname, time):
    vh = np.sqrt(vx**2 + vy**2)
    clevels=np.linspace(6,12,81)
    plt.figure(figsize=(6,5), dpi=125)
    plt.contourf(x, y, vh, clevels, cmap='coolwarm')
    plt.colorbar()
    plt.axis('scaled')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title('horizontal U, t=%0.1f, z=90m'%(time))
    plt.tight_layout()
    plt.savefig(fname)

