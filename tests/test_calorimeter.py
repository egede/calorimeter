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
    assert [v.z for v in cal.volumes(active=False)] == [0.0, 1.0]


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


def test_calorimeter_add_layers_empty_list():
    """Test add_layers with an empty list."""
    cal = Calorimeter()
    cal.add_layers([])
    assert cal._zend == 0.0
    assert len(cal.volumes(active=False)) == 0


def test_calorimeter_add_layers_single_layer():
    """Test add_layers with a single layer."""
    cal = Calorimeter()
    layers = [Layer("L1", material=0.0, thickness=1.0, response=1.0)]
    cal.add_layers(layers)

    assert cal._zend == 1.0
    assert len(cal.volumes(active=False)) == 1
    assert cal.volumes(active=False)[0].z == 0.0
    assert cal.volumes(active=False)[0].layer.get_name() == "L1"


def test_calorimeter_add_layers_multiple_layers():
    """Test add_layers with multiple layers."""
    cal = Calorimeter()
    layers = [
        Layer("L1", material=0.0, thickness=1.0, response=1.0),
        Layer("L2", material=0.5, thickness=2.0, response=0.0),
        Layer("L3", material=1.0, thickness=1.5, response=2.0)
    ]
    cal.add_layers(layers)

    assert cal._zend == 4.5
    assert len(cal.volumes(active=False)) == 3
    assert [v.z for v in cal.volumes(active=False)] == [0.0, 1.0, 3.0]
    assert [v.layer.get_name() for v in cal.volumes(active=False)] == ["L1", "L2", "L3"]


def test_calorimeter_add_layers_after_add_layer():
    """Test add_layers after adding individual layers."""
    cal = Calorimeter()
    cal.add_layer(Layer("L1", material=0.0, thickness=1.0, response=1.0))

    layers = [
        Layer("L2", material=0.5, thickness=2.0, response=0.0),
        Layer("L3", material=1.0, thickness=1.5, response=2.0)
    ]
    cal.add_layers(layers)

    assert cal._zend == 4.5
    assert len(cal.volumes(active=False)) == 3
    assert [v.z for v in cal.volumes(active=False)] == [0.0, 1.0, 3.0]


def test_calorimeter_add_layers_preserves_order():
    """Test that add_layers preserves the order of layers."""
    cal = Calorimeter()
    layers = [
        Layer("First", material=0.0, thickness=1.0, response=1.0),
        Layer("Second", material=0.5, thickness=1.0, response=1.0),
        Layer("Third", material=1.0, thickness=1.0, response=1.0)
    ]
    cal.add_layers(layers)

    names = [v.layer.get_name() for v in cal.volumes(active=False)]
    assert names == ["First", "Second", "Third"]


def test_calorimeter_add_layers_updates_positions():
    """Test that add_layers correctly updates z positions."""
    cal = Calorimeter()
    layers = [
        Layer("L1", material=0.0, thickness=0.5, response=1.0),
        Layer("L2", material=0.5, thickness=1.5, response=1.0),
        Layer("L3", material=1.0, thickness=2.0, response=1.0)
    ]
    cal.add_layers(layers)

    volumes = cal.volumes(active=False)
    assert volumes[0].z == 0.0
    assert volumes[1].z == 0.5
    assert volumes[2].z == 2.0
    assert cal._zend == 4.0


def test_calorimeter_add_layers_copies_layers():
    """Test that add_layers creates copies of layers, not references."""
    cal = Calorimeter()
    layer = Layer("L1", material=0.0, thickness=1.0, response=1.0)
    cal.add_layers([layer])

    # Modify the original layer
    layer._ionisation = 100.0

    # The calorimeter's layer should not be affected
    assert cal.volumes(active=False)[0].layer._ionisation == 0.0
