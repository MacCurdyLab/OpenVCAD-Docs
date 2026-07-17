"""Grade unit-cell spacing with an immutable field-warped CellMap."""

import pyvcad as pv
import pyvcad_metamaterials as mm
import pyvcad_rendering as viz

base_map = mm.rectangular_cell_map(
    (pv.Vec3(-30.0, -12.0, -12.0), pv.Vec3(30.0, 12.0, 12.0)),
    cells=(8, 3, 3),
)


def u_spacing(u, v, w, d):
    return -0.8 + 1.6 * u / 8.0


warped_map = mm.warp_cell_map(
    base_map,
    u_scale=mm.cell_field(base_map, u_spacing),
    lock_u_bounds=True,
)
root = mm.gyroid(warped_map, wall_thickness=1.4)
viz.Render(root)
