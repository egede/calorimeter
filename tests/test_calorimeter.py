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
