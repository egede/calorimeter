import random
import pytest

from calorimeter.calorimeter import Calorimeter
from calorimeter.layer import Layer
from calorimeter.particle import Electron, Photon


def test_calorimeter_add_layer_positions_and_zend():
    cal = Calorimeter()
    cal.add_layer(Layer("L1", material=0.0, thickness=1.0, response=1.0))
    cal.add_layer(Layer("L2", material=0.0, thickness=2.0, response=0.0))

    assert cal._zend == 3.0
    assert list(cal.positions(active=False)) == [0.0, 1.0]


def test_calorimeter_step_in_active_layer_ionises(monkeypatch):
    cal = Calorimeter()
    layer = Layer("L1", material=0.0, thickness=1.0, response=2.0)
    cal.add_layer(layer)

    e = Electron(z=0.0, energy=1.0)

    # No interaction path
    monkeypatch.setattr(random, "random", lambda: 1.0)
    out = cal.step(e, step=0.5)

    assert out == [e]
    # Access the layer from the calorimeter since add_layer makes a copy
    assert cal._layers[0].layer._ionisation == pytest.approx(1.0, abs=1e-8)


def test_calorimeter_reset_clears_ionisation_and_traces():
    cal = Calorimeter()
    layer = Layer("L1", material=0.0, thickness=1.0, response=1.0)
    cal.add_layer(layer)

    # Simulate some ionisation and traces
    p = Electron(z=0.0, energy=0.5, trace=[(0.0, 0.0, 0.0)])
    cal.enable_tracing()
    cal.record_trace(p)
    layer._ionisation = 3.0

    cal.reset()
    assert all(val == 0 for val in cal.ionisations(active=False))
    assert cal.get_particle_traces() == []


def test_calorimeter_record_trace_filters_particle_types():
    cal = Calorimeter()

    ph = Photon(z=0.0, energy=0.5, trace=[(0.0, 0.0, 0.0)])
    cal.enable_tracing()
    cal.record_trace(ph)
    assert cal.get_particle_traces() == []

    e = Electron(z=0.2, energy=0.5, trace=[(0.0, 0.0, 0.0)])
    cal.record_trace(e)
    traces = cal.get_particle_traces()
    assert len(traces) == 1
    particle, trace = traces[0]
    assert particle.type == "elec"
    assert len(trace) >= 2


def test_calorimeter_str_empty():
    """Test __str__ method for empty calorimeter."""
    cal = Calorimeter()
    result = str(cal)
    assert "The layers of the calorimeter:" in result


def test_calorimeter_str_single_layer():
    """Test __str__ method with a single layer."""
    cal = Calorimeter()
    layer = Layer("TestLayer", material=0.5, thickness=1.5, response=2.0)
    cal.add_layer(layer)

    result = str(cal)
    assert "The layers of the calorimeter:" in result
    assert "0.00" in result  # z position should be formatted to 2 decimal places
    assert "TestLayer" in result


def test_calorimeter_str_multiple_layers():
    """Test __str__ method with multiple layers."""
    cal = Calorimeter()
    layer1 = Layer("Layer1", material=0.0, thickness=1.0, response=1.0)
    layer2 = Layer("Layer2", material=0.5, thickness=2.0, response=0.0)
    layer3 = Layer("Layer3", material=1.0, thickness=1.5, response=2.0)

    cal.add_layer(layer1)
    cal.add_layer(layer2)
    cal.add_layer(layer3)

    result = str(cal)
    assert "The layers of the calorimeter:" in result
    assert "0.00" in result   # First layer at z=0.0
    assert "1.00" in result   # Second layer at z=1.0
    assert "3.00" in result   # Third layer at z=3.0
    assert "Layer1" in result
    assert "Layer2" in result
    assert "Layer3" in result


def test_calorimeter_str_z_formatting():
    """Test that z coordinates are formatted to 2 decimal places."""
    cal = Calorimeter()
    layer = Layer("L", material=0.123, thickness=0.456, response=1.0)
    cal.add_layer(layer)

    result = str(cal)
    lines = result.split('\n')
    # Second line should have the layer info (first line is header)
    assert len(lines) >= 2
    # Check that z position is formatted correctly
    assert "0.00" in result


def test_calorimeter_str_includes_layer_str():
    """Test that __str__ includes the string representation of each layer."""
    cal = Calorimeter()
    layer = Layer("MyLayer", material=0.25, thickness=2.5, response=1.5)
    cal.add_layer(layer)

    result = str(cal)
    layer_str = str(layer)

    # The layer's string representation should be included
    assert layer_str in result


def test_calorimeter_str_newline_separated():
    """Test that layers are separated by newlines."""
    cal = Calorimeter()
    cal.add_layer(Layer("L1", material=0.0, thickness=1.0, response=1.0))
    cal.add_layer(Layer("L2", material=0.5, thickness=2.0, response=0.0))

    result = str(cal)
    lines = [line for line in result.split('\n') if line.strip()]

    # Should have header + 2 layers = at least 3 lines
    assert len(lines) >= 3
    assert lines[0] == "The layers of the calorimeter:"
