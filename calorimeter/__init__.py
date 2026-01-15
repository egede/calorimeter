"""
Calorimeter package for visualization and analysis of calorimeter data.

This package provides tools for:
- Visualizing energy distributions from calorimeter detectors
- Processing and analyzing calorimeter measurements
- Working with calorimeter models and simulations
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "ulrik.egede@monash.edu"

# Import main classes now located at package level
from .calorimeter import Calorimeter
from .simulation import Simulation
from .layer import Layer
from .particle import Electron, Photon, Muon


# Public API
__all__ = [
    # Model classes
    "Calorimeter",
    "Simulation",
    "Layer",
    "Electron",
    "Photon",
    "Muon",
]
