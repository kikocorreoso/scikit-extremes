"""
This module contains algorithms found in the literature and used extensively in 
wind energy engineering as standard methods.

For more information visit:

https://www.ecn.nl/publications/ECN-C--98-096

https://webstore.iec.ch/preview/info_iec61400-1%7Bed3.0%7Den.pdf
"""

import numpy as _np
from scipy.special import gamma as _gamma


def wind_EWTSII_Exact(vave, k, T = 50, n = 23037):
    """
    Algorithm appeared in the European Wind Turbine Standards II (EWTS II).
    Exact variation.
    
    It uses 10-minute wind speeds to obtain the return period extreme wind
    speed for the ``T`` return period defined.
    
    **Parameters**
    
    vave : float or int
        Long term mean wind speed
    k : float or int
        Weibull k parameter as defined in the wind industry. To obtain the k
        parameter using scipy `have a look here 
        <http://stackoverflow.com/questions/17481672/fitting-a-weibull-distribution-using-scipy/17498673#17498673>`_.
        The `c` parameter in scipy is the k equivalent in the wind industry.
    T : float or int
        Return period in years. Default value is 50 (years).
    n : floar or int
        the number of independent events per year. Default value is 23037 for 
        10-min time steps and 1-yr extrema.
    
    **Returns**
    
    vref : float
        Expected extreme wind speed at the return period defined.
    
    **References**
    
        Dekker JWM, Pierik JTG (1998): 'European Wind Turbine Standards II', 
        ECN-C-99-073, ECN Solar & Wind Energy, Netherlands.
    """
    a = 1. / _gamma(1. + 1. / k)
    b = - _np.log(1 - _np.exp((_np.log(1. - 1. / T)) / n))
    res = vave * a * (b ** (1. / k))
    return res
    
def wind_EWTSII_Gumbel(vave, k, T = 50, n = 23037):
    """
    Algorithm appeared in the European Wind Turbine Standards II (EWTS II).
    Gumbel variation.
    
    It uses 10-minute wind speeds to obtain the return period extreme wind
    speed for the ``T`` return period defined.
    
    **Parameters**
    
    vave : float or int
        Long term mean wind speed
    k : float or int
        Weibull k parameter as defined in the wind industry. To obtain the k
        parameter using scipy `have a look here 
        <http://stackoverflow.com/questions/17481672/fitting-a-weibull-distribution-using-scipy/17498673#17498673>`_.
        The `c` parameter in scipy is the k equivalent in the wind industry.
    T : float or int
        Return period in years. Default value is 50 (years).
    n : floar or int
        the number of independent events per year. Default value is 23037 for 
        10-min time steps and 1-yr extrema.
    
    **Returns**
    
    vref : float
        Expected extreme wind speed at the return period defined.
    
    **References**
    
        Dekker JWM, Pierik JTG (1998): 'European Wind Turbine Standards II', 
        ECN-C-99-073, ECN Solar & Wind Energy, Netherlands.
    """
    a = ((_np.log(n))**(1/k -1)) / (k*_gamma(1+1/k))
    b = k * _np.log(n) - _np.log(-_np.log(1-1/T))
    res = vave * a * b
    return res

def wind_EWTSII_Davenport(vave, k, T = 50, n = 23037):
    """
    Algorithm appeared in the European Wind Turbine Standards II (EWTS II).
    Davenport variation.
    
    It uses 10-minute wind speeds to obtain the return period extreme wind
    speed for the ``T`` return period defined.
    
    **Parameters**
    
    vave : float or int
        Long term mean wind speed
    k : float or int
        Weibull k parameter as defined in the wind industry. To obtain the k
        parameter using scipy `have a look here 
        <http://stackoverflow.com/questions/17481672/fitting-a-weibull-distribution-using-scipy/17498673#17498673>`_.
        The `c` parameter in scipy is the k equivalent in the wind industry.
    T : float or int
        Return period in years. Default value is 50 (years).
    n : floar or int
        the number of independent events per year. Default value is 23037 for 
        10-min time steps and 1-yr extrema.
    
    **Returns**
    
    vref : float
        Expected extreme wind speed at the return period defined.
    
    **References**
    
        Dekker JWM, Pierik JTG (1998): 'European Wind Turbine Standards II', 
        ECN-C-99-073, ECN Solar & Wind Energy, Netherlands.
    """
    c1 = 1 - (k - 1) / (k * _np.log(n))
    c2 = 1 + (_np.log(k * _gamma(1+1/k) * ((_np.log(n))**(1-1/k)))) / (k * _np.log(n) - k + 1)
    a = ((_np.log(n))**(1/k-1)) / (c1 * k * _gamma(1+1/k))
    b = c1 * c2 * k * _np.log(n) - _np.log(-_np.log(1-1/T))
    res = vave * a * b
    return res

def wind_vref_5vave(vave, factor = 5):
    """
    It calculates the 50 year return expected maximum wind speed as 5 times the 
    long term average wind speed.
    
    It uses 10-minute wind speeds to obtain the 50-year return period extreme 
    wind speed.
    
    **Parameters**
    
    vave : float or int
        Long term mean wind speed
    factor : float or int
        Factor used to obtain vref. Default value is 5.
    
    **Returns**
    
    vref : float
        vref wind speed, i.e., 50 years expected maximum wind speed in the same
        units used by the vave input parameter.
    """
    return float(factor) * vave
