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


def test_base_particle_interact_returns_self():
    """Test that base Particle interact method returns list with itself."""
    p = Particle(type="test", z=0.0, energy=1.0, ionise=False, cutoff=0.1)
    result = p.interact()
    assert len(result) == 1
    assert result[0] is p


def test_electron_interact_below_cutoff_returns_empty():
    """Test that electron with energy below cutoff doesn't interact."""
    e = Electron(z=0.0, energy=0.005)  # Below cutoff of 0.01
    parts = e.interact()
    assert len(parts) == 0


def test_photon_interact_below_cutoff_returns_empty():
    """Test that photon with energy below cutoff doesn't interact."""
    ph = Photon(z=0.0, energy=0.005)  # Below cutoff of 0.01
    parts = ph.interact()
    assert len(parts) == 0


def test_electron_interact_energy_conservation(monkeypatch):
    """Test that electron interaction conserves energy for various splits."""
    monkeypatch.setattr(random, "gauss", lambda mu, sigma: 0.0)

    for split_value in [0.1, 0.3, 0.5, 0.7, 0.9]:
        monkeypatch.setattr(random, "random", lambda: split_value)
        e = Electron(z=0.0, energy=10.0)
        parts = e.interact()
        assert pytest.approx(sum(p.energy for p in parts), 1e-8) == e.energy


def test_photon_interact_energy_conservation(monkeypatch):
    """Test that photon interaction conserves energy for various splits."""
    monkeypatch.setattr(random, "gauss", lambda mu, sigma: 0.0)

    for split_value in [0.1, 0.3, 0.5, 0.7, 0.9]:
        monkeypatch.setattr(random, "random", lambda: split_value)
        ph = Photon(z=0.0, energy=10.0)
        parts = ph.interact()
        assert pytest.approx(sum(p.energy for p in parts), 1e-8) == ph.energy


def test_electron_interact_preserves_position():
    """Test that electron interaction creates particles at same position."""
    e = Electron(z=5.0, energy=1.0, x=2.5, y=3.5)
    parts = e.interact()
    assert all(p.z == 5.0 for p in parts)
    assert all(p.x == 2.5 for p in parts)
    assert all(p.y == 3.5 for p in parts)


def test_photon_interact_preserves_position():
    """Test that photon interaction creates particles at same position."""
    ph = Photon(z=5.0, energy=1.0, x=2.5, y=3.5)
    parts = ph.interact()
    assert all(p.z == 5.0 for p in parts)
    assert all(p.x == 2.5 for p in parts)
    assert all(p.y == 3.5 for p in parts)


def test_electron_interact_applies_scattering(monkeypatch):
    """Test that electron interaction applies random scattering angles."""
    monkeypatch.setattr(random, "random", lambda: 0.5)

    # Mock gauss to return predictable values
    call_count = [0]
    def mock_gauss(mu, sigma):
        call_count[0] += 1
        return 0.01 if call_count[0] % 2 == 1 else -0.01

    monkeypatch.setattr(random, "gauss", mock_gauss)

    e = Electron(z=0.0, energy=1.0, angle_x=0.1, angle_y=0.2)
    parts = e.interact()

    # Both particles should have modified angles
    for p in parts:
        assert p.angle_x != e.angle_x or p.angle_y != e.angle_y


def test_photon_interact_applies_scattering(monkeypatch):
    """Test that photon interaction applies random scattering angles."""
    monkeypatch.setattr(random, "random", lambda: 0.5)

    # Mock gauss to return predictable values
    call_count = [0]
    def mock_gauss(mu, sigma):
        call_count[0] += 1
        return 0.01 if call_count[0] % 2 == 1 else -0.01

    monkeypatch.setattr(random, "gauss", mock_gauss)

    ph = Photon(z=0.0, energy=1.0, angle_x=0.1, angle_y=0.2)
    parts = ph.interact()

    # Both particles should have modified angles
    for p in parts:
        assert p.angle_x != ph.angle_x or p.angle_y != ph.angle_y


def test_electron_interact_copies_trace():
    """Test that electron interaction copies the particle trace."""
    e = Electron(z=0.0, energy=1.0)
    e.trace = [(0.0, 0.0, 0.0), (0.5, 0.1, 0.1)]
    parts = e.interact()

    # Each new particle should have a copy of the trace
    for p in parts:
        assert p.trace == e.trace
        assert p.trace is not e.trace  # Should be a copy, not same object


def test_photon_interact_copies_trace():
    """Test that photon interaction copies the particle trace."""
    ph = Photon(z=0.0, energy=1.0)
    ph.trace = [(0.0, 0.0, 0.0), (0.5, 0.1, 0.1)]
    parts = ph.interact()

    # Each new particle should have a copy of the trace
    for p in parts:
        assert p.trace == ph.trace
        assert p.trace is not ph.trace  # Should be a copy, not same object


def test_muon_interact_returns_empty():
    """Test that muon doesn't interact (no interact method override)."""
    m = Muon(z=0.0, energy=10.0)
    # Muon doesn't override interact, so it inherits from Particle
    # which returns [self]
    result = m.interact()
    assert len(result) == 1
    assert result[0] is m


def test_particle_str_formatting():
    """Test that particle __str__ formats correctly."""
    p = Particle(type="test", z=1.234, energy=5.678, ionise=True, cutoff=0.1)
    result = str(p)
    # Format: '{type:10} z:{z:.3f} E:{energy:.3f}'
    assert "test" in result
    assert "z:1.234" in result
    assert "E:5.678" in result


def test_electron_str_formatting():
    """Test that electron __str__ formats correctly."""
    e = Electron(z=2.456, energy=3.789)
    result = str(e)
    assert "elec" in result
    assert "z:2.456" in result
    assert "E:3.789" in result


def test_photon_str_formatting():
    """Test that photon __str__ formats correctly."""
    ph = Photon(z=0.999, energy=7.654)
    result = str(ph)
    assert "phot" in result
    assert "z:0.999" in result
    assert "E:7.654" in result


def test_muon_str_formatting():
    """Test that muon __str__ formats correctly."""
    m = Muon(z=5.555, energy=10.101)
    result = str(m)
    assert "muon" in result
    assert "z:5.555" in result
    assert "E:10.101" in result


def test_str_rounding_precision():
    """Test that __str__ rounds to 3 decimal places."""
    p = Particle(type="test", z=1.23456, energy=9.87654, ionise=True, cutoff=0.1)
    result = str(p)
    # Should be rounded to 3 decimal places
    assert "z:1.235" in result  # Rounded up from 1.23456
    assert "E:9.877" in result  # Rounded up from 9.87654
