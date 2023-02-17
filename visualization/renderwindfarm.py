# trace generated using paraview version 5.11.0
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

import argparse
import ruamel.yaml as yaml
try:
    yaml = yaml.YAML()
except:
    print('Cannot do yaml=yaml.YAML()')
    pass
        

# Helper functions to get defaults from a dictionary
getdictval = lambda d, k, default: default[k] if k not in d else d[k]

def deleteall():
    """
    Delete all objects in paraview
    """
    for x in GetSources().values(): 
        Delete(x[0])
    return

# =====================================
def plotTurbine(turbname, turbstl, xpos, ypos, zpos, yaw, azimuth=0.0, yawoffset=270.0):
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

    newyaw = yawoffset - yaw #360.0 - yaw

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
        #print(turbspec)
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

def getClipPlane(name, targetplane, origin, normal):
    kPHHplane = FindSource(targetplane)
    # create a new 'Clip'
    clip1 = Clip(registrationName=name, Input=kPHHplane)
    clip1.ClipType = 'Plane'
    clip1.HyperTreeGridClipper = 'Plane'
    clip1.Scalars = [None, '']
    # init the 'Plane' selected for 'ClipType'
    clip1.ClipType.Origin = origin
    # init the 'Plane' selected for 'HyperTreeGridClipper'
    clip1.HyperTreeGridClipper.Origin = origin
    # Properties modified on clip1
    clip1.Scalars = ['POINTS', '']
    # Properties modified on clip1.ClipType
    clip1.ClipType.Normal = normal

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # show data in view
    clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')

    # get color transfer function/color map for 'velocity'
    velocityLUT = GetColorTransferFunction('velocity')

    # get opacity transfer function/opacity map for 'velocity'
    velocityPWF = GetOpacityTransferFunction('velocity')

    # trace defaults for the display properties.
    clip1Display.Representation = 'Surface'
    clip1Display.ColorArrayName = ['POINTS', 'velocity']
    clip1Display.LookupTable = velocityLUT
    clip1Display.SelectTCoordArray = 'None'
    clip1Display.SelectNormalArray = 'None'
    clip1Display.SelectTangentArray = 'None'
    clip1Display.OSPRayScaleArray = 'velocity'
    clip1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    clip1Display.SelectOrientationVectors = 'None'
    clip1Display.ScaleFactor = 102.80000000000001
    clip1Display.SelectScaleArray = 'None'
    clip1Display.GlyphType = 'Arrow'
    clip1Display.GlyphTableIndexArray = 'None'
    clip1Display.GaussianRadius = 5.14
    clip1Display.SetScaleArray = ['POINTS', 'velocity']
    clip1Display.ScaleTransferFunction = 'PiecewiseFunction'
    clip1Display.OpacityArray = ['POINTS', 'velocity']
    clip1Display.OpacityTransferFunction = 'PiecewiseFunction'
    clip1Display.DataAxesGrid = 'GridAxesRepresentation'
    clip1Display.PolarAxes = 'PolarAxesRepresentation'
    clip1Display.ScalarOpacityFunction = velocityPWF
    clip1Display.ScalarOpacityUnitDistance = 79.60793272669744
    clip1Display.OpacityArrayName = ['POINTS', 'velocity']
    clip1Display.SelectInputVectors = ['POINTS', 'velocity']
    clip1Display.WriteLog = ''
    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    clip1Display.ScaleTransferFunction.Points = [-3.67132568359375, 0.0, 0.5, 0.0, 3.2155568599700928, 1.0, 0.5, 0.0]
    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    clip1Display.OpacityTransferFunction.Points = [-3.67132568359375, 0.0, 0.5, 0.0, 3.2155568599700928, 1.0, 0.5, 0.0]
    
    # set active source
    SetActiveSource(FindSource(targetplane))

def plotSamplePlane(name, filename, clipopt={}):
    if not isinstance(filename, list):
        filenamelist = [filename]
    else:
        filenamelist = filename
    # create a new 'Legacy VTK Reader'
    sampleplane = LegacyVTKReader(registrationName=name, FileNames=filenamelist)

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # show data in view
    sampleplaneDisplay = Show(sampleplane, renderView1, 'StructuredGridRepresentation')

    # trace defaults for the display properties.
    sampleplaneDisplay.Representation = 'Surface'
    sampleplaneDisplay.ColorArrayName = [None, '']
    sampleplaneDisplay.SelectTCoordArray = 'None'
    sampleplaneDisplay.SelectNormalArray = 'None'
    sampleplaneDisplay.SelectTangentArray = 'None'
    sampleplaneDisplay.OSPRayScaleArray = 'velocity'
    sampleplaneDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    sampleplaneDisplay.SelectOrientationVectors = 'None'
    sampleplaneDisplay.ScaleFactor = 202.0
    sampleplaneDisplay.SelectScaleArray = 'None'
    sampleplaneDisplay.GlyphType = 'Arrow'
    sampleplaneDisplay.GlyphTableIndexArray = 'None'
    sampleplaneDisplay.GaussianRadius = 10.1
    sampleplaneDisplay.SetScaleArray = ['POINTS', 'velocity']
    sampleplaneDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    sampleplaneDisplay.OpacityArray = ['POINTS', 'velocity']
    sampleplaneDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    sampleplaneDisplay.DataAxesGrid = 'GridAxesRepresentation'
    sampleplaneDisplay.PolarAxes = 'PolarAxesRepresentation'
    sampleplaneDisplay.ScalarOpacityUnitDistance = 124.39538251074127
    sampleplaneDisplay.SelectInputVectors = ['POINTS', 'velocity']
    sampleplaneDisplay.WriteLog = ''

    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    sampleplaneDisplay.ScaleTransferFunction.Points = [-3.6802566051483154, 0.0, 0.5, 0.0, 2.4374403953552246, 1.0, 0.5, 0.0]

    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    sampleplaneDisplay.OpacityTransferFunction.Points = [-3.6802566051483154, 0.0, 0.5, 0.0, 2.4374403953552246, 1.0, 0.5, 0.0]

    # reset view to fit data
    renderView1.ResetCamera(False)
    # get the material library
    materialLibrary1 = GetMaterialLibrary()
    # update the view to ensure updated data information
    renderView1.Update()
    # set scalar coloring
    ColorBy(sampleplaneDisplay, ('POINTS', 'velocity', 'Magnitude'))
    # rescale color and/or opacity maps used to include current data range
    sampleplaneDisplay.RescaleTransferFunctionToDataRange(True, False)
    # show color bar/color legend
    sampleplaneDisplay.SetScalarBarVisibility(renderView1, True)    
    # get color transfer function/color map for 'velocity'
    velocityLUT = GetColorTransferFunction('velocity')
    # get opacity transfer function/opacity map for 'velocity'
    velocityPWF = GetOpacityTransferFunction('velocity')
    # get 2D transfer function for 'velocity'
    velocityTF2D = GetTransferFunction2D('velocity')

    # Handle any clip planes
    if bool(clipopt):
        normal    = clipopt['normal']
        origin    = clipopt['origin']
        clipname  = clipopt['name']
        targetname = name
        getClipPlane(clipname, targetname, origin, normal)
        # hide data in view
        Hide(sampleplane, renderView1)

    return sampleplane, sampleplaneDisplay

def plotSamplePlaneList(planedict):
    defaults = planedict['defaults']  if 'defaults' in planedict else {}
    for planespec in planedict['sampleplanelist']:
        #print(planespec)
        name   = planespec['name']
        files  = planespec['files']
        if 'clip' in planespec:
            clipopt = planespec['clip']
        else:
            clipopt = {}
        plotSamplePlane(name, files, clipopt=clipopt)

# =====================================
def runCommands(execdict):
    if 'execstring' in execdict:
        exec(execdict['execstring'])
    return

# =====================================
def saveoutput(outputdict):
    if 'filename' in outputdict:
        filename = outputdict['filename']
        imagesize = outputdict['imagesize']
        SaveScreenshot(filename,ImageResolution=imagesize)
    if 'savestate' in outputdict:
        SaveState(outputdict['savestate'])
    return

# =====================================
def processyamlinput(yamlfile, verbose=False):
    # Load the yaml input file
    with open(yamlfile) as fp:
        Loader = yaml.load
        yamldict = Loader(fp)
        # Plot the turbines
        if 'turbines' in yamldict:
            if verbose: print("Loading turbines")
            plotTurbineList(yamldict['turbines'])
        if 'solidplanes' in yamldict:
            if verbose: print("Loading solid planes")
            plotPlaneList(yamldict['solidplanes'])
        if 'sampleplanes' in yamldict:
            if verbose: print("Loading sample planes")
            plotSamplePlaneList(yamldict['sampleplanes'])
        if 'runcommands' in yamldict:
            if verbose: print("running commands")
            runCommands(yamldict['runcommands'])
        if 'output' in yamldict:
            if verbose: print("saving output")
            saveoutput(yamldict['output'])
        if verbose: print("Done")
    return

# =====================================

if __name__ == "__main__":
    title="Render wind farm scene"
    parser = argparse.ArgumentParser(description=title)
    parser.add_argument('inputfile')
    parser.add_argument('-v', '--verbose', 
                        help="Verbose output",
                        default=False,
                        action='store_true')
    # Load the options
    args      = parser.parse_args()
    inputfile = args.inputfile
    verbose   = args.verbose

    processyamlinput(inputfile, verbose=verbose)
