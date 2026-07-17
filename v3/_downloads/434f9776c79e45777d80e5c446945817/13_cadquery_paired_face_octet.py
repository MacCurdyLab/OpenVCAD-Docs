"""Map an octet lattice between two CadQuery-authored cylindrical faces."""

import cadquery as cq

import pyvcad_metamaterials as mm
import pyvcad_rendering as viz

inner_cad = cq.Workplane("XY").circle(15.0).extrude(30.0)
outer_cad = cq.Workplane("XY").circle(22.0).extrude(30.0)
inner = mm.cadquery.face(inner_cad.faces("%CYLINDER"))
outer = mm.cadquery.face(outer_cad.faces("%CYLINDER"))

cell_map = mm.cell_map_between_cad_faces(inner, outer, cells=(24, 10, 3))


def beam_radius(u, v, w, d):
    return 0.15 + 0.10 * w / 3.0


root = mm.octet(
    cell_map,
    beam_radius=mm.cell_field(cell_map, beam_radius),
)
viz.Render(root)
