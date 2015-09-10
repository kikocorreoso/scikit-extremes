
Quick and incomplete Extreme Value Theory introduction
======================================================

Extreme Value Theory (EVT) is unique as a statistical discipline in that
it develops techniques and models for describing the unusual rather than
the usual, e.g., it is focused in the tail of the distribution.

By definition, extreme values are scarce, meaning that estimates are
often required for levels of a process that are much greater than have
already been observed. This implies an extrapolation from an small set
of observed levels to unobserved levels. Extreme Value Theory provides
models to enable such extrapolation.

Fields of interest
------------------

Applications of extreme value theory include predicting the probability
distribution of:

-  Several engineering design processes:
-  Hydraulics engineering (extreme floods,...)
-  Structural engineering (earthquakes, wind speed,...)

-  Meteorology
-  Extreme temperatures, rainfall, Hurricanes...

-  Ocean engineering
-  The size of freak waves (wave height)

-  Environmental sciences
-  Large wildfires
-  Environmental loads on structures

-  Insurance industry
-  The amounts of large insurance losses, portfolio adjustment,...

-  Financial industry
-  Equity risks
-  Day to day market risk
-  Stock market crashes

-  Material sciences
-  Corrosion analysis
-  Strenght of materials

-  Telecommunications
-  Traffic prediction

-  Biology
-  Mutational events during evolution
-  Memory cell failure

-  ...

A brief history of Extreme Value Theory
---------------------------------------

One of the earliest books on the statistics of extreme values is `E.J.
Gumbel
(1958) <http://www.worldcat.org/title/statistics-of-extremes/oclc/180577>`__.
Research into extreme values as a subject in it’s own right began
between 1920 and 1940 when work by E.L. Dodd, M. Frêchet, E.J. Gumbel,
R. von Mises and L.H.C. Tippett investigated the asymptotic distribution
of the largest order statistic. This led to the main theoretical result:
the `Extremal Types
Theorem <http://www.statslab.cam.ac.uk/~rjs57/ExtremalTThm.pdf>`__ (also
known as the Fisher–Tippett–Gnedenko theorem, the Fisher–Tippett theorem
or the extreme value theorem) which was developed in stages by `Fisher,
Tippett and von Mises, and eventually proved in general by B. Gnedenko
in
1943 <https://en.wikipedia.org/wiki/Fisher%E2%80%93Tippett%E2%80%93Gnedenko_theorem>`__.

Until 1950, development was largely theoretical. In 1958, Gumbel started
applying theory to problems in engineering. In the 1970s, `L. de Haan,
Balkema and J. Pickands generalised the theoretical
results <https://en.wikipedia.org/wiki/Pickands%E2%80%93Balkema%E2%80%93de_Haan_theorem>`__
(the second theorem in extreme value theory), giving a better basis for
statistical models.

Since the 1980s, methods for the application of Extreme Value Theory
have become much more widespread.

General approaches to estimate extreme values
---------------------------------------------

There are two primary approaches to analyzing extremes of a dataset:

-  The first and more classical approach reduces the data considerably
   by taking maxima of long blocks of data, e.g., annual maxima. The
   generalized extreme value (GEV) distribution function has theoretical
   justification for fitting to block maxima of data.

-  The second approach is to analyze excesses over a high threshold. For
   this second approach the generalized Pareto (GP) distribution
   function has similar justification for fitting to excesses over a
   high threshold.

Block-Maxima + Generalised Extreme Value (GEV) and Gumbel distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The generalized extreme value (GEV) family of distribution functions has
theoretical support for fitting to block maximum data whereby the blocks
are sufficiently large, and is given by:

.. math:: G(z;\mu, \sigma, \xi) = exp\{-[1+\xi\frac{z - \mu}{\sigma}]^{-1/\xi}\}

The parameters :math:`\mu` (:math:`-\infty < \mu < \infty`),
:math:`\sigma` (:math:`\sigma > 0`) and :math:`\xi`
(:math:`\infty < \xi < \infty`) are location, scale and shape
parameters, respectively. The value of the shape parameter :math:`\xi`
differentiates between the three types of extreme value distribution in
`Extremal Types
Theorem <http://www.statslab.cam.ac.uk/~rjs57/ExtremalTThm.pdf>`__ (also
known as the Fisher–Tippett–Gnedenko theorem, the Fisher–Tippett theorem
or the extreme value theorem).

-  :math:`\xi = 0`, leading to, corresponds to the Gumbel distribution
   (type I). This special case can be formulated as

.. math:: G(z;\mu, \sigma) = exp\{-exp(\frac{z - \mu}{\sigma})\}

-  :math:`\xi > 0` correspond to the Frêchet (type II) and

-  :math:`\xi < 0` correspond to the Weibull (type III)

distributions respectively. In practice, when we estimate the shape
parameter :math:`\xi`, the standard error for :math:`\xi` accounts for
our uncertainty in choosing between the three models.

Peak-Over-Threshold (POT) + Generalised Pareto (GP) distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**TODO**

**TODO**

**TODO**

**TODO**

References used to prepare this section
---------------------------------------

-  `S. Coles (2001): *An introduction to statistical modelling of
   extreme values*.
   Springer. <http://www.springer.com/us/book/9781852334598>`__

-  `E. Gilleland, , M. Ribatet and A. G. Stephenson (2013): *A software
   review for extreme value analysis*. Extremes, 16 (1), 103 -
   119. <http://www.springerlink.com/openurl.asp?genre=article&id=doi:10.1007/s10687-012-0155-0>`__

-  `L. Fawcett (2013): *Teaching materials of MAS8391 at Newcastle
   University
   (UK)*. <http://www.mas.ncl.ac.uk/~nlf8/teaching/mas8391/>`__
