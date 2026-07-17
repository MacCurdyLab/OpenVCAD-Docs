"""Fit a freeform CadQuery saddle and map a diamond beam lattice across it."""

import math

import cadquery as cq

import pyvcad_metamaterials as mm
import pyvcad_rendering as viz


def saddle(u, v):
    x = 42.0 * (u - 0.5)
    y = 34.0 * (v - 0.5)
    z = 7.0 * math.sin(math.pi * (u - 0.5)) * math.sin(math.pi * (v - 0.5))
    return x, y, z


cad = cq.Workplane("XY").parametricSurface(
    saddle,
    N=20,
    tol=0.02,
    smoothing=None,
)
surface = mm.cadquery.face(cad)
cell_map = mm.cell_map_from_cad_face(
    surface,
    cells=(12, 10, 1),
    height=2.5,
)
root = mm.diamond(cell_map, beam_radius=0.24, node_radius=0.3)

viz.Render(root)
