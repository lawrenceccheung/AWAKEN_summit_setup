def getptlist():
    ipts = [0, 10, 20, 30, 40, 50]
    jpts = [0, 10, 20, 30, 40, 50]
    kpt  = 0
    ptlist = []
    for i in ipts:
        for j in jpts:
            ptlist.append((kpt, j, i))
    return ptlist

def formatplot(fig, ax):
    ax.set_ylim([1E-5, 1E-2])
    ax.grid(ls=':')
    return

def probelocations(s=1):
    import numpy as np
    ds = 10
    startx = np.arange(100,300,ds)
    starty = np.arange(100,300,ds)[::s]
    startp = []
    yoffset=0
    [[startp.append([x,y+yoffset*iy,0]) for x in startx] for iy, y in enumerate(starty)]
    return startp