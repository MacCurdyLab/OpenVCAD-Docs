"""Map a conformal gyroid onto a circular domed triangle-mesh patch.

The patch is a spherical-cap dome over a round boundary -- a shape the free-boundary conformal
parameterization handles naturally. The chart keeps the patch's circular outline inside its UV
bounding rectangle, and ``CellMap`` trimming deactivates the empty rectangle corners, so the
gyroid terminates exactly at the dome's round edge instead of being stretched onto a square.
"""

import math

import sys
from pathlib import Path

import pyvcad as pv
import pyvcad_metamaterials as mm
import pyvcad_rendering as viz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _triangle_surface_examples import disk_surface

RADIUS = 15.0
DOME_HEIGHT = 8.0


def spherical_cap(x, y):
    r2 = (x * x + y * y) / (RADIUS * RADIUS)
    return DOME_HEIGHT * math.sqrt(max(0.0, 1.0 - 0.75 * r2))


surface = disk_surface(RADIUS, 10, 36, spherical_cap)
cell_map = mm.cell_map_from_surface(
    surface,
    cells=(12, 12, 1),
    height=4.0,
    linear=False,
)
root = mm.gyroid(cell_map, wall_thickness=0.7)

viz.Render(root)
