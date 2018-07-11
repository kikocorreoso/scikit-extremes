"""
This module contains algorithms found in the literature and used extensively in 
some fields.

The following paragraphs have been adapted from 
`Makonnen, 2006 <http://journals.ametsoc.org/doi/pdf/10.1175/JAM2349.1>`_

The return period of an event of a specific large magnitude is of fundamental 
interest. All evaluations of the risks of extreme events require methods to 
statistically estimate their return periods from the measured data. Such
methods are widely used in building codes and regulations concerning the design 
of structures and community planning, as examples. Furthermore, it is crucial 
for the safety and economically optimized engineering of future communities to 
be able to estimate the changes in the frequency of various natural hazards 
with climatic change, and analyzing trends in the weather extremes.

The return period :math:`R` (in years) of an event is related to the 
probability :math:`P` of not exceeding this event in one year by

.. math:: R=\\frac{1}{1 - P}

A  standard  method  to  estimate :math:`R` from  measured data is the 
following. One first ranks the data, typically annual extremes or values over a 
threshold, in increasing order of magnitude from the smallest :math:`m = 1` to 
the largest :math:`m = N` and associates a cumulative probability :math:`P` to  
each  of  the mth  smallest  values.  Second,  one  fits  a line  to  the  
ranked  values  by  some  fitting  procedure. Third, one interpolates or 
extrapolates from the graph so that the return period of the extreme value of 
interest is estimated.

Basically, this extreme value analysis method, introduced by Hazen (1914), can 
be applied directly by using arithmetic paper. However, interpolation and 
extrapolation can be made more easily when the points fall on a straight line, 
which is rarely the case in an order-ranked plot of a physical variable on 
arithmetic paper. Therefore, almost invariably, the analysis is made by 
modifying the scale of the probability :math:`P`, and sometimes also that of 
the random variable :math:`x`, in such a way that the plot against :math:`x` of 
the anticipated cumulative distribution function :math:`P = F(x)` of the 
variable appears as a straight line. Typically, the Gumbel probability paper 
(Gumbel  1958) is used because  in many cases the distribution of the extremes, 
each selected from r events, asymptotically approaches the Gumbel distribution 
when :math:`r` goes to infinity.
"""

from scipy import integrate as _integrate
import numpy as _np
from scipy import stats as _st
import matplotlib.pyplot as _plt

_fact = _np.math.factorial

docstringbase = """
    Calculate extreme values based on yearly maxima using {0} plotting 
    positions and a least square fit.
    
    This methodology differ from others in the module in the location of the 
    probability plotting position.
    
    **Parameters**
    
    data : array_like
        Extreme values dataset.
    preconditioning : int or float
        You can choose to apply an exponent to the extreme data values before 
        performing the Gumbel curve fit. Preconditioning can often improve the 
        convergence of the curve fit and therefore improve the estimate T-year 
        extreme wind speed. Default value is 1.
    
    **Attributes**

    results : dict
        A dictionary containing different parameters of the fit.
    c : float
        Value of the 'shape' parameter. In the case of the Gumbel distribution
        this value is always 0.        
    loc : float
        Value of the 'localization' parameter.
    scale : float
        Value os the 'scale' parameter.
    distr : frozen ``scipy.stats.gumbel_r`` distribution
        Frozen distribution of type ``scipy.stats.gumbel_r`` with ``c``,
        ``loc`` and ``scale`` parameters equal to ``self.c``, ``self.loc``
        and ``self.scale``, respectively.
    
    **Methods**

    Methods to calculate the fit:
    
        {1}
    
    Methods to plot results:

        self.plot_summary()
    """

class _GumbelBase:
    def __init__(self, preconditioning = 1, ppp = None, **kwargs):
        super().__init__(**kwargs)        
        self.preconditioning = preconditioning
        self.ppp = None
        self.results = {}
    
    
    def plot_summary(self):
        """
        Summary plot including PP plot, QQ plot, empirical and fitted pdf and
        return values and periods.
        
        **Returns**
        
        4-panel plot including PP, QQ, pdf and return level plots
        """
        # data to be used
        x = self.results['data']
        extremes = self.results['Values for return period from 2 to 100 years']
        Y = self.results['Y']
        slope = self.results['slope']
        offset = self.results['offset']
        how = self.ppp
        xmin = _np.min(x)
        xmax = _np.max(x)
        
        # figure settings
        fig, (ax1, ax2, ax3) = _plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(how)
        
        # Plot the fit
        ax1.plot([xmin, xmax], 
                 [(xmin - offset) / slope, (xmax - offset) / slope],
                 '-', color = '0.25', lw = 2, alpha = 0.5)
        ax1.scatter(x, Y, 
                    facecolor = (0.7,0.7,1), color = '0', 
                    s= 50, linewidths = 1)   
        ax1.set_ylabel('$-ln(-ln(P))$')
        ax1.set_xlabel('$Extreme\ values$')
        
        # plot the return period
        ax2.plot(_np.arange(2,101), extremes)
        ax2.set_xlabel('$T (years)$')
        ax2.set_ylabel('$Extreme\ values$')
        
        # plot the distribution
        _x = _np.linspace(self.distr.ppf(0.001), self.distr.ppf(0.999), 100)
        ax3.hist(x,  
                 density = True, alpha = 0.2)
        ax3.plot(_x, self.distr.pdf(_x), label = 'Fitted', color = 'k')
        desf = xmax * 0.1
        ax3.set_xlim(xmin - desf, xmax + desf)
        ax3.set_ylabel('$Probability$')
        ax3.set_xlabel('$Extreme\ values$')
    
        return fig, ax1, ax2, ax3
        
class Harris1996(_GumbelBase):
    __doc__ = docstringbase.format('Harris1996', '_ppp_harris1996')
    
    def __init__(self, data = None, ppp = "Harris1996", **kwargs):
        super().__init__(**kwargs)
        try:
            self.data = data
            self.N = len(self.data)
            self.ppp = ppp
            self._ppp_harris1996()
        except:
            raise Exception('You should provide some data.')
        
    
    #ppp stands for probability plotting position
    def _ppp_harris1996(self):
        """
        Review of the traditional Gumbel extreme value method for analysing yearly
        maximum windspeeds or similar data, with a view to improving the 
        process. An improved set of plotting positions based on the mean values of 
        the order statistics are derived, together with a means of obtaining the 
        standard deviation of each position. This enables a fitting procedure using 
        weighted least squares to be adopted, which gives results similar to the 
        traditional Lieblein BLUE process, but with the advantages that it does not 
        require tabulated coefficients, is available for any number of data up to at 
        least 50, and provides a quantitative measure of goodness of fit.
        
        **References**
        
            Harris RI, (1996), 'Gumbel re-visited -- a new look at extreme value 
            statistics applied to wind speeds', Journal of Wind Engineering and 
            Industrial Aerodynamics, 59, 1-22. 
        """
        data = _np.sort(self.data)[::-1]
        data = data ** self.preconditioning
        N = self.N
        
        ymean = _np.empty(N)
        ymean2 = _np.empty(N)
        variance = _np.empty(N)
        weight = _np.empty(N)

        def integ_ymean(x, N, NU): 
            return -_np.log(-_np.log(x)) * (x** (N-NU)) * ((1-x)**(NU-1))
        def integ_ymean2(x, N, NU):
            return ((-_np.log(-_np.log(x)))**2) * (x** (N-NU)) * ((1-x)**(NU-1))

        for NU in range(1, N+1):
            # calculation of ymean
            a = _fact(N)/(_fact(NU - 1) * _fact(N - NU))
            b, err = _integrate.quad(integ_ymean, 0, 1, args = (N, NU))
            ymean[NU-1] = a * b
            # calculation of ymean2
            b, err = _integrate.quad(integ_ymean2, 0, 1, args = (N, NU))
            ymean2[NU-1] = a * b
            # calculation of variance
            variance[NU-1] = _np.sqrt((ymean2[NU-1] - ymean[NU-1]**2))

        # calculation of weights
        denominator = _np.sum(1/variance**2)
        for NU in range(1, N+1):
            weight[NU-1] = (1 / variance[NU-1]**2) / denominator

        # calculation of alpha
        # Numerator
        sum1 = _np.sum(weight * ymean * (data))
        sum2 = _np.sum(weight * ymean)
        sum3 = _np.sum(weight * (data))
        # Denominator
        sum4 = _np.sum(weight * (data**2))
        sum5 = sum3 ** 2
        # alpha
        alpha = (sum1 - sum2 * sum3) / (sum4 - sum5)

        # calculation of characteristic product
        pi_upper = alpha * sum3 - sum2

        # calculation of the extreme values for the return periods between 2 and 100 years
        return_periods = _np.arange(2, 100 + 1)
        v_ext_tmp = [(-_np.log(-_np.log(1 - 1 / return_period)) + pi_upper) / alpha 
                     for return_period in return_periods]
        v_ext = [v ** (1 / self.preconditioning) for v in v_ext_tmp]

        # Calculation of the residual std dev
        deviation = _np.sum(weight * ((ymean - alpha * data + pi_upper)**2))
        residual_stddev = _np.sqrt(deviation * N / (N - 2))

        self.results = {}
        
        self.results['Y'] = ymean
        self.results['weights'] = weight
        self.results['data'] = data
        self.results['Values for return period from 2 to 100 years'] = v_ext 
        self.results['slope'] = 1. / alpha
        self.results['offset'] = pi_upper / alpha
        self.results['characteristic product'] = pi_upper
        self.results['alpha'] = alpha
        self.results['residual standard deviation'] = residual_stddev
        self.c     = 0
        self.loc   = self.results['offset']
        self.scale = self.results['slope']
        self.distr = _st.gumbel_r(loc = self.loc, 
                                   scale = self.scale)
    

class Lieblein(_GumbelBase):
    __doc__ = docstringbase.format('Lieblein', '_ppp_lieblein')
    
    def __init__(self, data = None, ppp = "Lieblein", **kwargs):
        super().__init__(**kwargs)
        try:
            self.data = data
            self.N = len(self.data)
            self.ppp = ppp
            self._ppp_lieblein()
        except:
            raise Exception('You should provide some data.')    
    
    #ppp stands for probability plotting position
    def _ppp_lieblein(self):
        """
        Lieblein-BLUE (Best Linear Unbiased Estimator) to obtain extreme values
        using a Type I (Gumbel) extreme value distribution.
        
        It approaches the calculation of extremes using a very classical 
        methodology provided by Julius Lieblein. It exists just to check how 
        several consultants made the calculation of wind speed extremes in the wind 
        energy industry.
        
        It calculates extremes using an adjustment of Gumbel distribution using 
        least squares fit and considering several probability-plotting positions 
        used in the wild.
        
        **References**
        
            Lieblein J, (1974), 'Efficient methods of Extreme-Value Methodology', 
            NBSIR 74-602, National Bureau of Standards, U.S. Department of Commerce.
        """
        # coefficients for sample below or equal to 16 elements
        ai = {
            'n = 02': [0.916373, 0.083627],
            'n = 03': [0.656320, 0.255714, 0.087966],
            'n = 04': [0.510998, 0.263943, 0.153680, 0.071380],
            'n = 05': [0.418934, 0.246282, 0.167609, 0.108824, 
                       0.058350],
            'n = 06': [0.355450, 0.225488, 0.165620, 0.121054, 
                       0.083522, 0.048867],
            'n = 07': [0.309008, 0.206260, 0.158590, 0.123223, 
                       0.093747, 0.067331, 0.041841],
            'n = 08': [0.273535, 0.189428, 0.150200, 0.121174, 
                       0.097142, 0.075904, 0.056132, 0.036485],
            'n = 09': [0.245539, 0.174882, 0.141789, 0.117357, 
                       0.097218, 0.079569, 0.063400, 0.047957, 
                       0.032291],
            'n = 10': [0.222867, 0.162308, 0.133845, 0.112868, 
                       0.095636, 0.080618, 0.066988, 0.054193, 
                       0.041748, 0.028929],
            'n = 11': [0.204123, 0.151384, 0.126522, 0.108226, 
                       0.093234, 0.080222, 0.068485, 0.057578, 
                       0.047159, 0.036886, 0.026180],
            'n = 12': [0.188361, 0.141833, 0.119838, 0.103673, 
                       0.090455, 0.079018, 0.068747, 0.059266, 
                       0.050303, 0.041628, 0.032984, 0.023894],
            'n = 13': [0.174916, 0.133422, 0.113759, 0.099323, 
                       0.087540, 0.077368, 0.068264, 0.059900, 
                       0.052047, 0.044528, 0.037177, 0.029790, 
                       0.021965],
            'n = 14': [0.163309, 0.125966, 0.108230, 0.095223,
                       0.084619, 0.075484, 0.067331, 0.059866,
                       0.052891, 0.046260, 0.039847, 0.033526,
                       0.027131, 0.020317],
            'n = 15': [0.153184, 0.119314, 0.103196, 0.091384, 
                       0.081767, 0.073495, 0.066128, 0.059401,
                       0.053140, 0.047217, 0.041529, 0.035984,
                       0.030484, 0.024887, 0.018894],
            'n = 16': [0.144271, 0.113346, 0.098600, 0.087801,
                       0.079021, 0.071476, 0.064771, 0.058660,
                       0.052989, 0.047646, 0.042539, 0.037597,
                       0.032748, 0.027911, 0.022969, 0.017653]
        }

        bi = {
            'n = 02': [-0.721348, 0.721348],
            'n = 03': [-0.630541, 0.255816, 0.374725],
            'n = 04': [-0.558619, 0.085903, 0.223919, 0.248797],
            'n = 05': [-0.503127, 0.006534, 0.130455, 0.181656, 
                       0.184483],
            'n = 06': [-0.459273, -0.035992, 0.073199, 0.126724,
                       0.149534, 0.145807],
            'n = 07': [-0.423700, -0.060698, 0.036192, 0.087339,
                       0.114868, 0.125859, 0.120141],
            'n = 08': [-0.394187, -0.075767, 0.011124, 0.058928,
                       0.087162, 0.102728, 0.108074, 0.101936],
            'n = 09': [-0.369242, -0.085203, -0.006486, 0.037977,
                       0.065574, 0.082654, 0.091965, 0.094369,
                       0.088391],
            'n = 10': [-0.347830, -0.091158, -0.019210, 0.022179,
                       0.048671, 0.066064, 0.077021, 0.082771,
                       0.083552, 0.077940],
            'n = 11': [-0.329210, -0.094869, -0.028604, 0.010032,
                       0.035284, 0.052464, 0.064071, 0.071381,
                       0.074977, 0.074830, 0.069644],
            'n = 12': [-0.312840, -0.097086, -0.035655, 0.000534,
                       0.024548, 0.041278, 0.053053, 0.061112,
                       0.066122, 0.068357, 0.067671, 0.062906],
            'n = 13': [-0.298313, -0.098284, -0.041013, -0.006997, 
                       0.015836, 0.032014, 0.043710, 0.052101, 
                       0.057862, 0.061355, 0.062699, 0.061699, 
                       0.057330],
            'n = 14': [-0.285316, -0.098775, -0.045120, -0.013039, 
                       0.008690, 0.024282, 0.035768, 0.044262, 
                       0.050418, 0.054624, 0.057083, 0.057829, 
                       0.056652, 0.052642],
            'n = 15': [-0.273606, -0.098768, -0.048285, -0.017934,
                       0.002773, 0.017779, 0.028988, 0.037452,
                       0.043798, 0.048415, 0.051534, 0.053267,
                       0.053603, 0.052334, 0.048648],
            'n = 16': [-0.262990, -0.098406, -0.050731, -0.021933,
                       -0.002167, 0.012270, 0.023168, 0.031528, 
                       0.037939, 0.042787, 0.046308, 0.048646, 
                       0.049860, 0.049912, 0.048602, 0.045207]
        }
        data = _np.sort(self.data)
        data = data ** self.preconditioning
        N = self.N
        
        # hyp and coeffs are used to calculate values for samples higher than 16 elements
        # Hypergeometric distribution function
        def hyp(n,m,i,t):
            bin1 = _fact(i)/(_fact(t) * _fact(i - t))
            bin2 = _fact(n-i)/(_fact(m-t) * _fact((n-i) - (m-t)))
            bin3 = _fact(n)/(_fact(m) * _fact(n - m))
            return bin1 * bin2 / bin3

        # Coefficients
        def coeffs(n, m):
            aip = []
            bip = []
            for i in range(n):
                a = 0
                b = 0
                for t in range(m):
                    try:
                        a += ai['n = {:02}'.format(m)][t] * ((t + 1) / (i + 1)) * hyp(n, m, i + 1, t + 1)
                        b += bi['n = {:02}'.format(m)][t] * ((t + 1) / (i + 1)) * hyp(n, m, i + 1, t + 1)
                    except:
                        pass
                aip.append(a)
                bip.append(b)
            return aip, bip
        
        def distr_params():
            if N <= 16:
                mu = _np.sum(_np.array(ai['n = {:02}'.format(N)]) * data)    #parameter u in the paper
                sigma = _np.sum(_np.array(bi['n = {:02}'.format(N)]) * data) #parameter b in the paper
            else:
                aip, bip = coeffs(N, 16)
                mu = _np.sum(_np.array(aip) * data)
                sigma = _np.sum(_np.array(bip) * data)
            return mu, sigma

        mu, sigma = distr_params()
        return_period = _np.arange(2, 100 + 1)
        P = ((_np.arange(N) + 1)) / (N + 1)
        Y = -_np.log(-_np.log(P))
        vref = (- sigma * _np.log(-_np.log(1 - 1 / return_period)) + mu)**(1 / self.preconditioning)
        
        self.results = {}
        self.results['Y'] = Y
        self.results['data'] = data
        self.results['Values for return period from 2 to 100 years'] = vref 
        self.results['slope'] = sigma
        self.results['offset'] = mu
        self.c     = 0
        self.loc   = self.results['offset']
        self.scale = self.results['slope']
        self.distr = _st.gumbel_r(loc = self.loc, 
                                   scale = self.scale)
    

class PPPLiterature(_GumbelBase):
    __doc__ = docstringbase.format('several', """_ppp_adamowski
    
        _ppp_beard

        _ppp_blom

        _ppp_gringorten

        _ppp_hazen

        _ppp_hirsch

        _ppp_iec56

        _ppp_landwehr

        _ppp_laplace

        _ppp_mm

        _ppp_tukey

        _ppp_weibull""")
    
    def __init__(self, data = None, ppp = "Weibull", **kwargs):
        super().__init__(**kwargs)
        try:
            self.data = data
            self.N = len(self.data)
            self.ppp = ppp
            self._calculate_values(how = self.ppp)
        except:
            raise Exception('You should provide some data.')    
    
    #ppp stands for probability plotting position
    def _calculate_values(self, how = None):
        data = _np.sort(self.data)
        data = data ** self.preconditioning
        N = self.N
        
        if how == 'Adamowski':
            # see De, M., 2000. A new unbiased plotting position formula for gumbel distribution. 
            #     Stochastic Envir. Res. Risk Asses., 14: 1-7.
            P = ((_np.arange(N) + 1) - 0.25) / (N + 0.5)
        if how == 'Beard':
            # see De, M., 2000. A new unbiased plotting position formula for gumbel distribution. 
            #     Stochastic Envir. Res. Risk Asses., 14: 1-7.
            P = ((_np.arange(N) + 1) - 0.31) / (N + 0.38)
        if how == 'Blom':
            # see Adeboye, O.B. and M.O. Alatise, 2007. Performance of probability distributions and plotting 
            #      positions in estimating the flood of River Osun at Apoje Sub-basin, Nigeria. Agric. Eng. Int.: CIGR J., Vol. 9. 
            P = ((_np.arange(N) + 1) - 0.375) / (N + 0.25)
        if how == 'Chegodayev':
            # see De, M., 2000. A new unbiased plotting position formula for gumbel distribution. 
            #     Stochastic Envir. Res. Risk Asses., 14: 1-7.
            P = ((_np.arange(N) + 1) - 0.3) / (N + 0.4)
        if how == 'Cunnane':
            # see Cunnane, C., 1978. Unbiased plotting positions: A review. J. Hydrol., 37: 205-222.
            P = ((_np.arange(N) + 1) - 0.4) / (N + 0.2)
        if how == 'Gringorten':
            # see Adeboye, O.B. and M.O. Alatise, 2007. Performance of probability distributions and plotting 
            #     positions in estimating the flood of River Osun at Apoje Sub-basin, Nigeria. Agric. Eng. Int.: CIGR J., Vol. 9. 
            P = ((_np.arange(N) + 1) - 0.44) / (N + 0.12)
        if how == 'Hazen':
            # see Adeboye, O.B. and M.O. Alatise, 2007. Performance of probability distributions and plotting 
            #     positions in estimating the flood of River Osun at Apoje Sub-basin, Nigeria. Agric. Eng. Int.: CIGR J., Vol. 9. 
            P = ((_np.arange(N) + 1) - 0.5) / (N)
        if how == 'Hirsch':
            # see Jay, R.L., O. Kalman and M. Jenkins, 1998. Integrated planning and management for Urban water 
            #     supplies considering multi uncertainties. Technical Report, 
            #     Department of Civil and Environmental Engineering, Universities of California.
            P = ((_np.arange(N) + 1) + 0.5) / (N + 1)
        if how == 'IEC56':
            # see Forthegill, J.C., 1990. Estimating the cumulative probability of failure data points to be 
            #     plotted on weibull and other probability paper. Electr. Insulation Transact., 25: 489-492.
            P = ((_np.arange(N) + 1) - 0.5) / (N + 0.25)
        if how == 'Landwehr':
            # see Makkonen, L., 2008. Problem in the extreme value analysis. Structural Safety, 30: 405-419.
            P = ((_np.arange(N) + 1) - 0.35) / (N)
        if how == 'Laplace':
            # see Jay, R.L., O. Kalman and M. Jenkins, 1998. Integrated planning and management for Urban 
            #     water supplies considering multi uncertainties. Technical Report, 
            #     Department of Civil and Environmental Engineering, Universities of California.
            P = ((_np.arange(N) + 1) + 1) / (N + 2)
        if how == 'McClung and Mears':
            # see Makkonen, L., 2008. Problem in the extreme value analysis. Structural Safety, 30: 405-419.
            P = ((_np.arange(N) + 1) - 0.4) / (N)
        if how == 'Tukey':
            # see Makkonen, L., 2008. Problem in the extreme value analysis. Structural Safety, 30: 405-419.
            P = ((_np.arange(N) + 1) - 1/3) / (N + 1/3)
        if how == 'Weibull':
            # see Hynman, R.J. and Y. Fan, 1996. Sample quantiles in statistical packages. Am. Stat., 50: 361-365.
            P = ((_np.arange(N) + 1)) / (N + 1)

        Y = -_np.log(-_np.log(P))
        slope, offset = _np.polyfit(Y, data, 1)
        R2 = _np.corrcoef(Y, data)[0, 1]**2
        #fit = slope * Y + offset
        return_period = _np.arange(2,101)
        vref = (- slope * _np.log(-_np.log(1 - 1 / return_period)) + offset)**(1 / self.preconditioning)
        
        self.results = {}
        self.results['data'] = data
        self.results['Y'] = Y
        self.results['Values for return period from 2 to 100 years'] = vref
        self.results['R2'] = R2
        self.results['slope'] = slope
        self.results['offset'] = offset
        self.c     = 0
        self.loc   = self.results['offset']
        self.scale = self.results['slope']
        self.distr = _st.gumbel_r(loc = self.loc, 
                                   scale = self.scale)
    
    def _ppp_adamowski(self):
        """
        Perform the calculations using the Adamowski method available for the 
        probability positions.
        
        Probability positions are defined as:
        
        .. math::
        
           P = \\frac{(N + 1) - 0.25}{N + 0.5}
        
        **References**
        
            De, M., 2000. A new unbiased plotting position formula for gumbel 
            distribution. Stochastic Envir. Res. Risk Asses., 14: 1-7.
        """
        self._calculate_values(how = "Adamowski")
        
    def _ppp_beard(self):
        """
        Perform the calculations using the Beard method available for the 
        probability positions.
        
        Probability positions are defined as:

        .. math::
        
           P = \\frac{(N + 1) - 0.31}{N + 0.38}
        
        **References**
        
            De, M., 2000. A new unbiased plotting position formula for gumbel 
            distribution. Stochastic Envir. Res. Risk Asses., 14: 1-7.
        """
        self._calculate_values(how = "Beard")
        
    def _ppp_blom(self):
        """
        Perform the calculations using the Blom method available for the 
        probability positions.
        
        Probability positions are defined as:

        .. math::
        
           P = \\frac{(N + 1) - 0.375}{N + 0.25}
        
        **References**
        
            De, M., 2000. A new unbiased plotting position formula for gumbel 
            distribution. Stochastic Envir. Res. Risk Asses., 14: 1-7.
        """
        self._calculate_values(how = "Blom")
        
    def _ppp_chegodayev(self):
        """
        Perform the calculations using the Chegodayev method available for the 
        probability positions.
        
        Probability positions are defined as:

        .. math::
        
           P = \\frac{(N + 1) - 0.3}{N + 0.4}
        
        **References**
        
            De, M., 2000. A new unbiased plotting position formula for gumbel 
            distribution. Stochastic Envir. Res. Risk Asses., 14: 1-7.
        """
        self._calculate_values(how = "Chegodayev")
        
    def _ppp_cunnane(self):
        """
        Perform the calculations using the Cunnane method available for the 
        probability positions.
                
        Probability positions are defined as:

        .. math::
        
           P = \\frac{(N + 1) - 0.4}{N + 0.2}
        
        **References**
        
            Cunnane, C., 1978. Unbiased plotting positions: A review. 
            J. Hydrol., 37: 205-222.
        """
        self._calculate_values(how = "Cunnane")
        
    def _ppp_gringorten(self):
        """
        Perform the calculations using the Gringorten method available for the 
        probability positions.
        
        Probability positions are defined as:

        .. math::
        
           P = \\frac{(N + 1) - 0.44}{N + 0.12}
        
        **References**
        
            Adeboye, O.B. and M.O. Alatise, 2007. Performance of probability 
            distributions and plotting positions in estimating the flood of 
            River Osun at Apoje Sub-basin, Nigeria. Agric. Eng. Int.: 
            CIGR J., Vol. 9.
        """
        self._calculate_values(how = "Gringorten")
        
    def _ppp_hazen(self):
        """
        Perform the calculations using the Hazen method available for the 
        probability positions.
        
        Probability positions are defined as:

        .. math::
        
           P = \\frac{(N + 1) - 0.5}{N}
        
        **References**
        
            Adeboye, O.B. and M.O. Alatise, 2007. Performance of probability 
            distributions and plotting positions in estimating the flood of 
            River Osun at Apoje Sub-basin, Nigeria. Agric. Eng. Int.: 
            CIGR J., Vol. 9.
        """
        self._calculate_values(how = "Hazen")
    
    def _ppp_hirsch(self):
        """
        Perform the calculations using the Hirsch method available for the 
        probability positions.
        
        Probability positions are defined as:

        .. math::
        
           P = \\frac{(N + 1) + 0.5}{N + 1}
        
        **References**
        
            Jay, R.L., O. Kalman and M. Jenkins, 1998. Integrated planning and 
            management for Urban water supplies considering multi uncertainties. 
            Technical Report, Department of Civil and Environmental Engineering, 
            Universities of California.
        """
        self._calculate_values(how = "Hirsch")
        
    def _ppp_iec56(self):
        """
        Perform the calculations using the IEC56 method available for the 
        probability positions.
        
        Probability positions are defined as:

        .. math::
        
           P = \\frac{(N + 1) - 0.5}{N + 0.25}
        
        **References**
        
            Forthegill, J.C., 1990. Estimating the cumulative probability of 
            failure data points to be plotted on weibull and other probability 
            paper. Electr. Insulation Transact., 25: 489-492.
        """
        self._calculate_values(how = "IEC56")
        
    def _ppp_landwehr(self):
        """
        Perform the calculations using the Landwehr method available for the 
        probability positions.
        
        Probability positions are defined as:

        .. math::
        
           P = \\frac{(N + 1) - 0.35}{N}
        
        **References**
        
            Makkonen, L., 2008. Problem in the extreme value analysis. 
            Structural Safety, 30: 405-419.
        """
        self._calculate_values(how = "Landwehr")
    
    def _ppp_laplace(self):
        """
        Perform the calculations using the Laplace method available for the 
        probability positions.
        
        Probability positions are defined as:

        .. math::
        
           P = \\frac{(N + 1) + 1}{N + 2}
        
        **References**
        
            Jay, R.L., O. Kalman and M. Jenkins, 1998. Integrated planning and 
            management for Urban water supplies considering multi uncertainties. 
            Technical Report, Department of Civil and Environmental Engineering, 
            Universities of California.
        """
        self._calculate_values(how = "Laplace")
        
    def _ppp_mm(self):
        """
        Perform the calculations using the McClung and Mears method available 
        for the probability positions.
        
        Probability positions are defined as:

        .. math::
        
           P = \\frac{(N + 1) - 0.4}{N}
        
        **References**
        
            Makkonen, L., 2008. Problem in the extreme value analysis. 
            Structural Safety, 30: 405-419.
        """
        self._calculate_values(how = "McClung and Mears")
    
    def _ppp_tukey(self):
        """
        Perform the calculations using the Tukey method available for the 
        probability positions.
        
        Probability positions are defined as:

        .. math::
        
           P = \\frac{(N + 1) - 1/3}{N + 1/3}
        
        **References**
        
            Makkonen, L., 2008. Problem in the extreme value analysis. 
            Structural Safety, 30: 405-419.
        """
        self._calculate_values(how = "Tukey")
    
    def _ppp_weibull(self):
        """
        Perform the calculations using the Weibull method available for the 
        probability positions.
        
        Probability positions are defined as:

        .. math::
        
           P = \\frac{(N + 1) + 1}{N + 1}
        
        **References**
        
            Hynman, R.J. and Y. Fan, 1996. Sample quantiles in statistical 
            packages. Am. Stat., 50: 361-365.
        """
        self._calculate_values(how = "Weibull")