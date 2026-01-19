import pytest
import numpy as np

from calorimeter import Electron
from calorimeter.spectrum import Spectrum


def test_spectrum_initialization_defaults():
    """Test that Spectrum initializes with default values."""
    spectrum = Spectrum()
    assert spectrum.particle_type == Electron
    assert spectrum.min_energy == 3
    assert spectrum.max_energy == 50


def test_spectrum_initialization_custom():
    """Test that Spectrum initializes with custom values."""
    spectrum = Spectrum(particle_type=Electron, min_energy=5, max_energy=100)
    assert spectrum.particle_type == Electron
    assert spectrum.min_energy == 5
    assert spectrum.max_energy == 100


def test_discrete_generates_correct_number_of_particles():
    """Test that discrete method generates the correct number of particles."""
    spectrum = Spectrum()
    particles = spectrum.discrete(n_particles=10, energy=25.0)
    assert len(particles) == 10


def test_discrete_all_particles_have_same_energy():
    """Test that all particles from discrete method have the specified energy."""
    spectrum = Spectrum()
    energy = 25.0
    particles = spectrum.discrete(n_particles=10, energy=energy)
    for particle in particles:
        assert pytest.approx(particle.energy, 1e-8) == energy


def test_discrete_particles_are_correct_type():
    """Test that discrete method generates particles of the correct type."""
    spectrum = Spectrum(particle_type=Electron)
    particles = spectrum.discrete(n_particles=5, energy=10.0)
    for particle in particles:
        assert particle.type == "elec"


def test_discrete_particles_start_at_z_zero():
    """Test that discrete method particles start at z=0."""
    spectrum = Spectrum()
    particles = spectrum.discrete(n_particles=5, energy=10.0)
    for particle in particles:
        assert pytest.approx(particle.z, 1e-8) == 0.0


def test_uniform_generates_correct_number_of_particles():
    """Test that uniform method generates the correct number of particles."""
    spectrum = Spectrum()
    particles = spectrum.uniform(n_particles=20, seed=42)
    assert len(particles) == 20


def test_uniform_energies_within_range():
    """Test that uniform method generates energies within the specified range."""
    spectrum = Spectrum(min_energy=10, max_energy=30)
    particles = spectrum.uniform(n_particles=100, seed=42)
    for particle in particles:
        assert particle.energy >= 10
        assert particle.energy <= 30


def test_uniform_energies_are_distributed():
    """Test that uniform method generates a distribution of energies."""
    spectrum = Spectrum(min_energy=10, max_energy=30)
    particles = spectrum.uniform(n_particles=100, seed=42)
    energies = [p.energy for p in particles]
    # With 100 particles uniformly distributed, we expect decent spread
    assert np.std(energies) > 1.0  # Should have some variance
    assert len(set(energies)) > 50  # Most energies should be unique


def test_uniform_seed_reproducibility():
    """Test that uniform method produces same results with same seed."""
    spectrum = Spectrum(min_energy=5, max_energy=50)
    particles1 = spectrum.uniform(n_particles=10, seed=123)
    particles2 = spectrum.uniform(n_particles=10, seed=123)

    for p1, p2 in zip(particles1, particles2):
        assert pytest.approx(p1.energy, 1e-8) == p2.energy


def test_uniform_particles_are_correct_type():
    """Test that uniform method generates particles of the correct type."""
    spectrum = Spectrum(particle_type=Electron)
    particles = spectrum.uniform(n_particles=5, seed=42)
    for particle in particles:
        assert particle.type == "elec"


def test_spectrum_generates_correct_number_of_particles():
    """Test that spectrum method generates the correct number of particles."""
    spectrum = Spectrum()
    particles = spectrum.spectrum(n_particles=50, rise_constant=8, fall_constant=30, seed=42)
    assert len(particles) == 50


def test_spectrum_energies_within_range():
    """Test that spectrum method generates energies within the specified range."""
    spectrum = Spectrum(min_energy=5, max_energy=40)
    particles = spectrum.spectrum(n_particles=100, rise_constant=8, fall_constant=30, seed=42)
    for particle in particles:
        assert particle.energy >= 5
        assert particle.energy <= 40


def test_spectrum_seed_reproducibility():
    """Test that spectrum method produces same results with same seed."""
    spectrum = Spectrum(min_energy=3, max_energy=50)
    particles1 = spectrum.spectrum(n_particles=20, rise_constant=8, fall_constant=30, seed=456)
    particles2 = spectrum.spectrum(n_particles=20, rise_constant=8, fall_constant=30, seed=456)

    for p1, p2 in zip(particles1, particles2):
        assert pytest.approx(p1.energy, 1e-8) == p2.energy


def test_spectrum_particles_are_correct_type():
    """Test that spectrum method generates particles of the correct type."""
    spectrum = Spectrum(particle_type=Electron)
    particles = spectrum.spectrum(n_particles=10, rise_constant=8, fall_constant=30, seed=42)
    for particle in particles:
        assert particle.type == "elec"


def test_spectrum_different_constants_produce_different_distributions():
    """Test that different constants produce different energy distributions."""
    spectrum = Spectrum(min_energy=5, max_energy=50)

    # Generate with different constants
    particles1 = spectrum.spectrum(n_particles=100, rise_constant=5, fall_constant=20, seed=42)
    particles2 = spectrum.spectrum(n_particles=100, rise_constant=10, fall_constant=40, seed=42)

    energies1 = [p.energy for p in particles1]
    energies2 = [p.energy for p in particles2]

    # Distributions should be different
    assert np.mean(energies1) != pytest.approx(np.mean(energies2), abs=1.0)


def test_spectrum_particles_start_at_z_zero():
    """Test that spectrum method particles start at z=0."""
    spectrum = Spectrum()
    particles = spectrum.spectrum(n_particles=5, rise_constant=8, fall_constant=30, seed=42)
    for particle in particles:
        assert pytest.approx(particle.z, 1e-8) == 0.0


def test_discrete_with_zero_particles():
    """Test that discrete method handles zero particles."""
    spectrum = Spectrum()
    particles = spectrum.discrete(n_particles=0, energy=10.0)
    assert len(particles) == 0


def test_uniform_with_zero_particles():
    """Test that uniform method handles zero particles."""
    spectrum = Spectrum()
    particles = spectrum.uniform(n_particles=0, seed=42)
    assert len(particles) == 0


def test_spectrum_with_zero_particles():
    """Test that spectrum method handles zero particles."""
    spectrum = Spectrum()
    particles = spectrum.spectrum(n_particles=0, rise_constant=8, fall_constant=30, seed=42)
    assert len(particles) == 0


def test_spectrum_default_constants():
    """Test that spectrum method uses default constants when not specified."""
    spectrum = Spectrum()
    particles = spectrum.spectrum(n_particles=10, seed=42)
    assert len(particles) == 10
    # Should complete without error using default rise_constant=8, fall_constant=30


def test_discrete_energy_below_min_raises_error():
    """Test that discrete method raises ValueError when energy is below min_energy."""
    spectrum = Spectrum(min_energy=10, max_energy=50)
    with pytest.raises(ValueError, match=r"Energy .* is outside the allowed range"):
        spectrum.discrete(n_particles=5, energy=5.0)


def test_discrete_energy_above_max_raises_error():
    """Test that discrete method raises ValueError when energy is above max_energy."""
    spectrum = Spectrum(min_energy=10, max_energy=50)
    with pytest.raises(ValueError, match=r"Energy .* is outside the allowed range"):
        spectrum.discrete(n_particles=5, energy=60.0)


def test_discrete_energy_at_boundaries_succeeds():
    """Test that discrete method accepts energies at the min and max boundaries."""
    spectrum = Spectrum(min_energy=10, max_energy=50)
    particles_min = spectrum.discrete(n_particles=3, energy=10.0)
    particles_max = spectrum.discrete(n_particles=3, energy=50.0)
    assert len(particles_min) == 3
    assert len(particles_max) == 3
    assert all(p.energy == 10.0 for p in particles_min)
    assert all(p.energy == 50.0 for p in particles_max)
