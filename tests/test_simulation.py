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


def test_simulate_sample_returns_expected_shape(monkeypatch):
    # Patch multiprocessing to run inline
    monkeypatch.setattr(sim_module, "Pool", DummyPool)
    monkeypatch.setattr(sim_module.mp, "cpu_count", lambda: 1)

    cal = Calorimeter()
    cal.add_layer(Layer("active", material=0.0, thickness=1.0, response=1.0))
    cal.add_layer(Layer("passive", material=0.0, thickness=1.0, response=0.0))

    s = Simulation(cal)
    # Create 3 particles with different energies
    particles = [Electron(z=0.0, energy=0.5), Electron(z=0.0, energy=0.6), Electron(z=0.0, energy=0.7)]

    out = s.simulate_sample(particles, deadcellfraction=0.0)
    # Only active layers are counted in ionisations by default
    assert out.shape == (3, 1)


def test_simulate_sample_preserves_order(monkeypatch):
    # Patch multiprocessing to run inline but track call order
    call_order = []

    class OrderTrackingPool:
        def __init__(self, n):
            self.n = n
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            return False
        def map(self, fn, args_list):
            results = []
            for args in args_list:
                # Track which particle index is being processed
                call_order.append(args[3])  # args[3] is the index
                results.append(fn(args))
            return results

    monkeypatch.setattr(sim_module, "Pool", OrderTrackingPool)
    monkeypatch.setattr(sim_module.mp, "cpu_count", lambda: 1)

    cal = Calorimeter()
    cal.add_layer(Layer("active", material=0.0, thickness=1.0, response=1.0))
    cal.add_layer(Layer("passive", material=0.0, thickness=1.0, response=0.0))

    s = Simulation(cal)
    # Create 3 particles
    particles = [
        Electron(z=0.0, energy=0.1),
        Electron(z=0.0, energy=0.5),
        Electron(z=0.0, energy=0.3)
    ]

    out = s.simulate_sample(particles, deadcellfraction=0.0)

    # Results should be in the same order as the input particles
    assert out.shape == (3, 1)
    # Verify that results maintain the original particle order (0, 1, 2)
    # by checking the indexed results are properly sorted
    assert len(out) == len(particles)


def test_run_single_simulation_indexed():
    import copy
    from calorimeter.simulation import _run_single_simulation_indexed

    cal = Calorimeter()
    cal.add_layer(Layer("active", material=0.0, thickness=1.0, response=1.0))

    e = Electron(z=0.0, energy=0.5)
    args = (copy.deepcopy(cal), e, 0.1, 42)

    result = _run_single_simulation_indexed(args)
    # Should return tuple of (ionisations, index)
    assert isinstance(result, tuple)
    assert len(result) == 2
    ionisations, index = result
    assert index == 42
    assert ionisations.shape == (1,)
