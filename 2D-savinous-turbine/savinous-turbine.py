import pathlib
from build123d import *
from ocp_vscode import show, Camera
import numpy as np

# --- Parameters ---
blade_radius = 50.0
overlap = 20.0
blade_thickness = 3.0
disk_radius = 100.0     # Radius of the circle holding the turbine
rect_width = 800.0
rect_height = 400.0

# --- Body 1: The Inner Turbine Disk ---
with BuildSketch() as turbine_disk:
    Circle(disk_radius)
    with BuildSketch(mode=Mode.SUBTRACT):
        with BuildLine() as path:
            # 3 blades: 60 deg, 180 deg, -60 deg
            center = (blade_radius - overlap / 2)
            l1 = CenterArc((-center, 0), blade_radius, 0, 180)
            with Locations(Location((0,0), -120)):
                l2 = CenterArc((-center, 0), blade_radius, 0, 180)
                add(l2)
            with Locations(Location((0,0), 120)):
                l3 = CenterArc((-center, 0), blade_radius, 0, 180)
                add(l3)
        for edge in path.edges():
            make_face(offset(edge, amount=blade_thickness / 2, kind=Kind.INTERSECTION))

# --- Body 2: The Outer Rectangular Plate ---
with BuildSketch() as outer_plate:
    Rectangle(rect_width, rect_height)
    # Subtract the disk for clearance
    Circle(disk_radius, mode=Mode.SUBTRACT)

# Combine for export
current_folder = pathlib.Path(__file__).parent
output_path = current_folder / "2d-savinous-turbine.step"
comp_domain = Compound([turbine_disk.sketch, outer_plate.sketch])
export_step(comp_domain, str(output_path))

# --- Display ---
show(
    turbine_disk.sketch, 
    outer_plate.sketch, 
    names=["Turbine Disk", "Outer Plate"],
    colors=["#0078D7", "#7A7A7A"],
    reset_camera=Camera.RESET)