"""
Setup configuration for the calorimeter package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="calorimeter",
    version="0.1.0",
    author="Ulrik Egede",
    author_email="ulrik.egede@monash.edu",
    description="A package that for education purposes creates a simple calorimeter that can be used for simulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/egede/calorimeter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.11",
    install_requires=[
        "matplotlib>=3.5.0",
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.6.0",
        ],
    },
    include_package_data=True,
    data_files=[
        ("calorimeter/examples", [
            "calorimeter/examples/simulate.ipynb",
        ]),
    ],
)
