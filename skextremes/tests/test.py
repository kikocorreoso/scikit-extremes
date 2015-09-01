import unittest
import warnings

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover('.')
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        unittest.TextTestRunner(verbosity = 2).run(testsuite)

