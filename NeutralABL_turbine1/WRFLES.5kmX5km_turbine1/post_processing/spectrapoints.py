def probelocations(s=1):
    import numpy as np
    ds = 20
    startx = np.arange(5,200,ds)
    starty = np.arange(110,200,ds)[::s]
    startp = []
    yoffset=0
    iplane = 1
    [[startp.append([x,y+yoffset*iy,0]) for x in startx] for iy, y in enumerate(starty)]
    return startp