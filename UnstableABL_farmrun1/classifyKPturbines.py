import numpy             as np
import math
import pandas as pd
import os

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

def getTurbSubsetXY(csvfile, suffix, xlim=[-np.finfo(np.float64).max, np.finfo(np.float64).max], ylim=[-np.finfo(np.float64).max, np.finfo(np.float64).max]):
    # Load the data from the database of all turbines
    allturbsdf = pd.read_csv(csvfile, low_memory=False)
    # Get just the King Plains turbines
    subset = [] 
    for x in allturbsdf.iterrows():
        xy = [float(x[1][' x']), float(x[1][' y'])]
        if x[1]['# name'].endswith(suffix) and ((xlim[0] <= xy[0]) and (xy[0]<=xlim[1]) and (ylim[0]<=xy[1]) and (xy[1]<=ylim[1])):
            #print(x[1])
            subset.append(x[1])
    subsetdf = pd.DataFrame(subset[:])
    return subsetdf

getturbnames = lambda df: [x[1]['# name'] for x in df.iterrows()]

def getTurbCategoryList(csvfile, suffix, limitdict):
    allturbs = []
    for box in limitdict['bboxes']:
        turbinbox = getturbnames(getTurbSubsetXY(csvfile, suffix, xlim=box[0], ylim=box[1]))
        allturbs += turbinbox
    return allturbs

frontrow = {'label':'frontrow',
            'bboxes':[[[640000, 650000], [4025000, 4026500]],
                      [[638500, 640000], [4026000, 4027500]],
                      [[634900, 638500], [4027500, 4028500]],
                     ],
            'plotargs':{'facecolor':'b', 'alpha':0.5}, #{'linewidth':1, 'edgecolor':'r', 'facecolor':'none'}
           }

AFwaked  = {'label':'AFwaked',
            'bboxes':[
                      [[633000, 634900], [4027500, 4028500]],
                      [[630000, 633000], [4029000, 4029900]],
                     ],
            'plotargs':{'facecolor':'pink', 'alpha':0.75}, #{'linewidth':1, 'edgecolor':'r', 'facecolor':'none'}
           }

midrow   = {'label':'midrow',
            'bboxes':[[[640000, 650000], [4026600, 4029500]],
                      [[637500, 640000], [4028500, 4029500]],
                      [[633000, 637500], [4028500, 4030500]],
                      [[630000, 633000], [4029900, 4031500]],
                     ],
            'plotargs':{'facecolor':'lightblue', 'alpha':0.5}, #{'linewidth':1, 'edgecolor':'r', 'facecolor':'none'}
           }

backrow  = {'label':'backrow',
            'bboxes':[[[637500, 650000], [4029500, 4032500]],
                      [[633500, 637500], [4030500, 4032500]],
                      [[631000, 633500], [4031500, 4033500]],
                     ],
            'plotargs':{'facecolor':'cyan', 'alpha':0.5}, #{'linewidth':1, 'edgecolor':'r', 'facecolor':'none'}
           }

allcategories = [frontrow,
                 AFwaked,
                 midrow,
                 backrow,
                ]

turbinecategorylist = {}


scriptdir    = os.path.dirname(os.path.abspath(__file__))
summitcsv    = 'UnstableABL_farmrun_turbines.csv'

allturbines = turblist = getturbnames(getTurbSubset(scriptdir+'/'+summitcsv, '-KP'))

for d in allcategories:
    turblist = getTurbCategoryList(scriptdir+'/'+summitcsv, '-KP', d)
    d['turblist'] = turblist
    turbinecategorylist[d['label']] = turblist