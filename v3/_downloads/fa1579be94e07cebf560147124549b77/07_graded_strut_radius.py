"""Grade native mapped beam radius in explicit world coordinates."""

import pyvcad as pv
import pyvcad_metamaterials as mm
import pyvcad_rendering as viz

cell_map = mm.rectangular_cell_map(
    (pv.Vec3(-22.0, -22.0, -22.0), pv.Vec3(22.0, 22.0, 22.0)),
    cells=(4, 4, 4),
)


def beam_radius(x, y, z, d):
    return 0.3 + (x + 22.0) / 44.0


root = mm.bcc(cell_map, beam_radius=mm.world_field(beam_radius))
viz.Render(root)
