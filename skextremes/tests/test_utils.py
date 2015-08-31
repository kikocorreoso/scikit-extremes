"""
Tests for utils module
"""

import unittest
import warnings
warnings.filterwarnings('always')

from numpy.testing import assert_array_almost_equal
import numpy as np
from scipy import stats

from skextremes.utils import bootstrap_ci

class UtilsBootstrapTest(unittest.TestCase):
    """
    This tests are an adaptation of 
    https://github.com/cgevans/scikits-bootstrap/blob/master/scikits/bootstrap/test_bootstrap.py
    in order to test the simple implementation used in skextremes.
    """
    
    def __init__(self, *args, **kwargs):
        super(UtilsBootstrapTest, self).__init__(*args, **kwargs)
        # Input data from original scikit boostrap implementation
        self.data = np.array([ 1.34016346,  1.73759123,  1.49898834, 
                              -0.22864333,  2.031034  ,  2.17032495,  
                               1.59645265, -0.76945156,  0.56605824, 
                              -0.11927018, -0.1465108 , -0.79890338, 
                               0.77183278, -0.82819136,  1.32667483,
                               1.05986776,  2.14408873, -1.43464512,  
                               2.28743654,  0.42864858])
        self.x = [1,2,3,4,5,6]
        self.y = [2,1,2,5,1,2]
        
    def test_pi_simple(self):
        # I'm not considering the multi alpha case. Just one alpha can be used.
        np.random.seed(1234567890)
        results = bootstrap_ci(self.data, np.average, 
                               alpha = 0.1, n_samples = 100)
        assert_array_almost_equal(results, [0.3148352 ,  1.10458334])  
        np.random.seed(1234567890)        
        results = bootstrap_ci(self.data, np.average, 
                               alpha = 0.2, n_samples = 100)
        assert_array_almost_equal(results, [0.35975001,  1.02974178])
        np.random.seed(1234567890)
        results = bootstrap_ci(self.data, np.average, 
                               alpha = 0.8, n_samples = 100)
        assert_array_almost_equal(results, [0.68154479,  0.84423589])
        np.random.seed(1234567890)
        results = bootstrap_ci(self.data, np.average, 
                               alpha = 0.9, n_samples = 100)
        assert_array_almost_equal(results, [0.71450871,  0.77017119])
    
    def test_pi_multi_2dout_multialpha(self):
        # I'm not considering the multi option of bootstrap so only 1d arrays
        # are valid and this test should fail as is so i modified the original
        # test to make it usable
        np.random.seed(1234567890)
        results = bootstrap_ci(np.vstack((self.x, self.y)).T, 
                               lambda a: stats.linregress(a)[0], 
                               alpha = 0.1,
                               n_samples = 2000)
        assert_array_almost_equal(results, [-0.375, 0.90243902])
        np.random.seed(1234567890)
        results = bootstrap_ci(np.vstack((self.x, self.y)).T, 
                               lambda a: stats.linregress(a)[1], 
                               alpha = 0.1,
                               n_samples = 2000)
        assert_array_almost_equal(results, [0.22727273, 3.95121951])
        

if __name__ == "__main__":
    unittest.main(verbosity = 2)