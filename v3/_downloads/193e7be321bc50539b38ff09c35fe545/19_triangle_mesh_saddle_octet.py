"""Map an octet graph lattice onto a saddle-shaped triangle-mesh disk patch."""

import sys
from pathlib import Path

import pyvcad as pv
import pyvcad_metamaterials as mm
import pyvcad_rendering as viz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _triangle_surface_examples import grid_surface


def saddle(x, y):
    return 0.02 * (x * x - y * y)


# The free-boundary parameterization flattens the saddle without constraining its outline; the
# map's logical cell counts are chosen independently of the mesh resolution.
surface = grid_surface(30.0, 30.0, 14, 14, saddle)
cell_map = mm.cell_map_from_surface(
    surface,
    cells=(12, 10, 1),
    height=5.0,
    linear=False,
)
root = mm.fcc(cell_map, beam_radius=0.3)

viz.Render(root)
