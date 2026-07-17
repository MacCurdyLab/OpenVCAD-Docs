"""Grade mapped TPMS wall thickness in explicit world coordinates."""

import pyvcad as pv
import pyvcad_metamaterials as mm
import pyvcad_rendering as viz

block = 48.0
cell_map = mm.rectangular_cell_map(
    (pv.Vec3(-24.0, -10.0, -10.0), pv.Vec3(24.0, 10.0, 10.0)),
    cells=(6, 3, 3),
)


def wall_thickness(x, y, z, d):
    return 0.6 + 2.0 * (x + block / 2.0) / block


root = mm.gyroid(cell_map, wall_thickness=mm.world_field(wall_thickness))
viz.Render(root)
