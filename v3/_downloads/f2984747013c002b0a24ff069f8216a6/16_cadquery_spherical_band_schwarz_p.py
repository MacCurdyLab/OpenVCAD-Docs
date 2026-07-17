"""Map a Schwarz-P TPMS across a CadQuery-authored spherical band."""

import cadquery as cq

import pyvcad_metamaterials as mm
import pyvcad_rendering as viz


cad = cq.Workplane(
    obj=cq.Solid.makeSphere(
        22.0,
        angleDegrees1=-60.0,
        angleDegrees2=60.0,
    )
)
surface = mm.cadquery.face(cad.faces("%SPHERE"))
cell_map = mm.cell_map_from_cad_face(
    surface,
    cells=(14, 7, 1),
    height=4.5,
)
root = mm.schwarz_p(cell_map, wall_thickness=0.45)

viz.Render(root)
