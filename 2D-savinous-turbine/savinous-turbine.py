import pathlib
from build123d import *
from ocp_vscode import show

# --- Parameters ---
blade_radius = 50.0
overlap = 10.0
blade_thickness = 3.0
disk_radius = 100.0     # Radius of the circle holding the turbine
rect_width = 500.0
rect_height = 250.0

# --- Body 1: The Inner Turbine Disk ---
with BuildSketch() as turbine_disk:
    Circle(disk_radius)
    with BuildSketch(mode=Mode.SUBTRACT):
        with BuildLine() as path:
            CenterArc((blade_radius - overlap / 2, 0), blade_radius, 0, 180)
            CenterArc((-(blade_radius - overlap / 2), 0), blade_radius, 180, 180)
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
    colors=["#0078D7", "#7A7A7A"]
)