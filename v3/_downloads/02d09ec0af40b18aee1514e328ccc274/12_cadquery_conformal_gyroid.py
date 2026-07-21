"""Author a cylindrical CAD face and map a conformal gyroid onto it."""

import cadquery as cq

import pyvcad as pv
import pyvcad_metamaterials as mm
import pyvcad_rendering as viz

cad = cq.Workplane("XY").circle(20.0).extrude(30.0)
surface = pv.CADModel.from_cadquery(cad.faces("%CYLINDER")).faces[0]
cell_map = mm.cell_map_from_cad_face(
    surface,
    cells=(24, 10, 1),
    height=4.0,
    linear=False,
)
root = mm.gyroid(cell_map, wall_thickness=0.65)

viz.Render(root)
