"""
Tests for classic module
"""

import unittest

from numpy.testing import assert_almost_equal, assert_array_almost_equal

from skextremes.models.classic import GEV, Gumbel
from skextremes.datasets import portpirie, fremantle

class GEVTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(GEVTest, self).__init__(*args, **kwargs)
        self.datasets = [portpirie().fields.sea_level, 
                         fremantle().fields.sea_level]
        # The following values are obtained using ismev and extRemes R
        # packages
        self.expected_mle_params = [(-0.0501, 3.8747, 0.1980),
                                    (-0.2174, 1.4823, 0.1413)]
        self.expected_mle_nnlf = [-4.3391, -43.5667]
        self.expected_mle_se = [(0.09826, 0.02793, 0.02025),
                                (0.06377, 0.01671, 0.01149)]
        # The following values are obtained using extRemes R package
        self.expected_lmom_params = [(-0.0515, 3.8732, 0.2031),
                                     (-0.1963, 1.4807, 0.1391)]
    
    def test_mle_fit(self):
        for i in range(len(self.datasets)):
            model = GEV(self.datasets[i], 
                        fit_method = "mle", 
                        ci = 0.05, 
                        ci_method='delta')
            params = (-model.c, model.loc, model.scale)
            assert_array_almost_equal(params, self.expected_mle_params[i], 
                                      decimal = 3)
            assert_almost_equal(model._nnlf(params), self.expected_mle_nnlf[i],
                                decimal = 3)
            assert_array_almost_equal(model._se, self.expected_mle_se[i],
                                decimal = 4)
    
    def test_lmoments_fit(self):
        for i in range(len(self.datasets)):
            model = GEV(self.datasets[i], 
                        fit_method = "lmoments")
            params = (-model.c, model.loc, model.scale)
            assert_array_almost_equal(params, self.expected_lmom_params[i], 
                                      decimal = 3)
    
    def test_plot_summary(self):
        for i in range(len(self.datasets)):
            model = GEV(self.datasets[i], 
                        fit_method = "mle", 
                        ci = 0.05, 
                        ci_method='delta')
            fig, ax1, ax2, ax3, ax4 = model.plot_summary()
            self.assertEqual(len(fig.get_axes()), 4)
            self.assertTrue(ax1.has_data())
            self.assertTrue(ax2.has_data())
            self.assertTrue(ax3.has_data())
            self.assertTrue(ax4.has_data())

class GumbelTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(GumbelTest, self).__init__(*args, **kwargs)
        self.datasets = [portpirie().fields.sea_level, 
                         fremantle().fields.sea_level]
        # The following values are obtained using ismev and extRemes R
        # packages        
        self.expected_mle_params = [(0, 3.8694, 0.1949),
                                    (0, 1.4663, 0.1394)]
        self.expected_mle_nnlf = [-4.2177, -39.1909]
        self.expected_mle_se = [(0.02549, 0.01885),
                                (0.01593, 0.01084)]
        # The following values are obtained using lmom R package
        self.expected_lmom_params = [(0, 3.8685, 0.1943),
                                     (0, 1.4690, 0.1195)]        
    
    def test_mle_fit(self):
        for i in range(len(self.datasets)):
            model = Gumbel(self.datasets[i], 
                          fit_method = "mle", 
                          ci = 0.05, 
                          ci_method='delta')
            params = (-model.c, model.loc, model.scale)
            assert_array_almost_equal(params, self.expected_mle_params[i], 
                                      decimal = 4)
            assert_almost_equal(model._nnlf(params), self.expected_mle_nnlf[i],
                                decimal = 4)
            assert_array_almost_equal(model._se, self.expected_mle_se[i],
                                decimal = 4)
    
    def test_lmoments_fit(self):
        for i in range(len(self.datasets)):
            model = Gumbel(self.datasets[i], 
                           fit_method = "lmoments")
            params = (-model.c, model.loc, model.scale)
            assert_array_almost_equal(params, self.expected_lmom_params[i], 
                                      decimal = 3)
    
    def test_plot_summary(self):
        for i in range(len(self.datasets)):
            model = Gumbel(self.datasets[i], 
                           fit_method = "mle", 
                           ci = 0.05, 
                           ci_method='delta')
            fig, ax1, ax2, ax3, ax4 = model.plot_summary()
            self.assertEqual(len(fig.get_axes()), 4)
            self.assertTrue(ax1.has_data())
            self.assertTrue(ax2.has_data())
            self.assertTrue(ax3.has_data())
            self.assertTrue(ax4.has_data())
                            
if __name__ == "__main__":
    unittest.main(verbosity = 2)
