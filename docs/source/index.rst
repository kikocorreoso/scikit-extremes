Welcome to scikit-extremes's documentation!
===========================================

scikit-extremes is a python library to perform univariate extreme value
calculations.

There are two main classical approaches to calculate extreme values:

-  Gumbel/Generalised Extreme Value distribution (GEV) + Block Maxima.
-  Generalised Pareto Distribution (GPD) + Peak-Over-Threshold (POT).

Dependencies
------------

To work with scikit-extremes you will need the following libraries:

-  Numpy
-  Scipy
-  Matplotlib
-  Numdifftools

Installation
------------

At this moment there isn't an official release. To install the package you can
follow the next steps:

.. parsed-literal::

    # lmoments has not been updated in a while so we use the master
    # (see https://github.com/OpenHydrology/lmoments3/issues/8)
    pip install git+https://github.com/OpenHydrology/lmoments3.git

    git clone https://github.com/kikocorreoso/scikit-extremes.git

    cd scikit-extremes

    pip install -e .

Support
-------

If you find a bug, something wrong or want a new feature, please, `open
a new issue on
Github <https://github.com/kikocorreoso/scikit-extremes/issues>`__.

If you want to ask about the usage of scikit-extremes or something
related with extreme value theory/analysis with Python you can post a
question at `stackoverflow <http://stackoverflow.com/>`__ tagged with
``scikit-extremes`` or ``skextremes``.

License
-------

This software is licensed under the MIT license except:

* ``skextremes.utils.bootstrap_ci`` function that is based on the `scikits-bootstrap`_ package licensed under the Modified BSD License.

.. _scikits-bootstrap: https://github.com/cgevans/scikits-bootstrap

The MIT License (MIT)

Copyright (c) [2015] [Kiko Correoso]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Contents:
---------

.. toctree::
   :maxdepth: 2

   Small EVT introduction
   User guide
   Module utils
   Module models.wind
   Module models.engineering
   Module models.classic
