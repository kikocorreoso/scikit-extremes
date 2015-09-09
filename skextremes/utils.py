"""
This module provides utility functions that are used within scikit-extremes
that are also useful for external consumption.
"""

import warnings as _warnings

from numpy.random import randint as _randint
import numpy as _np
import scipy.stats as _st
from scipy import optimize as _op
from scipy.special import gamma as _gamma


###############################################################################
# Bootstrap confidence intervals calculations using percentile interval method
###############################################################################
class InstabilityWarning(UserWarning):
    """Issued when results may be unstable."""
    pass

# On import, make sure that InstabilityWarnings are not filtered out.
_warnings.simplefilter('always', InstabilityWarning)
_warnings.simplefilter('always', UserWarning)

def bootstrap_ci(data, statfunction=_np.average, alpha = 0.05, 
                 n_samples = 100):
    """
    Given a set of data ``data``, and a statistics function ``statfunction`` that
    applies to that data, computes the bootstrap confidence interval for
    ``statfunction`` on that data. Data points are assumed to be delineated by
    axis 0.
    
    This function has been derived and simplified from scikits-bootstrap 
    package created by cgevans (https://github.com/cgevans/scikits-bootstrap).
    All the credits shall go to him.

    **Parameters**
    
    data : array_like, shape (N, ...) OR tuple of array_like all with shape (N, ...)
        Input data. Data points are assumed to be delineated by axis 0. Beyond this,
        the shape doesn't matter, so long as ``statfunction`` can be applied to the
        array. If a tuple of array_likes is passed, then samples from each array (along
        axis 0) are passed in order as separate parameters to the statfunction. The
        type of data (single array or tuple of arrays) can be explicitly specified
        by the multi parameter.
    statfunction : function (data, weights = (weights, optional)) -> value
        This function should accept samples of data from ``data``. It is applied
        to these samples individually. 
    alpha : float, optional
        The percentiles to use for the confidence interval (default=0.05). The 
        returned values are (alpha/2, 1-alpha/2) percentile confidence
        intervals. 
    n_samples : int or float, optional
        The number of bootstrap samples to use (default=100)
        
    **Returns**
    
    confidences : tuple of floats
        The confidence percentiles specified by alpha

    **Calculation Methods**
    
    'pi' : Percentile Interval (Efron 13.3)
        The percentile interval method simply returns the 100*alphath bootstrap
        sample's values for the statistic. This is an extremely simple method of 
        confidence interval calculation. However, it has several disadvantages 
        compared to the bias-corrected accelerated method.
        
        If you want to use more complex calculation methods, please, see
        `scikits-bootstrap package 
        <https://github.com/cgevans/scikits-bootstrap>`_.


    **References**
    
        Efron (1993): 'An Introduction to the Bootstrap', Chapman & Hall.
    """

    def bootstrap_indexes(data, n_samples=10000):
        """
    Given data points data, where axis 0 is considered to delineate points, return
    an generator for sets of bootstrap indexes. This can be used as a list
    of bootstrap indexes (with list(bootstrap_indexes(data))) as well.
        """
        for _ in range(n_samples):
            yield _randint(data.shape[0], size=(data.shape[0],))    
    
    alphas = _np.array([alpha / 2,1 - alpha / 2])

    data = _np.array(data)
    tdata = (data,)
    
    # We don't need to generate actual samples; that would take more memory.
    # Instead, we can generate just the indexes, and then apply the statfun
    # to those indexes.
    bootindexes = bootstrap_indexes(tdata[0], n_samples)
    stat = _np.array([statfunction(*(x[indexes] for x in tdata)) for indexes in bootindexes])
    stat.sort(axis=0)

    # Percentile Interval Method
    avals = alphas

    nvals = _np.round((n_samples - 1)*avals).astype('int')

    if _np.any(nvals == 0) or _np.any(nvals == n_samples - 1):
        _warnings.warn("Some values used extremal samples; results are probably unstable.", InstabilityWarning)
    elif _np.any(nvals<10) or _np.any(nvals>=n_samples-10):
        _warnings.warn("Some values used top 10 low/high samples; results may be unstable.", InstabilityWarning)

    if nvals.ndim == 1:
        # All nvals are the same. Simple broadcasting
        return stat[nvals]
    else:
        # Nvals are different for each data point. Not simple broadcasting.
        # Each set of nvals along axis 0 corresponds to the data at the same
        # point in other axes.
        return stat[(nvals, _np.indices(nvals.shape)[1:].squeeze())]
        
###############################################################################
# Function to estimate parameters of GEV using method of moments
###############################################################################
def gev_momfit(data):
    """
    Estimate parameters of Generalised Extreme Value distribution using the 
    method of moments. The methodology has been extracted from appendix A.4
    on EVA (see references below).
    
    **Parameters**
    
    data : array_like
        Sample extreme data
    
    **Returns**
    
    tuple
        tuple with the shape, location and scale parameters. In this,
        case, the shape parameter is always 0.
    
    **References**
    
        DHI, (2003): '`EVA(Extreme Value Analysis - Reference manual) 
        <http://www.tnmckc.org/upload/document/wup/1/1.3/Manuals/MIKE%2011/eva/EVA_RefManual.pdf>`_', 
        DHI.
    """
            
    g = lambda n, x : _gamma(1 + n * x)
    
    mean = _np.mean(data)
    std = _np.std(data)
    skew = _st.skew(data)
    
    def minimize_skew(x):
        a = -g(3, x) + 3 * g(1, x) * g(2, x) - 2 * g(1, x)**3
        b = (g(2, x) - (g(1, x))**2)**1.5
        c = abs(a / b - skew)
        return c
        
    c = _op.fmin(minimize_skew, 0)[0] # first guess is set to 0
    scale = std * abs(c) / _np.sqrt((g(2, c) - g(1, c)**2))
    loc = mean - scale * (1 - g(1, c)) / c
    
    return c, loc, scale

###############################################################################
# Function to estimate parameters of Gumbel using method of moments
###############################################################################
def gum_momfit(data):
    """
    Estimate parameters of Gumbel distribution using the 
    method of moments. The methodology has been extracted from Wilks 
    (see references below).
    
    **Parameters**
    
    data : array_like
        Sample extreme data
    
    **Returns**
    
    tuple
        tuple with the shape, location and scale parameters. In this,
        case, the shape parameter is always 0.
        
    **References**
    
    
        Wilks,D.S. (2006): '`Statistical Methods in the Atmospheric Sciences, 
        second edition <http://store.elsevier.com/Statistical-Methods-in-the-Atmospheric-Sciences/Daniel-Wilks/isbn-9780080456225/>`_', 
        Academic Press.
    """
    
    mean = _np.mean(data)
    std = _np.std(data)
    
    euler_cte = 0.5772156649015328606065120900824024310421
    
    scale = std * _np.sqrt(6) / _np.pi    
    loc = mean - scale * euler_cte
    
    return 0, loc, scale