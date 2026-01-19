"""
Setup configuration for the calorimeter package.
"""

from setuptools import setup, find_packages


def read_requirements(filename):
    """Read requirements from a file, excluding comments and -r directives."""
    with open(filename, "r", encoding="utf-8") as fh:
        lines = []
        for line in fh:
            line = line.strip()
            # Skip empty lines, comments, and -r directives
            if line and not line.startswith("#") and not line.startswith("-r"):
                lines.append(line)
        return lines


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="calorimeter",
    version="1.0.0",
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
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.11",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
    },
    include_package_data=True,
    data_files=[
        ("calorimeter/examples", [
            "calorimeter/examples/simulate.ipynb",
            "calorimeter/examples/test.ipynb",
        ]),
    ],
)
