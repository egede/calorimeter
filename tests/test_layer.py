import random
import pytest

from calorimeter.layer import Layer
from calorimeter.particle import Electron, Photon, Particle


def test_layer_ionise_increments_for_ionising_particle():
    layer = Layer(name="active", material=0.0, thickness=1.0, response=2.0)
    p = Particle(type="t", z=0.0, energy=1.0, ionise=True, cutoff=0.1)
    layer.ionise(p, step=0.5)
    assert pytest.approx(layer._ionisation, 1e-8) == 1.0


def test_layer_interact_no_interaction_when_random_high(monkeypatch):
    layer = Layer(name="mat", material=0.5, thickness=1.0, response=1.0)
    p = Particle(type="t", z=0.0, energy=1.0, ionise=True, cutoff=0.1)

    # Force no interaction: random >= material * step
    monkeypatch.setattr(random, "random", lambda: 1.0)
    out = layer.interact(p, step=0.5)
    assert out == [p]


def test_layer_interact_triggers(monkeypatch):
    layer = Layer(name="mat", material=1.0, thickness=1.0, response=1.0)
    e = Electron(z=0.0, energy=1.0)

    # Force interaction
    monkeypatch.setattr(random, "random", lambda: 0.0)
    monkeypatch.setattr(random, "gauss", lambda mu, sigma: 0.0)

    out = layer.interact(e, step=0.5)
    # Electron either radiates a photon and itself
    assert len(out) in (1, 2)


def test_layer_get_name():
    """Test the getter for layer name."""
    layer = Layer(name="TestLayer", material=0.5, thickness=1.0, response=1.0)
    assert layer.get_name() == "TestLayer"


def test_layer_get_material():
    """Test the getter for layer material."""
    layer = Layer(name="TestLayer", material=0.5, thickness=1.0, response=1.0)
    assert layer.get_material() == 0.5


def test_layer_get_thickness():
    """Test the getter for layer thickness."""
    layer = Layer(name="TestLayer", material=0.5, thickness=1.0, response=1.0)
    assert layer.get_thickness() == 1.0


def test_layer_get_response():
    """Test the getter for layer response."""
    layer = Layer(name="TestLayer", material=0.5, thickness=1.0, response=1.0)
    assert layer.get_yield() == 1.0
