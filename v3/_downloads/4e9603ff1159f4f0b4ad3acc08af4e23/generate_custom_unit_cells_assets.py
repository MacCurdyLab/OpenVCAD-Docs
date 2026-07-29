#!/usr/bin/env python3
"""Regenerate every figure owned by the Custom unit cells guide."""

from pathlib import Path
import runpy

import pyvcad_rendering as viz


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
EXAMPLES_DIR = REPO_ROOT / "examples" / "metamaterials" / "custom_unit_cells"
IMAGES_DIR = REPO_ROOT / "docs" / "source" / "guides" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 900
HEIGHT = 640
BASE_SETTINGS = {
    "quality": "medium",
    "render_mode": "iso_surface",
    "visualized_attribute": "none",
    "use_blending": True,
    "show_bbox": False,
    "show_origin": False,
    "show_orientation_marker": False,
    "background_color": (1.0, 1.0, 1.0),
    "transparent_background": False,
    "scale_bar_visible": False,
    "scale": 2,
}


def camera(focal_point, parallel_scale):
    return {
        "position": (
            focal_point[0] + 42.0,
            focal_point[1] - 58.0,
            focal_point[2] + 36.0,
        ),
        "focal_point": focal_point,
        "view_up": (0.0, 0.0, 1.0),
        "parallel_projection": True,
        "parallel_scale": parallel_scale,
        "view_angle": 30.0,
    }


SINGLE_CELL_CAMERA = camera((0.0, 0.0, 0.0), 10.0)
TILED_CELL_CAMERA = camera((0.0, 0.0, 0.0), 27.0)
GRAPH_CONFORMAL_CAMERA = camera((-20.0, 0.0, 12.0), 20.0)
IMPLICIT_CONFORMAL_CAMERA = camera((20.0, 0.0, 12.0), 20.0)


def capture_example(filename):
    original_render = viz.Render
    captured = {}

    def capture(node, materials=None):
        captured["root"] = node
        captured["materials"] = materials

    viz.Render = capture
    try:
        namespace = runpy.run_path(
            str(EXAMPLES_DIR / filename),
            run_name="__main__",
        )
    finally:
        viz.Render = original_render

    if "root" not in captured:
        raise RuntimeError("{} did not call viz.Render".format(filename))
    return namespace


def render(node, name, **overrides):
    settings = dict(BASE_SETTINGS)
    settings.update(overrides)
    output = IMAGES_DIR / "mm_custom_unit_cells_{}.png".format(name)
    viz.Render_Image(
        node,
        str(output),
        settings=settings,
        width=WIDTH,
        height=HEIGHT,
    )
    print("wrote", output)


def generate_all():
    explicit = capture_example("01_explicit_graph_cell.py")
    programmed = capture_example("02_programmed_graph_cell.py")
    implicit = capture_example("03_custom_implicit_cell.py")
    conformal = capture_example("04_conformal_custom_cells.py")

    render(
        explicit["unit_cell_preview"],
        "axis_star_single",
        camera_state=SINGLE_CELL_CAMERA,
        show_bbox=True,
    )
    render(
        explicit["tiled_lattice"],
        "axis_star_tiled",
        camera_state=TILED_CELL_CAMERA,
    )
    render(
        programmed["unit_cell_preview"],
        "hourglass_single",
        camera_state=SINGLE_CELL_CAMERA,
        show_bbox=True,
    )
    render(
        programmed["tiled_lattice"],
        "hourglass_graded",
        camera_state=TILED_CELL_CAMERA,
    )
    render(
        implicit["unit_cell_preview"],
        "implicit_single",
        quality="low",
        camera_state=SINGLE_CELL_CAMERA,
        show_bbox=True,
    )
    render(
        implicit["tiled_lattice"],
        "implicit_tiled",
        quality="low",
        camera_state=TILED_CELL_CAMERA,
    )
    render(
        conformal["conformal_graph"],
        "graph_conformal",
        camera_state=GRAPH_CONFORMAL_CAMERA,
    )
    render(
        conformal["conformal_implicit"],
        "implicit_conformal",
        quality="low",
        camera_state=IMPLICIT_CONFORMAL_CAMERA,
    )


if __name__ == "__main__":
    generate_all()
