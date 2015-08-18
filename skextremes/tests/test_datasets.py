"""
Tests for datasets module
"""

import unittest

import numpy as np

from skextremes.datasets import (dowjones, engine, euroex, exchange,
                                        fremantle, glass, portpirie, rain,
                                        venice, wavesurge, wind, wooster,
                                        harris1996)

datasets = (dowjones, engine, euroex, exchange, fremantle, glass, portpirie, 
            rain, venice, wavesurge, wind, wooster, harris1996)

class DatasetsTest(unittest.TestCase):
    
    def test_dataset_has_description(self):
        for dataset in datasets:
            self.assertIsInstance(dataset().description.__str__(), str)
            
    def test_dataset_asarray(self):
        for dataset in datasets:
            self.assertIsInstance(dataset().asarray(), np.ndarray)
    
    def test_dataset_has_fields(self):
        for dataset in datasets:
            self.assertTrue(hasattr(dowjones(), 'fields'))


if __name__ == "__main__":
    unittest.main()
