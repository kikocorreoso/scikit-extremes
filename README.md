# scikit-extremes

Basic statistical package to perform univariate extreme value calculations
using Python

# Docs

Documentation can be found [here](https://scikit-extremes.readthedocs.io/en/latest/).

# Installation

To install the package you can follow the next steps:

    # lmoments has not been updated in a while so we use the master 
    # (see https://github.com/OpenHydrology/lmoments3/issues/8)
    pip install git+https://github.com/OpenHydrology/lmoments3.git
    
    git clone https://github.com/kikocorreoso/scikit-extremes.git

    cd scikit-extremes

    pip install -e .

# Dependencies

* Python >= 3.6
* Numpy
* Scipy >= 1.0
* Matplotlib
* NumDiffTools >= 0.9.20
* lmoments3

# WIP

This is work in progress and at its current state only some models can be used:

### Gumbel.
### Generalised Extreme Value (GEV).
### Other functionality related mainly with the wind industry.

# To-Do

### Add GPD.
### Add Bayesian inference.
### Point process?
### Improve matplotlib figures.
### Add pandas as a dependency to work with dates.
### Add Mean Residual Life Plot.
### Add statistical tests.

# Issues

[In case you find a bug, please, open an issue](https://github.com/kikocorreoso/scikit-extremes/issues).
 You can also use the issues to propose more features or enhancements.