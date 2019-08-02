"""
Tests for wind module
"""

import pytest

from numpy.testing import assert_almost_equal

from skextremes.models.wind import (
    wind_EWTSII_Exact,
    wind_EWTSII_Gumbel,
    wind_EWTSII_Davenport,
    wind_vref_5vave,
)

# Results as provided by windographer
vave = [8.588, 9.924, 10.767, 9.974]
weibk = [2.156, 2.051, 2.206, 2.467]
expected_Exact = [32.918, 40.493, 40.135, 32.724]
expected_Gumbel = [33.364, 41.040, 40.677, 33.158]
expected_Davenport = [36.288, 44.580, 44.263, 36.129]


class TestWind:
    @pytest.mark.parametrize(
        "v, k, e", [(v, k, e) for v, k, e in zip(vave, weibk, expected_Exact)]
    )
    def test_wind_EWTSII_Exact(self, v, k, e):
        assert_almost_equal(wind_EWTSII_Exact(v, k), e, decimal=1)

    @pytest.mark.parametrize(
        "v, k, e", [(v, k, e) for v, k, e in zip(vave, weibk, expected_Gumbel)]
    )
    def test_wind_EWTSII_Gumbel(self, v, k, e):
        assert_almost_equal(wind_EWTSII_Gumbel(v, k), e, decimal=1)

    @pytest.mark.parametrize(
        "v, k, e",
        [(v, k, e) for v, k, e in zip(vave, weibk, expected_Davenport)],
    )
    def test_wind_EWTSII_Davenport(self, v, k, e):
        assert_almost_equal(wind_EWTSII_Davenport(v, k), e, decimal=1)

    def test_wind_vref_5vave(self):
        # Results as provided by windographer
        vave = [5, 6, 7, 8]
        expected = [25, 30, 35, 40]
        expected2 = [22.5, 27, 31.5, 36]
        for v, e, e2 in zip(vave, expected, expected2):
            assert_almost_equal(wind_vref_5vave(v), e, decimal=5)
            assert_almost_equal(wind_vref_5vave(v, 4.5), e2, decimal=5)
