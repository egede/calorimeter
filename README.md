[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
![Tests](https://github.com/egede/calorimeter/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/egede/calorimeter/branch/main/graph/badge.svg)](https://codecov.io/gh/egede/calorimeter)
[![Binder](https://binderhub.rc.nectar.org.au/badge_logo.svg)](https://binderhub.rc.nectar.org.au/v2/gh/egede/calorimeter/HEAD?labpath=calorimeter%2Fexamples%2Fsimulate.ipynb)

# Calorimeter

A Python package for visualization and analysis of calorimeter data.

## Features

- **Create a 1D calorimenter with active and passive layers**
- **Visualise shower development**
- **Monte Carlo generation to explore resolution**

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

## Run in Binder
If you are staff or student at an Australian or New Zealand University, you can use [binder](https://binderhub.rc.nectar.org.au/v2/gh/egede/calorimeter/HEAD?labpath=calorimeter%2Fexamples%2Fsimulate.ipynb) on ARDC resources.

## Quick Start

```python
from calorimeter import Calorimeter, Simulation, Layer, Electron
import matplotlib.pyplot as plt

mycal = Calorimeter()
lead = Layer('lead', 2.0, 0.5, 0.0)
scintillator = Layer('Scin', 0.01, 0.5, 1.0)
for i in range(40):
    mycal.add_layers([lead, scintillator])

sim = Simulation(mycal)
ionisations, cal_with_traces = sim.simulate_with_tracing(Electron(0.0, 100.0), deadcellfraction=0.0)

fig, ax = plt.subplots(figsize=(14, 6))
ax = cal_with_traces.draw(ax=ax, show_traces=True)
plt.tight_layout()
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


## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE.md) file for details.

## Contributing

Contributions are welcome! Before submitting a PR:

- Install dev dependencies: `pip install -e ".[dev]"`
- Run the test suite: `pytest -q`
- Check linting and types: `flake8 calorimeter tests` and `mypy calorimeter`

### Running Tests Locally

In a fresh clone, run:

```bash
pip install -e ".[dev]"
pytest -q
```

### Pre-commit Hooks

This repository includes a shared pre-commit configuration at [.pre-commit-config.yaml](.pre-commit-config.yaml).

It will:
- Strip outputs from `*.ipynb` notebooks (via `nbstripout`).
- Apply basic hygiene checks (trailing whitespace, EOF fixer, YAML checks).

Set up locally:

```bash
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files
```

Note: pre-commit runs automatically on `git commit` after installation.

## Support

- For issues, or bug reports, please open an [issue](https://github.com/egede/calorimeter/issues) on GitHub.
- For questions and discussions, use the [discussion forum](https://github.com/egede/calorimeter/discussions).
