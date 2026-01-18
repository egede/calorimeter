import matplotlib
matplotlib.use("Agg")

import pytest
from matplotlib.colors import to_rgba

from calorimeter.calorimeter import Calorimeter
from calorimeter.layer import Layer
from calorimeter.particle import Electron
from calorimeter.particle import Muon


def test_draw_returns_axes_and_rectangles():
    cal = Calorimeter()
    cal.add_layer(Layer("active", material=0.0, thickness=1.0, response=1.0))
    cal.add_layer(Layer("passive", material=0.0, thickness=2.0, response=0.0))

    ax = cal.draw(show_traces=False)
    assert ax is not None
    # Two rectangles for two layers
    assert len(ax.patches) >= 2

    # Check colors for active/passive layers (alpha=0.7 as set in draw method)
    active_color = to_rgba("#1f77b4", alpha=0.7)
    passive_color = to_rgba("#999999", alpha=0.7)
    # First two patches correspond to two layers added
    colors = [p.get_facecolor() for p in ax.patches[:2]]
    assert colors[0] == active_color
    assert colors[1] == passive_color

    # Axis labels and title
    assert ax.get_xlabel() == "z position (cm)"
    assert ax.get_ylabel() == "Perpendicular extent (cm)"
    assert ax.get_title() == "Calorimeter Design"

    # Limits include zend with margin
    assert pytest.approx(ax.get_xlim()[1], 1e-8) == cal._zend + 0.5


def test_draw_with_traces_adds_legend_entries():
    cal = Calorimeter()
    cal.add_layer(Layer("active", material=0.0, thickness=1.0, response=1.0))

    # Record an electron trace and a muon trace
    cal.enable_tracing()
    e = Electron(z=0.0, energy=0.05, trace=[(0.0, 0.0, 0.0), (0.1, 0.01, 0.0)])
    cal.record_trace(e)

    m = Muon(z=0.0, energy=0.1, trace=[(0.0, 0.0, 0.0), (0.2, 0.02, 0.0)])
    cal.record_trace(m)

    ax = cal.draw(show_traces=True)
    legend = ax.get_legend()
    assert legend is not None
    labels = [t.get_text() for t in legend.get_texts()]
    # Active/passive are always present; electron and muon traces labels present as well
    assert any("Active layer" in s for s in labels)
    assert any("Electron traces" in s for s in labels)
    assert any("Muon traces" in s for s in labels)
