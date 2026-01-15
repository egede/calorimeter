import random
import pytest

from calorimeter.particle import Particle, Electron, Photon, Muon


def test_particle_move_updates_positions_and_trace():
    p = Particle(type="test", z=0.0, energy=1.0, ionise=True, cutoff=0.1, x=0.0, y=0.0, angle_x=0.5, angle_y=-0.5)
    p.move(0.2)
    assert pytest.approx(p.z, 1e-8) == 0.2
    assert pytest.approx(p.x, 1e-8) == 0.1
    assert pytest.approx(p.y, 1e-8) == -0.1
    assert len(p.trace) == 1
    assert p.trace[0] == (0.0, 0.0, 0.0)


def test_electron_interact_splits_when_energy_above_cutoff(monkeypatch):
    monkeypatch.setattr(random, "random", lambda: 0.5)
    monkeypatch.setattr(random, "gauss", lambda mu, sigma: 0.0)

    e = Electron(z=0.0, energy=1.0)
    parts = e.interact()
    assert len(parts) == 2
    types = {p.type for p in parts}
    assert types == {"elec", "phot"}
    assert pytest.approx(sum(p.energy for p in parts), 1e-8) == e.energy


def test_photon_interact_splits_when_energy_above_cutoff(monkeypatch):
    monkeypatch.setattr(random, "random", lambda: 0.5)
    monkeypatch.setattr(random, "gauss", lambda mu, sigma: 0.0)

    ph = Photon(z=0.0, energy=1.0)
    parts = ph.interact()
    assert len(parts) == 2
    assert all(p.type == "elec" for p in parts)
    assert pytest.approx(sum(p.energy for p in parts), 1e-8) == ph.energy


def test_muon_basic_properties():
    m = Muon(z=0.0, energy=2.0)
    assert m.type == "muon"
    m.move(0.1)
    assert pytest.approx(m.z, 1e-8) == 0.1
