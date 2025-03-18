# The goal is to compare the hull drag force to the thrust force of the motor at different speeds

import os

#linux environmnet variables 
#os.environ['AWP_ROOT222'] = '/opt/packages/ansys/v222' #bridges2 location of ansys 
#os.environ['AWP_ROOT242'] = '/usr/ansys_inc/v242' # local ansys location



# what this code needs: a spaceclaim file that has been converted into a mesh file (linux machines cannot read space claim cad files)



import ansys.fluent.core as pyfluent
#meshing = pyfluent.launch_fluent(mode ="meshing", precision=pyfluent.Precision.DOUBLE, dimension=pyfluent.Dimension.THREE, processor_count=8, start_timeout=360)
#meshing.file.read(file_type="mesh", file_name='/workspaces/ANSYS/60cmd240cml20mminner.msh.h5')


# Archimedes Screw Workflow #
# first thing you do -> create the mesh based off spaceclaim mesh file (define boundaries and element sizes)
# second thing you do -> load the case file based off small mesh 
workdir = 'C:/Users/boatingAway/Desktop/real/Prodesign'
# mesh from spaceclaim, preprovided
startmesh = 'archimeshsmol.msh.h5'
meshfolder = 'solution'
meshfile = 'solutionmesh.msh.h5'
finalmeshlocation = '/'.join([workdir, meshfolder, meshfile])
# case file from fluent, preprovided 
startcase = 'archimedes.cas.h5'

if not os.path.exists(finalmeshlocation):
    # launch meshing session
    session = pyfluent.launch_fluent(mode="meshing", version="3d", precision="double", processor_count=6, start_timeout=360, show_gui=True)
    workflow = session.workflow
    meshing = session.meshing

    meshing.GlobalSettings.EnableCleanCAD.set_state(True)
    meshing.GlobalSettings.EnableComplexMeshing.set_state(True)
    meshing.GlobalSettings.UseAllowedValues.set_state(True)
    meshing.GlobalSettings.EnablePrimeMeshing.set_state(False)
    meshing.GlobalSettings.EnablePrime2dMeshing.set_state(False)
    workflow.InitializeWorkflow(WorkflowType=r'Watertight Geometry')
    location = [workdir, startmesh]
    workflow.TaskObject['Import Geometry'].Arguments.set_state({r'FileFormat': r'Mesh',r'ImportCadPreferences': {r'CISeparation': r'region',r'MaxFacetLength': 0,},r'LengthUnit': r'mm',r'MeshFileName': r'/'.join(location),})
    workflow.TaskObject['Import Geometry'].Execute()
    workflow.TaskObject['Add Local Sizing'].Arguments.set_state({r'AddChild': r'yes',r'BOICellsPerGap': 1,r'BOIControlName': r'bodysize_1',r'BOICurvatureNormalAngle': 18,r'BOIExecution': r'Body Size',r'BOIFaceLabelList': [r'dynamic'],r'BOIGrowthRate': 1.2,r'BOISize': 100,r'BOIZoneorLabel': r'label',})
    workflow.TaskObject['Add Local Sizing'].AddChildAndUpdate(DeferUpdate=False)
    workflow.TaskObject['Generate the Surface Mesh'].Arguments.set_state({r'CFDSurfaceMeshControls': {r'MinSize': 10,},})
    workflow.TaskObject['bodysize_1'].Revert()
    workflow.TaskObject['bodysize_1'].Arguments.set_state({r'AddChild': r'yes',r'BOICellsPerGap': 1,r'BOIControlName': r'bodysize_1',r'BOICurvatureNormalAngle': 18,r'BOIExecution': r'Body Size',r'BOIFaceLabelList': [r'dynamic'],r'BOIGrowthRate': 1.2,r'BOISize': 10,r'BOIZoneorLabel': r'label',r'CompleteFaceLabelList': [r'dynamic'],r'DrawSizeControl': True,})
    workflow.TaskObject['bodysize_1'].Execute()
    workflow.TaskObject['Generate the Surface Mesh'].Execute()
    workflow.TaskObject['Describe Geometry'].UpdateChildTasks(SetupTypeChanged=False)
    workflow.TaskObject['Describe Geometry'].Arguments.set_state({r'NonConformal': r'No',r'SetupType': r'The geometry consists of only fluid regions with no voids',})
    workflow.TaskObject['Describe Geometry'].UpdateChildTasks(SetupTypeChanged=True)
    workflow.TaskObject['Describe Geometry'].Arguments.set_state({r'NonConformal': r'No',r'SetupType': r'The geometry consists of only fluid regions with no voids',r'WallToInternal': r'Yes',})
    workflow.TaskObject['Describe Geometry'].Execute()
    workflow.TaskObject['Update Boundaries'].Execute()
    workflow.TaskObject['Update Regions'].Arguments.set_state({r'OldRegionNameList': [r'fluid'],r'OldRegionTypeList': [r'fluid'],r'RegionNameList': [r'fluid'],r'RegionTypeList': [r'dead'],})
    workflow.TaskObject['Update Regions'].Execute()
    workflow.TaskObject['Add Boundary Layers'].Arguments.set_state({r'BLControlName': r'last-ratio_1',r'LocalPrismPreferences': {r'Continuous': r'Continuous',},r'OffsetMethodType': r'last-ratio',})
    workflow.TaskObject['Add Boundary Layers'].AddChildAndUpdate(DeferUpdate=False)
    workflow.TaskObject['last-ratio_1'].Revert()
    workflow.TaskObject['last-ratio_1'].Arguments.set_state({r'BLControlName': r'last-ratio_1',r'BLRegionList': [r'dynamic', r'origin-origin-fff'],r'BLZoneList': [r'origin-wall'],r'FirstHeight': 1,r'LocalPrismPreferences': {r'Continuous': r'Continuous',},r'OffsetMethodType': r'last-ratio',})
    workflow.TaskObject['last-ratio_1'].Execute()
    workflow.TaskObject['Generate the Volume Mesh'].Arguments.set_state({r'VolumeFill': r'poly-hexcore',r'VolumeMeshPreferences': {r'Avoid1_8Transition': r'yes',r'ShowVolumeMeshPreferences': True,},})
    workflow.TaskObject['Generate the Volume Mesh'].Execute()
    # write mesh file to selected folder for reuse and easy import to case later
    meshing.File.WriteMesh(FileName=finalmeshlocation)

    #close fluent once meshing done
    session.exit()



# relaunch fluent as solution mode
solver = pyfluent.launch_fluent(mode="solver", version="3d", precision="double", processor_count=6, start_timeout=360, show_gui=True)

# read case file 
case_file_name = '/'.join([workdir, startcase])
solver.file.read_case(file_type="case", file_name=case_file_name)

# replace the mesh
solver.file.replace_mesh(file_type="mesh", file_name=finalmeshlocation)

# iterate over [ 1 2 3 4 5 5 6 7 8 9 10 ] m/s of water 
for  velocity in range(1, 11):
    solver.setup.boundary_conditions.pressure_inlet['origin-inlet'] = {"phase" : {"mixture" : {"multiphase" : {"vmag" : {"value" : velocity}}}}}
    #initialize 
    #solver.initialization.open_channel_auto_init = {"boundary_zone": "origin-inlet", "flat_init": True}
    #solver.initialization.open_channel_auto_init.flat_init=True
    #solver.tui.initialize()

    # run calculation
    solver.solution.run_calculation.iterate(number_of_iterations=15)
    datapath = os.path.join(workdir, meshfolder, str(velocity))
    if not os.path.exists(datapath):
        os.mkdir(datapath)
    solver.file.write_data(FileName=datapath)
    # save all the results in between iterations 
solver.exit()

# DONE






#fit the curve of the drag of the boat

# https://fluent.docs.pyansys.com/version/stable/examples/00-fluent/mixing_elbow_settings_api.html#sphx-glr-examples-00-fluent-mixing-elbow-settings-api-py


# loop through the variables we want to change
startVel = 0 # set these initial values as a starting point
startRPM = 500 # set the initial guess rpm


# basically we want to match the drag of the boat to the power of the propeller

# do a simple " linear fit to minimize number of trials needed"

#use the data of the drag on the boat -> initial guess should be 500 rpm -> create a list with all the tested rpms and their force,
# and interpolate between the data
# use some sort of fitting / gradient descent method to get closer to the value we want 
# dont use anything complicated, just like newton raphson or something and instead of searching for the zero,
# search for the drag force of the boat 

# store RPM, Torque, Force
dataList = [[startRPM]]

# use a dictionary to store data of combination of rpm, water speed that give a certain force


for waterVel in (range(4, 30)/2):
    error = 1000
    while error > 1: # set max error (for force) that we are comfortable with


    # once you find an rpm and watervel match, then



#### add local sizing
#  body size 
# target mesh size .003
# rotary domain select 



#### generate the surface mesh
# use custom size control field size (no)
# minimum size 10^-4
# maximum size .075
# growth rate 1.2
# size functions: curvature and proximity
# curvature to normal angle 18
# cells per gap - 1
# scope proximity to edges
# separate out boundary zones by angle (no)



#### describe the geometry
# the geometry consists of only fluid regions with no voids
# change all fluid boundary types from wall to internal (yes)
# Do you want to apply share topology (yes?) but use no for now
# enable multizone meshing (no)



#### update boundaries
#outlet should be outflow
#inlet should be velocity inlet
#propeller should be wall



#### update regions
# rotary and stationary should be fluid


#### boundary layer -> 
# last-ratio type
# 3 layers
# transition ration = .27
# first height = 4*10^-5
# add in fluid regions
# grow on selected labels -> propeller 



#### generate the volume mesh
#solver fluent
# fill with poly-hexcore 
# sizing method global
# buffer layers 2
# peel layers 1
# min cell length 10^-4
# max cell length .0512
#enable parallel meshing
## advance options
# quality method orthogonal
# quality improve limit .05
#use size field no
# polyhedral mesh feature angle (deg) 30 
# avoid 1/8 octree transition (yes)
# check self proximity (no)
# write prism control file (no)







# fluent solver

#### method 
# Piso
# skewness correction 1
# neighbor correlation 1
# gradient green gauss node based 
# pressure presto
# momentum quick
# turbulent kinetic energy quick
# specific dissipation rate quick
# 









##### for a different project, not for CMSR propeller
# but can be a reference 

#### dynamic mesh (nothing on the 3 left side options)
# just choose 6 DOF
# set the mass
# one DOF rotation
# set the axis 
# set the moment of inertia along that axis 

# dynamic mesh zones
# turbine wall 
# rigid body 



#### initialization 
# compute from all zones
