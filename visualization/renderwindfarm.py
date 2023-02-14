# trace generated using paraview version 5.11.0
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

import ruamel.yaml as yaml
try:
    yaml = yaml.YAML()
except:
    print('Cannot do yaml=yaml.YAML()')
    pass
        

# Helper functions to get defaults from a dictionary
getdictval = lambda d, k, default: default[k] if k not in d else d[k]

# =====================================
def plotTurbine(turbname, turbstl, xpos, ypos, zpos, yaw, azimuth=0.0):
    """
    Plot a turbine from an stl file in turbstl
    """
    # create a new 'STL Reader'
    turbinestl = STLReader(registrationName=turbname, FileNames=[turbstl])

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    
    # show data in view
    turbinestlDisplay = Show(turbinestl, renderView1, 'GeometryRepresentation')

    # trace defaults for the display properties.
    turbinestlDisplay.Representation = 'Surface'
    turbinestlDisplay.ColorArrayName = [None, '']
    turbinestlDisplay.SelectTCoordArray = 'None'
    turbinestlDisplay.SelectNormalArray = 'None'
    turbinestlDisplay.SelectTangentArray = 'None'
    turbinestlDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    turbinestlDisplay.SelectOrientationVectors = 'None'
    turbinestlDisplay.ScaleFactor = 10.92962226867676
    turbinestlDisplay.SelectScaleArray = 'None'
    turbinestlDisplay.GlyphType = 'Arrow'
    turbinestlDisplay.GlyphTableIndexArray = 'None'
    turbinestlDisplay.GaussianRadius = 0.5464811134338379
    turbinestlDisplay.SetScaleArray = [None, '']
    turbinestlDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    turbinestlDisplay.OpacityArray = [None, '']
    turbinestlDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    turbinestlDisplay.DataAxesGrid = 'GridAxesRepresentation'
    turbinestlDisplay.PolarAxes = 'PolarAxesRepresentation'
    turbinestlDisplay.SelectInputVectors = [None, '']
    turbinestlDisplay.WriteLog = ''

    # Properties modified on turbinestlDisplay
    turbinestlDisplay.Position = [xpos, ypos, zpos]
    # Properties modified on turbinestlDisplay.DataAxesGrid
    turbinestlDisplay.DataAxesGrid.Position = [xpos, ypos, zpos]
    # Properties modified on turbinestlDisplay.PolarAxes
    turbinestlDisplay.PolarAxes.Translation = [xpos, ypos, zpos]

    newyaw = 360.0 - yaw

    # Properties modified on turbinestlDisplay
    turbinestlDisplay.Orientation = [0.0, azimuth, newyaw]
    # Properties modified on turbinestlDisplay.PolarAxes
    turbinestlDisplay.PolarAxes.Orientation = [0.0, azimuth, newyaw]
    return turbinestl, turbinestlDisplay

def plotTurbineList(turbdict):
    """
    Plot a list of turbines from the dict in turbdict
    """
    defaults = turbdict['defaults']  if 'defaults' in turbdict else {}
    for turbspec in turbdict['turbinelist']:
        print(turbspec)
        turbname = turbspec['name']
        turbfile = getdictval(turbspec, 'turbfile', defaults)
        azimuth  = getdictval(turbspec, 'azimuth', defaults)
        pos      = turbspec['pos']
        xpos     = pos[0]
        ypos     = pos[1]
        zpos     = defaults['hubheight'] if len(pos)<3 else pos[2]
        yaw      = getdictval(turbspec, 'yaw', defaults)
        turbstl, turbstlDisplay = plotTurbine(turbname, turbfile, 
                                              xpos, ypos, zpos, yaw, 
                                              azimuth=azimuth)
    return

# =====================================
def plotPlane(name, origin, p1, p2, 
              xres=10, yres=10, color=[0.0, 0.0, 0.0]):

    # create a new 'Plane'
    plane1             = Plane(registrationName=name)
    # Properties modified on plane1
    plane1.Origin      = origin
    plane1.Point1      = p1
    plane1.Point2      = p2
    plane1.XResolution = xres
    plane1.YResolution = yres

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # show data in view
    plane1Display = Show(plane1, renderView1, 'GeometryRepresentation')

    # trace defaults for the display properties.
    plane1Display.Representation = 'Surface'
    plane1Display.ColorArrayName = [None, '']
    plane1Display.SelectTCoordArray = 'TextureCoordinates'
    plane1Display.SelectNormalArray = 'Normals'
    plane1Display.SelectTangentArray = 'None'
    plane1Display.OSPRayScaleArray = 'Normals'
    plane1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    plane1Display.SelectOrientationVectors = 'None'
    plane1Display.ScaleFactor = 10.0
    plane1Display.SelectScaleArray = 'None'
    plane1Display.GlyphType = 'Arrow'
    plane1Display.GlyphTableIndexArray = 'None'
    plane1Display.GaussianRadius = 0.5
    plane1Display.SetScaleArray = ['POINTS', 'Normals']
    plane1Display.ScaleTransferFunction = 'PiecewiseFunction'
    plane1Display.OpacityArray = ['POINTS', 'Normals']
    plane1Display.OpacityTransferFunction = 'PiecewiseFunction'
    plane1Display.DataAxesGrid = 'GridAxesRepresentation'
    plane1Display.PolarAxes = 'PolarAxesRepresentation'
    plane1Display.SelectInputVectors = ['POINTS', 'Normals']
    plane1Display.WriteLog = ''

    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    plane1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]
    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    plane1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]


    # change solid color
    plane1Display.AmbientColor = color
    plane1Display.DiffuseColor = color

def plotPlaneList(planedict):
    defaults = planedict['defaults']  if 'defaults' in planedict else {}
    for planespec in planedict['planelist']:
        name   = planespec['name']
        origin = planespec['origin']
        p1     = planespec['p1']
        p2     = planespec['p2']
        color  = getdictval(planespec, 'color', defaults)        
        plotPlane(name, origin, p1, p2, color=color)

# =====================================
configyaml='config.yaml'

# Load the yaml input file
with open(configyaml) as fp:
    Loader = yaml.load
    yamldict = Loader(fp)
    #print(yamldict)
    # Plot the turbines
    if 'turbines' in yamldict:
        plotTurbineList(yamldict['turbines'])
    if 'solidplanes' in yamldict:
        plotPlaneList(yamldict['solidplanes'])
