# The goal is to compare the hull drag force to the thrust force of the motor at different speeds


import ansys.fluent.core as pyfluent

import_file_name = examples.download_file(
    "fillernamefornow.msh.h5", "path/to/file"
)

solver = pyfluent.launch_fluent(
    precision="double",
    processor_count=16,
    gpu=[0], # set the gpu to be used (usually index 0 for nvidia)
    mode="solver", # this assumes mesh is predone
)



# read the mesh file
solver.file.read_case(file_name=import_file_name)


#setup materials
solver.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")


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
