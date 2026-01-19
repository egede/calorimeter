import numpy as np
from calorimeter import Electron


class Spectrum:
    """Class for generating particles from various energy distributions."""

    def __init__(self, particle_type=Electron, min_energy=3, max_energy=50):
        """
        Initialize the spectrum generator.

        Parameters
        ----------
        particle_type : class
            Particle class to instantiate (default: Electron)
        min_energy : float
            Minimum energy for sampling (default: 3 GeV)
        max_energy : float
            Maximum energy for sampling (default: 50 GeV)
        """
        self.particle_type = particle_type
        self.min_energy = min_energy
        self.max_energy = max_energy

    def discrete(self, n_particles, energy):
        """
        Generate particles with a discrete energy.

        Parameters
        ----------
        n_particles : int
            Number of particles to generate
        energy : float
            Energy of all particles

        Returns
        -------
        list
            List of particle objects with the specified energy

        Raises
        ------
        ValueError
            If energy is outside the range [min_energy, max_energy]
        """
        if energy < self.min_energy or energy > self.max_energy:
            raise ValueError(f"Energy {energy} is outside the allowed range [{self.min_energy}, {self.max_energy}]")
        return [self.particle_type(0.0, energy) for _ in range(n_particles)]

    def uniform(self, n_particles, seed=None):
        """
        Generate particles with uniform energy distribution.

        Parameters
        ----------
        n_particles : int
            Number of particles to generate
        seed : int or None
            Random seed for reproducibility

        Returns
        -------
        list
            List of particle objects with uniformly sampled energies
        """
        if seed is not None:
            np.random.seed(seed)

        energies = np.random.uniform(self.min_energy, self.max_energy, n_particles)
        return [self.particle_type(0.0, E) for E in energies]

    def spectrum(self, n_particles, rise_constant=8, fall_constant=30, seed=None):
        """
        Generate particles from an exponential spectrum distribution using rejection sampling.

        Parameters
        ----------
        n_particles : int
            Number of particles to generate
        rise_constant : float
            Exponential constant for the rise of the distribution (1/e power)
        fall_constant : float
            Exponential constant for the fall of the distribution (1/e power)
        seed : int or None
            Random seed for reproducibility (default: None)

        Returns
        -------
        list
            List of particle objects with sampled energies from the spectrum
        """
        if seed is not None:
            np.random.seed(seed)

        def energy_spectrum_pdf(E):
            """Compute the probability density function for the energy spectrum."""
            return (1 - np.exp(-E / rise_constant)) * np.exp(-E / fall_constant)

        # Find maximum of pdf in range for rejection sampling
        E_test = np.linspace(self.min_energy, self.max_energy, 1000)
        pdf_max = np.max(energy_spectrum_pdf(E_test))

        # Rejection sampling
        samples = []
        while len(samples) < n_particles:
            E_candidate = np.random.uniform(self.min_energy, self.max_energy)
            acceptance = energy_spectrum_pdf(E_candidate) / pdf_max
            if np.random.uniform(0, 1) < acceptance:
                samples.append(E_candidate)

        energies = np.array(samples)
        return [self.particle_type(0.0, E) for E in energies]
