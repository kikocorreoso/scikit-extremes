"""
Datasets to be used in the docs and tests.
Most of the datasets are adapted from the R ismev package.
For more information visit: 
http://cran.r-project.org/web/packages/ismev/index.html

Other datasets includes:
-harris1996 - Annual maximum wind speeds used in Harris (1996), "Gumbel 
re-visited - a new look at extreme value statistics applied to wind speeds"
"""

import os as _os

import numpy as _np

_path = _os.path.dirname(_os.path.abspath(__file__))

class _BaseDataset:
    def __init__(self, d):
        for key in d.keys():
            setattr(self, key, d[key])


class _BaseDescription:
    def __init__(self, description):
        self._description = description
    def __str__(self):
        return self._description
    def __repr__(self):
        return self._description


class _Base:
    def __init__(self, description, data, fields): 
        if data.ndim == 1:
            cols = 1
        else:
            cols = data.shape[1]
        if len(fields) != cols:
            raise ValueError(('The number of fields is not equal to') 
                             ('the number of dimensions of the input.'))
        self._data = data
        self.description = _BaseDescription(description)
        if cols == 1:
            tmpdict = {fields[0]: data}
        else:
            tmpdict = {fields[i]: data[:,i] for i in range(len(fields))}
        self.fields = _BaseDataset(tmpdict)
    
    def asarray(self):
        return self._data
        

# dowjones dataset (ismev R package)
def dowjones():
    """Return a class containing the dowjones data and description."""
    _desc = """
    Daily Closing Prices of The Dow Jones Index
    -------------------------------------------

    Fields:
    obs: numpy.array defining the observation number.
    year: numpy.array defining the year of the observation.
    damage: numpy.array defining the damage per year ('damage') in 
            bllions USD/y.

    More information on these data can be found in:
    - Pielke, R. A. Jr. and Landsea, C. W. (1998) Normalized hurricane 
    damages in the United States: 1925-95. Weather and Forecasting, 13, 
    (3), 621 - 631.
    - Katz, R. W. (2002) Stochastic modeling of hurricane damage. Journal 
    of Applied Meteorology, 41, 754–762.
  
    Source:
    http://sciencepolicy.colorado.edu/pielke/hp_roger/hurr_norm/data.html
    """
    index = _np.loadtxt(_os.path.join(_path, 'dowjones.csv'), 
                        usecols = (1,))
    date = _np.genfromtxt(_os.path.join(_path, 'dowjones.csv'), 
                          usecols = (0,), dtype = _np.str)
    data = _np.array([date.astype('datetime64[D]'), index])
    return _Base(_desc, data.T, ('date', 'index'))


# engine dataset (ismev R package)
def engine():
    """Return a class containing the engine data and description."""
    _desc = """
    Engine Failure Time Data
    ------------------------

    Fields:
     time: numpy.array defining the corrosion levels.
     Corrosion: numpy.array defining the failure times.
     
    Source:
     Unknown :-(
    """
    data = _np.loadtxt(_os.path.join(_path, 'engine.csv'))
    return _Base(_desc, data, ('time', 'corrosion'))


# euroex dataset (ismev R package)
def euroex():
    """Return a class containing the euroex data and description."""
    _desc = """
    UK/Euro Exchange Rates
    ----------------------

    Fields:
     rate: numpy.array defining the exchange rates.
     
    Source:
     Unknown :-(
    """
    data = _np.loadtxt(_os.path.join(_path, 'euroex.csv'))
    return _Base(_desc, data, ('rate',))
    
 
# exchange dataset (ismev R package)
def exchange():
    """Return a class containing the exchange data and description."""
    _desc = """
    UK/US and UK/Canada Exchange Rates
    ----------------------------------
    The dataset contain daily exchange rates, UK sterling against the US 
    dollar and UK sterling against the Canadian dollar. 

    Fields:
     dates: numpy.array defining the date for the exchange rates.
     rate_UK_US: numpy.array defining UK sterling against the US dollar
        exchange rate 
     rate_UK_CAN: numpy.array defining UK sterling against the Canadian
        dollar exchange rate
     
    Source:
     -Coles, S. G. (2001). An Introduction to Statistical Modelling of 
        Extreme Values. London: Springer.
    """

    data = _np.loadtxt(_os.path.join(_path, 'exchange.csv'), 
                       usecols = (1, 2))
    date = _np.genfromtxt(_os.path.join(_path, 'exchange.csv'), 
                          usecols = (0,), dtype = _np.str)
    data = _np.array([date.astype('datetime64[D]'), data[:,0], data[:,1]])
    return _Base(_desc, data.T, ('date', 'rate_UK_US', 'rate_UK_CAN'))


# Fremantle dataset (ismev R package)
def fremantle():
    """Return a class containing the fremantle data and description."""
    _desc = """
    Annual Maximum Sea Levels at Fremantle, Western Australia
    ---------------------------------------------------------

    Fields:
     year: numpy.array defining the year for the row data.
     sea_level: numpy.array defining annual maximum sea level recorded at
        Fremantle, Western Australia 
     SOI: numpy.array defining annual mean values of the Southern 
        Oscillation Index (SOI)
     
    Source:
     -Coles, S. G. (2001). An Introduction to Statistical Modelling of 
        Extreme Values. London: Springer.
    """
    data = _np.loadtxt(_os.path.join(_path, 'fremantle.csv'))
    return _Base(_desc, data, ('year', 'sea_level', 'SOI'))


# glass dataset (ismev R package)
def glass():
    """Return a class containing the glass data and description."""
    _desc = """
    Breaking Strengths of Glass Fibres
    ----------------------------------

    Fields:
     breaking_strength: numpy.array defining breaking strengths of 63 glass 
         fibres of length 1.5 centimetres, recorded under experimental 
         conditions.
     
    Source:
     -Smith, R. L. and Naylor, J. C. (1987) A comparison of maximum 
        likelihood and Bayesian estimators for the three-parameter Weibull 
        distribution. Applied Statistics 36, 358–396.
    """
    data = _np.loadtxt(_os.path.join(_path, 'glass.csv'))
    return _Base(_desc, data, ('breaking_strength',))


# Port Pirie dataset (ismev R package)
def portpirie():
    """Return a class containing the portpirie data and description."""
    _desc = """
    Annual Maximum Sea Levels at Port Pirie, South Australia
    --------------------------------------------------------

    Fields:
     year: numpy.array defining the year for the row data.
     sea_level: numpy.array defining annual maximum sea level recorded at
        Port Pirie, South Australia.
     
    Source:
     -Coles, S. G. (2001). An Introduction to Statistical Modelling of 
        Extreme Values. London: Springer.
    """
    data = _np.loadtxt(_os.path.join(_path, 'portpirie.csv'))
    return _Base(_desc, data, ('year', 'sea_level'))
    

# rain dataset (ismev R package)
def rain():
    """Return a class containing the rain data and description."""
    _desc = """
    Daily Rainfall Accumulations in South-West England
    --------------------------------------------------

    Fields:
     sea_level: numpy.array defining daily rainfall accumulations at a 
        location in south-west England over the period 1914 to 1962 .
     
    Source:
     -Coles, S. G. and Tawn, J. A. (1996) Modelling extremes of the areal 
        rainfall process. Journal of the Royal Statistical Society, B 53, 
        329–347.
    """
    data = _np.loadtxt(_os.path.join(_path, 'rain.csv'))
    return _Base(_desc, data, ('rain',))


# Venice dataset (ismev R package)
def venice():
    """Return a class containing the rain data and description."""
    _desc = """
    Venice sea levels
    -----------------
    The dataset contain the 10 largest sea levels observed within the year. 
    The ten largest sea levels are given for every year in the period 1931 
    to 1981, excluding 1935 in which only the six largest measurements
    are available (the rest are 'numpy.nan').

    Fields:
     year: numpy.array defining the year for the row data.
     r01: numpy.array defining annual sea level maxima.
     r02: numpy.array defining the second sea level.
     r03: numpy.array defining the third sea level.
     r04: numpy.array defining the fourth sea level.
     r05: numpy.array defining the fifth sea level.
     r06: numpy.array defining the sixth sea level.
     r07: numpy.array defining the seventh sea level.
     r08: numpy.array defining the eigth sea level.
     r09: numpy.array defining the ninth sea level.
     r10: numpy.array defining the tenth sea level.
     
    Source:
     -Smith, R. L. (1986) Extreme value theory based on the r largest annual
        events. Journal of Hydrology, 86, 27–43.
    """
    data = _np.genfromtxt(_os.path.join(_path, 'venice.csv'),
                          missing_values = 'NA', 
                          filling_values = _np.nan)
    return _Base(_desc, data, ('year', 
                               'r01', 'r02', 'r03', 'r04', 'r05',
                               'r06', 'r07', 'r08', 'r09', 'r10'))


# wavesurge dataset (ismev R package)
def wavesurge():
    """Return a class containing the wavesurge data and description."""
    _desc = """
    Wave and Surge Heights in South-West England
    --------------------------------------------

    Fields:
     wave: numpy.array defining wave heights.
     surge: numpy.array defining surge heights.
     
    Source:
     -Coles, S. G. (2001). An Introduction to Statistical Modelling of 
        Extreme Values. London: Springer.
    """
    data = _np.loadtxt(_os.path.join(_path, 'wavesurge.csv'))
    return _Base(_desc, data, ('wave', 'surge'))


# Wind dataset (ismev R package)
def wind():
    """Return a class containing the wind data and description."""
    _desc = """
    Annual Maximum Wind Speeds at Albany and Hartford
    -------------------------------------------------

    Fields:
     year: numpy.array defining the year for the row data.
     hartford: numpy.array defining annual maximum wind speeds at Hartford
     albany: numpy.array defining annual maximum wind speeds at Albany
     
    Source:
     -Coles, S. G. (2001). An Introduction to Statistical Modelling of 
        Extreme Values. London: Springer.
    """
    data = _np.loadtxt(_os.path.join(_path, 'wind.csv'))
    return _Base(_desc, data, ('year', 'hartford', 'albany'))


# Wooster dataset (ismev R package)
def wooster():
    """Return a class containing the wooster data and description."""
    _desc = """
    Minimum Temperatures at Wooster, Ohio
    -------------------------------------

    Fields:
     temp: numpy.array defining daily minimum temperatures, in degrees 
        Fahrenheit, at Wooster, Ohio, over the period 1983 to 1988.
     
    Source:
     -Coles, S. G., Tawn, J. A. and Smith, R. L. (1994) A seasonal Markov 
        model for extremely low temperatures. Environmetrics 5, 221–239.
    """
    data = _np.loadtxt(_os.path.join(_path, 'wooster.csv'))
    return _Base(_desc, data, ('wooster',))


# Harris 1996 dataset
def harris1996():
    """Return a class containing the dataset used in Harris1996."""
    _desc = """
    Maximum hourly wind speed at Honington Station, UK
    --------------------------------------------------

    Fields:
     temp: numpy.array defining maximum hourly wind speed per year, in knots , 
         at Honington station, UK, over the period 1970 to 1990.
     
    Source:
     -Harris, R. I. (1996) "Gumbel re-visited - a new look at extreme value 
         statistics applied to wind speeds". Journal of Wind Engineering and
         Industrial Arodynamics 59, 1–22.
    """
    data = _np.sqrt(_np.array([610.5, 424.0, 382.6, 382.6, 382.6, 362.8, 343.4, 
                               324.6, 306.3, 288.6, 288.6, 288.6, 288.6, 271.3,
                               271.3, 254.7, 254.7, 238.5, 207.8, 207.8, 193.2]))
    return _Base(_desc, data, ('harris1996',))
