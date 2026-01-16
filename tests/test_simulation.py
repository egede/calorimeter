import random
import pytest

from calorimeter.calorimeter import Calorimeter
from calorimeter.layer import Layer
from calorimeter.particle import Electron
import calorimeter.simulation as sim_module
from calorimeter.simulation import Simulation


class DummyPool:
    def __init__(self, n):
        self.n = n
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return False
    def map(self, fn, args_list):
        return [fn(args) for args in args_list]


def test_simulate_returns_expected_shape(monkeypatch):
    # Patch multiprocessing to run inline
    monkeypatch.setattr(sim_module, "Pool", DummyPool)
    monkeypatch.setattr(sim_module.mp, "cpu_count", lambda: 1)

    cal = Calorimeter()
    cal.add_layer(Layer("active", material=0.0, thickness=1.0, response=1.0))
    cal.add_layer(Layer("passive", material=0.0, thickness=1.0, response=0.0))

    s = Simulation(cal)
    e = Electron(z=0.0, energy=0.5)

    out = s.simulate(e, number=3, deadcellfraction=0.0)
    # Only active layers are counted in ionisations by default
    assert out.shape == (3, 1)


def test_simulate_with_tracing_records_traces():
    cal = Calorimeter()
    cal.add_layer(Layer("active", material=0.0, thickness=1.0, response=1.0))

    s = Simulation(cal)
    # Energy below cutoff ensures no new particles; simpler trace
    e = Electron(z=0.0, energy=0.005)

    ion, c = s.simulate_with_tracing(e, deadcellfraction=0.0)
    assert ion.shape == (1,)
    traces = c.get_particle_traces()
    assert isinstance(traces, list)
    # At least one electron trace should be recorded
    assert any(p.type == "elec" for p, _ in traces)
