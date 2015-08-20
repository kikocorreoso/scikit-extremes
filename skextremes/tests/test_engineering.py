"""
Tests for engineering module
"""

import unittest
import warnings
warnings.filterwarnings('always')

from numpy.testing import assert_almost_equal

from skextremes.models.engineering import Harris1996, Lieblein, PPPLiterature
from skextremes.datasets import harris1996

class Harris1996Test(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(Harris1996Test, self).__init__(*args, **kwargs)
        # Input data from harris 1996 paper
        self.extremes = harris1996().fields.harris1996
        # Results using Harris methodology on harris 1996 paper
        self.modeHarris = 271.6
        self.alphaHarris = 0.01437
        self.charprodHarris = 3.903
    
    def test_results(self):
        # Results as provided by harris 1996
        har = Harris1996(self.extremes, preconditioning = 2)
        assert_almost_equal(har.results['offset'], 
                            self.modeHarris, 
                            decimal = 1)
        assert_almost_equal(har.results['alpha'], 
                            self.alphaHarris, 
                            decimal = 4)    
        assert_almost_equal(har.results['characteristic product'], 
                            self.charprodHarris, 
                            decimal = 2)
        
    def test_input(self):
        # Check if input is correct
        self.assertRaises(Exception, Harris1996)
        self.assertRaises(Exception, Harris1996, 1)
    
    def test_plot_results_dict(self):
        har = Harris1996(self.extremes)
        fig, ax1, ax2, ax3 = har.plot_results()
        self.assertEqual(len(fig.get_axes()), 3)
        self.assertTrue(ax1.has_data())
        self.assertTrue(ax2.has_data())
        self.assertTrue(ax3.has_data())
    
    def test_results_dict(self):
        har = Harris1996(self.extremes)
        self.assertEqual(har.ppp, 'Harris1996')
        self.assertTrue(bool(har.results.keys()))

class LiebleinTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(LiebleinTest, self).__init__(*args, **kwargs)
        # Input data from harris 1996 paper
        self.extremes = harris1996().fields.harris1996
        # Results using Lieblein methodology on harris 1996 paper
        self.modeLieblein = 272.9    
    
    def test_results(self):
        # Results as provided by harris 1996
        lie = Lieblein(self.extremes, preconditioning = 2)
        assert_almost_equal(lie.results['offset'], 
                            self.modeLieblein, 
                            decimal = 0)
        
    def test_input(self):
        # Check if input is correct
        self.assertRaises(Exception, Lieblein)
        self.assertRaises(Exception, Lieblein, 1)
    
    def test_plot_results(self):
        lie = Lieblein(self.extremes)
        fig, ax1, ax2, ax3 = lie.plot_results()
        self.assertEqual(len(fig.get_axes()), 3)
        self.assertTrue(ax1.has_data())
        self.assertTrue(ax2.has_data())
        self.assertTrue(ax3.has_data())
    
    def test_results_dict(self):
        lie = Lieblein(self.extremes)
        self.assertEqual(lie.ppp, 'Lieblein')
        self.assertTrue(bool(lie.results.keys()))
        
class PPPLiteratureTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(PPPLiteratureTest, self).__init__(*args, **kwargs)
        # Input data from harris 1996 paper
        self.extremes = harris1996().fields.harris1996
        self.hows = ['Adamowski', 'Beard', 'Blom', 'Chegodayev', 'Cunnane',
                     'Gringorten', 'Hazen', 'Hirsch', 'IEC56', 'Landwehr', 
                     'Laplace', 'McClung and Mears', 'Tukey', 'Weibull']
    
    def test_results(self):
        # Check results against other tested methods
        har = Harris1996(self.extremes, preconditioning = 2)
        lie = Lieblein(self.extremes, preconditioning = 2)
        models = [har, lie]
        attrs = ['loc', 'scale']
        for how in self.hows:
            for model in models:
                for attr in attrs:
                    pli = PPPLiterature(self.extremes, 
                                        preconditioning = 2,
                                        ppp = how)
                    value = getattr(model, attr)
                    up = value + value * 0.01
                    do = value - value * 0.01
                    if (pli.loc > do) and (pli.loc < up):
                        result = True
                    self.assertTrue(result)
        
    def test_input(self):
        # Check if input is correct
        self.assertRaises(Exception, PPPLiterature)
        self.assertRaises(Exception, PPPLiterature, 1)
    
    def test_plot_results(self):
        for how in self.hows:
            pli = PPPLiterature(self.extremes, ppp = how)
            fig, ax1, ax2, ax3 = pli.plot_results()
            self.assertEqual(len(fig.get_axes()), 3)
            self.assertTrue(ax1.has_data())
            self.assertTrue(ax2.has_data())
            self.assertTrue(ax3.has_data())
    
    def test_results_dict(self):
        for how in self.hows:
            pli = PPPLiterature(self.extremes, ppp = how)
            self.assertEqual(pli.ppp, how)
            self.assertTrue(bool(pli.results.keys()))

if __name__ == "__main__":
    unittest.main(verbosity = 2)
