# trace generated using paraview version 5.11.0
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

import sys
import argparse
import numpy as np
import json

try:
    import ruamel.yaml as yaml
    yaml = yaml.YAML()
    yamlokay = True
    print('loaded ruamel.yaml')
except:
    yamlokay = False
    print('no loaded yaml')

# import ruamel.yaml as yaml
# try:
#    yaml = yaml.YAML()
# except:
#    print('Cannot do yaml=yaml.YAML()')
#    pass
        

# Helper functions to get defaults from a dictionary
getdictval = lambda d, k, default: default[k] if k not in d else d[k]

def deleteall():
    """
    Delete all objects in paraview
    """
    for x in GetSources().values(): 
        Delete(x[0])
    RenderAllViews()
    return

# =====================================
def plotTower(towername, xpos, ypos, towerheight, yaw, 
              yawoffset=270.0, radius=1.5, nacelleL=10):
    hubspacing=1.5
    # create a new 'Cylinder'
    cylinder1 = Cylinder(registrationName=towername)

    # Properties modified on cylinder1
    cylinder1.Resolution = 12
    cylinder1.Height = towerheight
    cylinder1.Radius = radius

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    
    # show data in view
    cylinder1Display = Show(cylinder1, renderView1, 'GeometryRepresentation')

    # trace defaults for the display properties.
    cylinder1Display.Representation = 'Surface'
    cylinder1Display.ColorArrayName = [None, '']
    cylinder1Display.SelectTCoordArray = 'TCoords'
    cylinder1Display.SelectNormalArray = 'Normals'
    cylinder1Display.SelectTangentArray = 'None'
    cylinder1Display.OSPRayScaleArray = 'Normals'
    cylinder1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    cylinder1Display.SelectOrientationVectors = 'None'
    cylinder1Display.SelectScaleArray = 'None'
    cylinder1Display.GlyphType = 'Arrow'
    cylinder1Display.GlyphTableIndexArray = 'None'
    cylinder1Display.GaussianRadius = 0.05
    cylinder1Display.SetScaleArray = ['POINTS', 'Normals']
    cylinder1Display.ScaleTransferFunction = 'PiecewiseFunction'
    cylinder1Display.OpacityArray = ['POINTS', 'Normals']
    cylinder1Display.OpacityTransferFunction = 'PiecewiseFunction'
    cylinder1Display.DataAxesGrid = 'GridAxesRepresentation'
    cylinder1Display.PolarAxes = 'PolarAxesRepresentation'
    cylinder1Display.SelectInputVectors = ['POINTS', 'Normals']
    cylinder1Display.WriteLog = ''
    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    cylinder1Display.ScaleTransferFunction.Points = [-1.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    cylinder1Display.OpacityTransferFunction.Points = [-1.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
    newyaw = yawoffset - yaw 
    windvec = np.array([np.cos(newyaw*np.pi/180.0), 
                        np.sin(newyaw*np.pi/180.0), 
                        0.0])
    toweroffset = (0.5*nacelleL + hubspacing)*windvec
    towercenter = [xpos + toweroffset[0], 
                   ypos + toweroffset[1],
                   0.5*towerheight + toweroffset[2]]
    # Properties modified on turbinestlDisplay
    #cylinder1Display.Position = towercenter
    cylinder1Display.Translation = towercenter
    # Properties modified on turbinestlDisplay.DataAxesGrid
    cylinder1Display.DataAxesGrid.Position = towercenter
    # Properties modified on turbinestlDisplay.PolarAxes
    cylinder1Display.PolarAxes.Translation = towercenter
    # Properties modified on box1Display
    cylinder1Display.Orientation = [90.0, 0.0, newyaw]
    # Properties modified on box1Display.PolarAxes
    cylinder1Display.PolarAxes.Orientation = [90.0, 0.0, newyaw]   
    return

def plotNacelle(nacellename, xpos, ypos, zpos, yaw, 
                yawoffset=270.0, L=10, W=8, H=8):
    hubspacing = 1.5
    # create a new 'Box'
    box1 = Box(registrationName=nacellename)
    
    # Properties modified on box1
    box1.XLength = L
    box1.YLength = W
    box1.ZLength = H
    box1.Center = [0.0, 0.0, 0.0]
    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    # show data in view
    box1Display = Show(box1, renderView1, 'GeometryRepresentation')
    # trace defaults for the display properties.
    box1Display.Representation = 'Surface'
    box1Display.ColorArrayName = [None, '']
    box1Display.SelectTCoordArray = 'TCoords'
    box1Display.SelectNormalArray = 'Normals'
    box1Display.SelectTangentArray = 'None'
    box1Display.OSPRayScaleArray = 'Normals'
    box1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    box1Display.SelectOrientationVectors = 'None'
    box1Display.ScaleFactor = 0.30000000000000004
    box1Display.SelectScaleArray = 'None'
    box1Display.GlyphType = 'Arrow'
    box1Display.GlyphTableIndexArray = 'None'
    box1Display.GaussianRadius = 0.015
    box1Display.SetScaleArray = ['POINTS', 'Normals']
    box1Display.ScaleTransferFunction = 'PiecewiseFunction'
    box1Display.OpacityArray = ['POINTS', 'Normals']
    box1Display.OpacityTransferFunction = 'PiecewiseFunction'
    box1Display.DataAxesGrid = 'GridAxesRepresentation'
    box1Display.PolarAxes = 'PolarAxesRepresentation'
    box1Display.SelectInputVectors = ['POINTS', 'Normals']
    box1Display.WriteLog = ''
    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    box1Display.ScaleTransferFunction.Points = [-1.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]

    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    box1Display.OpacityTransferFunction.Points = [-1.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]

    newyaw = yawoffset - yaw 
    windvec = np.array([np.cos(newyaw*np.pi/180.0), 
                        np.sin(newyaw*np.pi/180.0), 
                        0.0])
    nacelleoffset = (0.5*L + hubspacing)*windvec
    nacellecenter = [xpos + nacelleoffset[0], 
                     ypos + nacelleoffset[1],
                     zpos + nacelleoffset[2]]
    # Properties modified on turbinestlDisplay
    #box1Display.Position = nacellecenter
    box1Display.Translation = nacellecenter
    # Properties modified on turbinestlDisplay.DataAxesGrid
    box1Display.DataAxesGrid.Position = nacellecenter
    # Properties modified on turbinestlDisplay.PolarAxes
    box1Display.PolarAxes.Translation = nacellecenter

    # Properties modified on box1Display
    box1Display.Origin = [0.0, 0.0, 0.0]

    # Properties modified on box1Display
    box1Display.Orientation = [0.0, 0.0, newyaw]
    # Properties modified on box1Display.PolarAxes
    box1Display.PolarAxes.Orientation = [0.0, 0.0, newyaw]   
    return

def plotTurbine(turbname, turbstl, xpos, ypos, zpos, yaw, 
                azimuth=0.0, 
                yawoffset=270.0,
                scale=[1.0, 1.0, 1.0], origin=[0.0, 0.0, 0.0], colordict=None,
                drawnacelle=True, drawtower=True):
    """
    Plot a turbine from an stl file in turbstl
    """
    # create a new 'STL Reader'
    if turbstl.lower().endswith('.iges') or turbstl.lower().endswith('.igs'):
        turbinestl = IGESReader(registrationName=turbname, FileNames=[turbstl])
        turbinestl.LinearDeflection = 1.0
        turbinestl.AngularDeflection = 2.0
    elif turbstl.lower().endswith('.obj'):
        turbinestl = WavefrontOBJReader(registrationName=turbname, FileName=turbstl)
    else:
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

    turbinestlDisplay.Scale = scale
    turbinestlDisplay.Origin = origin
    
    # Properties modified on turbinestlDisplay
    #turbinestlDisplay.Position = [xpos, ypos, zpos]
    turbinestlDisplay.Translation = [xpos, ypos, zpos]
    # Properties modified on turbinestlDisplay.DataAxesGrid
    turbinestlDisplay.DataAxesGrid.Position = [xpos, ypos, zpos]
    # Properties modified on turbinestlDisplay.PolarAxes
    turbinestlDisplay.PolarAxes.Translation = [xpos, ypos, zpos]

    newyaw = yawoffset - yaw #360.0 - yaw

    if colordict is not None:
        turbinestlDisplay.Set(
            AmbientColor=colordict['AmbientColor'],
            DiffuseColor=colordict['DiffuseColor'],
        )
    
    # Properties modified on turbinestlDisplay
    turbinestlDisplay.Orientation = [azimuth, 0.0, newyaw] #[0.0, azimuth, newyaw]
    # Properties modified on turbinestlDisplay.PolarAxes
    turbinestlDisplay.PolarAxes.Orientation = [azimuth, 0.0, newyaw] #[0.0, azimuth, newyaw]
    if drawnacelle:
        nacellename = turbname + "_nacelle"
        plotNacelle(nacellename, xpos, ypos, zpos, yaw, 
                    yawoffset=yawoffset, L=10, W=5, H=5)
    if drawtower:
        towername = turbname + "_tower"
        plotTower(towername, xpos, ypos, zpos, yaw, yawoffset=270.0, 
                  radius=1.5, nacelleL=10)

    return turbinestl, turbinestlDisplay

def plotTurbineList(turbdict, verbose=True):
    """
    Plot a list of turbines from the dict in turbdict
    """
    defaults = {'turbfile':'', 'azimuth':0.0, 'yaw':0.0,
                'scale':[1.0, 1.0, 1.0], 'origin':[0.0, 0.0, 0.0],
                'colordict':None,
                'drawnacelle':True, 'drawtower':True}
    if 'defaults' in turbdict: defaults.update(turbdict['defaults'])

    for iturb, turbspec in enumerate(turbdict['turbinelist']):
        if verbose:
            print(" turbine [%i/%i]"%(iturb+1, 
                                    len(turbdict['turbinelist'])))
            sys.stdout.flush()
        turbname = turbspec['name']
        turbfile = getdictval(turbspec, 'turbfile', defaults)
        azimuth  = getdictval(turbspec, 'azimuth', defaults)
        pos      = turbspec['pos']
        xpos     = pos[0]
        ypos     = pos[1]
        zpos     = defaults['hubheight'] if len(pos)<3 else pos[2]
        yaw      = getdictval(turbspec, 'yaw', defaults)
        scale    = getdictval(turbspec, 'scale', defaults)
        origin   = getdictval(turbspec, 'origin', defaults)
        colordict= getdictval(turbspec, 'colordict', defaults)
        drawtower= getdictval(turbspec, 'drawtower', defaults)
        drawnacelle= getdictval(turbspec, 'drawnacelle', defaults)
        turbstl, turbstlDisplay = plotTurbine(turbname, turbfile, 
                                              xpos, ypos, zpos, yaw,
                                              scale=scale,
                                              origin=origin,
                                              colordict=colordict,
                                              azimuth=azimuth, 
                                              drawnacelle=drawnacelle,
                                              drawtower=drawtower)
    return

# =====================================
def plotPlane(name, origin, p1, p2, 
              xres=10, yres=10, color=[0.0, 0.0, 0.0], 
              representation='Surface', texture=None):

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
    plane1Display.Representation = representation #'Surface'
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

    if texture is not None:
        print('Apply texture '+texture+' DOES NOT WORK IN PARAVIEW 5.13.1')
        textureimage = FindTextureOrCreate(registrationName=name+'_texture',
                                           filename=texture)
        plane1Display.Texture = textureimage
    else:
        # change solid color
        plane1Display.AmbientColor = color
        plane1Display.DiffuseColor = color

    return

def plotPlaneList(planedict):
    defaultdict = {'color':[0.0, 0.0, 0.0], 'representation':'Surface', 'texture':None}
    defaults = planedict['defaults']  if 'defaults' in planedict else defaultdict
    for k,g in defaultdict.items():
        if k not in defaults: defaults[k] = defaultdict[k]
        
    for planespec in planedict['planelist']:
        name   = planespec['name']
        origin = planespec['origin']
        p1     = planespec['p1']
        p2     = planespec['p2']
        color  = getdictval(planespec, 'color', defaults)
        texture         = getdictval(planespec, 'texture', defaults)
        representation  = getdictval(planespec, 'representation', defaults)
        plotPlane(name, origin, p1, p2, color=color, 
                  representation=representation,
                  texture=texture)

# =====================================

def getClipPlane(name, targetplane, origin, normal, displayprop=None):
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

    if displayprop:
        for k,g in displayprop.items():
            exestr = 'clip1Display.%s = %s\n'%(k, repr(g))
            exec(exestr)
    
    # set active source
    SetActiveSource(FindSource(targetplane))

def plotSamplePlane(name, filename, clipopt={}, displayprop={}):
    if not isinstance(filename, list):
        filenamelist = [filename]
    else:
        filenamelist = filename
    # create a new 'Legacy VTK Reader'
    if filenamelist[0].endswith('.shp'):
        sampleplane = GDALVectorReader(registrationName=name, FileName=filenamelist)
        plotarray = [None, '']
    else:
        sampleplane = LegacyVTKReader(registrationName=name, FileNames=filenamelist)
        plotarray = ['POINTS', 'velocity']

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
    sampleplaneDisplay.SetScaleArray = plotarray
    sampleplaneDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    sampleplaneDisplay.OpacityArray = plotarray
    sampleplaneDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    sampleplaneDisplay.DataAxesGrid = 'GridAxesRepresentation'
    sampleplaneDisplay.PolarAxes = 'PolarAxesRepresentation'
    sampleplaneDisplay.ScalarOpacityUnitDistance = 124.39538251074127
    sampleplaneDisplay.SelectInputVectors = plotarray
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
    if plotarray[1] == 'velocity':
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
    else:
        # get color transfer function/color map for 'vtkBlockColors'
        vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')
        # get opacity transfer function/opacity map for 'vtkBlockColors'
        vtkBlockColorsPWF = GetOpacityTransferFunction('vtkBlockColors')
        # get 2D transfer function for 'vtkBlockColors'
        vtkBlockColorsTF2D = GetTransferFunction2D('vtkBlockColors')
        # Hide the scalar bar for this color map if no visible data is colored by it.
        HideScalarBarIfNotNeeded(vtkBlockColorsLUT, renderView1)

    if displayprop:
        for k,g in displayprop.items():
            exestr = 'sampleplaneDisplay.%s = %s\n'%(k, repr(g))
            exec(exestr)
            

    # Handle any clip planes
    if bool(clipopt):
        normal    = clipopt['normal']
        origin    = clipopt['origin']
        clipname  = clipopt['name']
        targetname = name
        getClipPlane(clipname, targetname, origin, normal, displayprop=displayprop)
        # hide data in view
        Hide(sampleplane, renderView1)

    return sampleplane, sampleplaneDisplay

def plotSamplePlaneList(planedict, verbose=False):
    defaults = planedict['defaults']  if 'defaults' in planedict else {}
    for iplane, planespec in enumerate(planedict['sampleplanelist']):
        if verbose:
            print(" plane [%i/%i]"%(iplane+1, 
                                    len(planedict['sampleplanelist'])))
            sys.stdout.flush()
        name   = planespec['name']
        files  = planespec['files']
        if 'clip' in planespec:
            clipopt = planespec['clip']
        else:
            clipopt = {}
        if 'displayprop' in planespec:
            displayprop = planespec['displayprop']
        else:
            displayprop = {}
        plotSamplePlane(name, files, clipopt=clipopt, displayprop=displayprop)

# =====================================

def plotPolyLine(name, linesegments, 
                 color=[0.0, 0.0, 0.0], 
                 closeloop=False, makesurface=False, surfacecolor=None):
    """
    """
    # create a new 'Poly Line Source'
    polyLineSource1 = PolyLineSource(registrationName=name)

    # Build point list
    allpoints = []
    for seg in linesegments:
        allpoints = allpoints + seg
    if closeloop: allpoints = allpoints + linesegments[0]
    polyLineSource1.Points = allpoints

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # show data in view
    polyLineSource1Display = Show(polyLineSource1, renderView1, 
                                  'GeometryRepresentation')

    # trace defaults for the display properties.
    polyLineSource1Display.Representation = 'Surface'
    polyLineSource1Display.ColorArrayName = [None, '']
    polyLineSource1Display.SelectTCoordArray = 'None'
    polyLineSource1Display.SelectNormalArray = 'None'
    polyLineSource1Display.SelectTangentArray = 'None'
    polyLineSource1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    polyLineSource1Display.SelectOrientationVectors = 'None'
    polyLineSource1Display.ScaleFactor = 0.1
    polyLineSource1Display.SelectScaleArray = 'None'
    polyLineSource1Display.GlyphType = 'Arrow'
    polyLineSource1Display.GlyphTableIndexArray = 'None'
    polyLineSource1Display.GaussianRadius = 0.005
    polyLineSource1Display.SetScaleArray = [None, '']
    polyLineSource1Display.ScaleTransferFunction = 'PiecewiseFunction'
    polyLineSource1Display.OpacityArray = [None, '']
    polyLineSource1Display.OpacityTransferFunction = 'PiecewiseFunction'
    polyLineSource1Display.DataAxesGrid = 'GridAxesRepresentation'
    polyLineSource1Display.PolarAxes = 'PolarAxesRepresentation'
    polyLineSource1Display.SelectInputVectors = [None, '']
    polyLineSource1Display.WriteLog = ''

    # change solid color
    polyLineSource1Display.AmbientColor = color
    polyLineSource1Display.DiffuseColor = color
    if makesurface:
        surfcolor = color if surfacecolor is None else surfacecolor
        # find source
        rect1 = FindSource(name)
        # create a new 'Delaunay 2D'
        delaunay2D1 = Delaunay2D(registrationName=name+'_surface', Input=rect1)
        # show data in view
        delaunay2D1Display = Show(delaunay2D1, renderView1, 'GeometryRepresentation')
        # trace defaults for the display properties.
        delaunay2D1Display.Representation = 'Surface'
        delaunay2D1Display.ColorArrayName = [None, '']
        delaunay2D1Display.SelectTCoordArray = 'None'
        delaunay2D1Display.SelectNormalArray = 'None'
        delaunay2D1Display.SelectTangentArray = 'None'
        delaunay2D1Display.OSPRayScaleFunction = 'PiecewiseFunction'
        delaunay2D1Display.SelectOrientationVectors = 'None'
        delaunay2D1Display.ScaleFactor = 0.1
        delaunay2D1Display.SelectScaleArray = 'None'
        delaunay2D1Display.GlyphType = 'Arrow'
        delaunay2D1Display.GlyphTableIndexArray = 'None'
        delaunay2D1Display.GaussianRadius = 0.005
        delaunay2D1Display.SetScaleArray = [None, '']
        delaunay2D1Display.ScaleTransferFunction = 'PiecewiseFunction'
        delaunay2D1Display.OpacityArray = [None, '']
        delaunay2D1Display.OpacityTransferFunction = 'PiecewiseFunction'
        delaunay2D1Display.DataAxesGrid = 'GridAxesRepresentation'
        delaunay2D1Display.PolarAxes = 'PolarAxesRepresentation'
        delaunay2D1Display.SelectInputVectors = [None, '']
        delaunay2D1Display.WriteLog = ''
        # change solid color
        delaunay2D1Display.AmbientColor = surfcolor
        delaunay2D1Display.DiffuseColor = surfcolor
    return

def plotPolyLineList(polydict):
    defaultdict =  {'color':[0,0,0],
                    'closeloop':False,
                    'makesurface':False, 'surfacecolor':[1,1,1]}
    defaults = polydict['defaults'] if 'defaults' in polydict else defaultdict
    for polyspec in polydict['polylinelist']:
        name   = polyspec['name']
        color      = getdictval(polyspec, 'color', defaults)
        closeloop  = getdictval(polyspec, 'closeloop', defaults)
        makesurface= getdictval(polyspec, 'makesurface', defaults)
        surfacecolor = getdictval(polyspec, 'surfacecolor', defaults)
        points = polyspec['points']
        plotPolyLine(name, points, color=color, closeloop=closeloop,
                     makesurface=makesurface, surfacecolor=surfacecolor)
    return
# =====================================
def add3DText(name, text, pos, color=[0.0, 0.0, 0.0], scale=[1,1,1]):
    # create a new '3D Text'
    a3DText1 = a3DText(registrationName=name)
    # Properties modified on a3DText1
    a3DText1.Text = text

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    a3DText1Display = Show(a3DText1, renderView1, 'GeometryRepresentation')
    # trace defaults for the display properties.
    a3DText1Display.Representation = 'Surface'
    a3DText1Display.ColorArrayName = [None, '']
    a3DText1Display.SelectTCoordArray = 'None'
    a3DText1Display.SelectNormalArray = 'None'
    a3DText1Display.SelectTangentArray = 'None'
    a3DText1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    a3DText1Display.SelectOrientationVectors = 'None'
    a3DText1Display.ScaleFactor = 0.5254759460687638
    a3DText1Display.SelectScaleArray = 'None'
    a3DText1Display.GlyphType = 'Arrow'
    a3DText1Display.GlyphTableIndexArray = 'None'
    a3DText1Display.GaussianRadius = 0.026273797303438186
    a3DText1Display.SetScaleArray = [None, '']
    a3DText1Display.ScaleTransferFunction = 'PiecewiseFunction'
    a3DText1Display.OpacityArray = [None, '']
    a3DText1Display.OpacityTransferFunction = 'PiecewiseFunction'
    a3DText1Display.DataAxesGrid = 'GridAxesRepresentation'
    a3DText1Display.PolarAxes = 'PolarAxesRepresentation'
    a3DText1Display.SelectInputVectors = [None, '']
    a3DText1Display.WriteLog = ''

    # change solid color
    a3DText1Display.AmbientColor = color
    a3DText1Display.DiffuseColor = color
    # Properties modified on a3DText1Display
    #a3DText1Display.Position = pos
    a3DText1Display.Translation = pos
    # Properties modified on a3DText1Display.DataAxesGrid
    a3DText1Display.DataAxesGrid.Position = pos
    # Properties modified on a3DText1Display.PolarAxes
    a3DText1Display.PolarAxes.Translation = pos

    # Properties modified on a3DText1Display
    a3DText1Display.Scale = scale
    # Properties modified on a3DText1Display.DataAxesGrid
    a3DText1Display.DataAxesGrid.Scale = scale
    # Properties modified on a3DText1Display.PolarAxes
    a3DText1Display.PolarAxes.Scale = scale
    return

def plot3DTextList(textdict):
    defaultdict =  {'color':[0,0,0], 'scale':[1,1,1]}
    defaults = textdict['defaults'] if 'defaults' in textdict else defaultdict
    for textspec in textdict['textlist']:
        name       = textspec['name']
        text       = textspec['text']
        pos        = textspec['pos']
        color      = getdictval(textspec, 'color', defaults)
        scale      = getdictval(textspec, 'scale', defaults)
        add3DText(name, text, pos, color=color, scale=scale)
    return

# =====================================

def add2DText(name, text, pos, color=[0.0, 0.0, 0.0], fontsize=12,
              WindowLocation='Any Location'):
    text1 = Text(registrationName=name)
    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    
    # show data in view
    text1Display = Show(text1, renderView1, 'TextSourceRepresentation')
    # Properties modified on text1Display
    text1.Text = text
    text1Display.Color = color
    text1Display.FontSize = fontsize
    # Properties modified on text1Display
    text1Display.WindowLocation = WindowLocation
    # Properties modified on text1Display
    #text1Display.Position = pos
    text1Display.Translation = pos    
    return

def plot2DTextList(textdict):
    defaultdict =  {'color':[0,0,0],
                    'pos':[0.9, 0.9],
                    'fontsize':12,
                    'WindowLocation':'Any Location'}
    defaults = textdict['defaults'] if 'defaults' in textdict else defaultdict
    for textspec in textdict['textlist']:
        name       = textspec['name']
        text       = textspec['text']
        pos        = getdictval(textspec, 'pos', defaults)
        fontsize   = getdictval(textspec, 'fontsize', defaults)
        color      = getdictval(textspec, 'color', defaults)
        WindowLocation = getdictval(textspec, 'WindowLocation', defaults)
        add2DText(name, text, pos, color=color, fontsize=fontsize,
                  WindowLocation=WindowLocation)
    return


# =====================================
def setRenderViewProps(renderdict):
    # get active view
    exestr="renderView1 = GetActiveViewOrCreate('RenderView')\n"
    exec(exestr)
    for prop in renderdict['properties']:
        exestr = 'renderView1.%s = %s\n'%(prop, 
                                          repr(renderdict['properties'][prop]))
        exec(exestr)
    exestr = "RenderAllViews()\n"
    exec(exestr)
    return

def setColorBarProps(CBdict):
    defaultdict =  {'var':'velocity',
                    'colormap':'Cool to Warm (Extended)'}
    defaults = CBdict['defaults'] if 'defaults' in CBdict else defaultdict
    var = defaults['var']
    # get color transfer function/color map for 'velocity'
    velocityLUT = GetColorTransferFunction(var)
    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    velocityLUT.ApplyPreset(defaults['colormap'], True)
    # get opacity transfer function/opacity map for 'velocity'
    velocityPWF = GetOpacityTransferFunction(var)
    # get 2D transfer function for 'velocity'
    velocityTF2D = GetTransferFunction2D(var)

    if 'limits' in CBdict:
        CBlimits = CBdict['limits']
        # Rescale transfer function
        velocityLUT.RescaleTransferFunction(CBlimits[0], CBlimits[1])
        velocityPWF.RescaleTransferFunction(CBlimits[0], CBlimits[1])
        velocityTF2D.RescaleTransferFunction(CBlimits[0], CBlimits[1], 0.0, 1.0)

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    # get color legend/bar for velocityLUT in view renderView1
    velocityLUTColorBar = GetScalarBar(velocityLUT, renderView1)
    for prop in CBdict['properties']:
        exestr = 'velocityLUTColorBar.%s = %s\n'%(prop, 
                                                  repr(CBdict['properties'][prop]))
        exec(exestr)
    return
    

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
def processyamlinput(yamlfile, usejson=False, verbose=False):
    # Load the yaml input file
    with open(yamlfile) as fp:
        if (usejson is False) and yamlokay:
            Loader = yaml.load
            yamldict = Loader(fp)
        else:
            yamldict = json.load(fp)

        # Plot the turbines
        if 'turbines' in yamldict:
            if verbose: print("Loading turbines")
            plotTurbineList(yamldict['turbines'])
        if 'solidplanes' in yamldict:
            if verbose: print("Loading solid planes")
            plotPlaneList(yamldict['solidplanes'])
        if 'polylines' in yamldict:
            if verbose: print("Loading polylines")
            plotPolyLineList(yamldict['polylines'])
        if 'sampleplanes' in yamldict:
            if verbose: print("Loading sample planes")
            plotSamplePlaneList(yamldict['sampleplanes'], verbose=verbose)
        if 'annotate3D' in yamldict:
            if verbose: print("Adding annotation")
            plot3DTextList(yamldict['annotate3D'])
        if 'annotate2D' in yamldict:
            if verbose: print("Adding 2D annotation")
            plot2DTextList(yamldict['annotate2D'])            
        if 'renderview' in yamldict:
            if verbose: print("Setting renderview")
            setRenderViewProps(yamldict['renderview'])
        if 'colorbar' in yamldict:
            if verbose: print("Setting colorbar")
            setColorBarProps(yamldict['colorbar'])            
        if 'runcommands' in yamldict:
            if verbose: print("running commands")
            runCommands(yamldict['runcommands'])
        if 'output' in yamldict:
            if verbose: print("saving output: "+yamldict['output']['filename'])
            saveoutput(yamldict['output'])
        if verbose: print("Done")
    return

# =====================================

if __name__ == "__main__":
    title="Render wind farm scene"
    parser = argparse.ArgumentParser(description=title)
    parser.add_argument('inputfile')
    parser.add_argument('-j', '--json', 
                        help="Use json input file",
                        default=False,
                        action='store_true')
    parser.add_argument('-v', '--verbose', 
                        help="Verbose output",
                        default=False,
                        action='store_true')
    # Load the options
    args      = parser.parse_args()
    inputfile = args.inputfile
    verbose   = args.verbose
    usejson   = args.json

    processyamlinput(inputfile, usejson=usejson, verbose=verbose)
