# Calorimeter

A Python package for visualization and analysis of calorimeter data.

## Features

- **Energy Distribution Plotting**: Visualize energy measurements from calorimeter detectors
- **Multi-Distribution Comparison**: Compare multiple energy distributions side-by-side
- **Easy Integration**: Simple API for quick visualization and analysis

## Installation

### From Source

Clone the repository and install in development mode:

```bash
git clone https://github.com/yourusername/calorimeter.git
cd calorimeter
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
import numpy as np
from calorimeter import plot_energy_distribution

# Generate sample energy data
energies = np.random.gamma(shape=2, scale=50, size=1000)

# Create a plot
fig, ax = plot_energy_distribution(energies, bins=50, title="Sample Calorimeter Data")
```

## Usage Examples

### Single Distribution

```python
import matplotlib.pyplot as plt
from calorimeter import plot_energy_distribution

# Your energy data
energies = [10.5, 15.3, 12.1, 18.9, ...]

# Plot
fig, ax = plot_energy_distribution(energies, bins=40)
plt.show()
```

### Multiple Distributions

```python
from calorimeter.plotter import plot_multiple_distributions
import matplotlib.pyplot as plt

# Compare datasets
data = {
    'Detector A': [10.5, 15.3, 12.1, 18.9, ...],
    'Detector B': [11.2, 14.8, 13.5, 17.2, ...],
    'Detector C': [9.8, 16.1, 11.5, 19.3, ...],
}

fig, ax = plot_multiple_distributions(data, bins=50)
plt.show()
```

## Running Tests

Run the test suite using pytest:

```bash
pytest
```

With coverage report:

```bash
pytest --cov=calorimeter tests/
```

## Development

### Code Quality

The project uses several tools for code quality:

- **pytest**: Testing framework
- **pytest-cov**: Code coverage measurement
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Static type checking

### Running Quality Checks

```bash
# Format code
black calorimeter tests

# Run linting
flake8 calorimeter tests

# Type checking
mypy calorimeter

# Tests with coverage
pytest --cov=calorimeter tests/
```

## Project Structure

```
calorimeter/
├── calorimeter/           # Package source code
│   ├── __init__.py
│   └── plotter.py
├── tests/                 # Test directory
│   ├── __init__.py
│   ├── test_plotter.py
│   └── test_integration.py
├── .github/
│   └── workflows/         # GitHub Actions workflows
│       └── tests.yml
├── setup.py              # Package setup configuration
├── requirements.txt      # Runtime dependencies
├── requirements-dev.txt  # Development dependencies
├── README.md            # This file
└── LICENSE              # MIT License
```

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE.md) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
