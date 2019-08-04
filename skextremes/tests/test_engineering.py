"""
Tests for engineering module
"""

import pytest
import warnings

warnings.filterwarnings("always")

from numpy.testing import assert_almost_equal

from skextremes.models.engineering import Harris1996, Lieblein, PPPLiterature
from skextremes.datasets import harris1996


class TestHarris1996:
    def setup_method(self):
        # Input data from harris 1996 paper
        self.extremes = harris1996().fields.harris1996
        # Results using Harris methodology on harris 1996 paper
        self.modeHarris = 271.6
        self.alphaHarris = 0.01437
        self.charprodHarris = 3.903

    def test_results(self):
        # Results as provided by harris 1996
        har = Harris1996(self.extremes, preconditioning=2)
        assert_almost_equal(har.results["offset"], self.modeHarris, decimal=1)
        assert_almost_equal(har.results["alpha"], self.alphaHarris, decimal=4)
        assert_almost_equal(
            har.results["characteristic product"],
            self.charprodHarris,
            decimal=2,
        )

    def test_input(self):
        # Check if input is correct
        with pytest.raises(Exception):
            Harris1996()
        with pytest.raises(Exception):
            Harris1996(1)

    def test_plot_summary_dict(self):
        har = Harris1996(self.extremes)
        fig, ax1, ax2, ax3 = har.plot_summary()
        assert len(fig.get_axes()) == 3
        assert ax1.has_data()
        assert ax2.has_data()
        assert ax3.has_data()

    def test_results_dict(self):
        har = Harris1996(self.extremes)
        assert har.ppp == "Harris1996"
        assert bool(har.results.keys())


class TestLieblein:
    def setup_method(self):
        # Input data from harris 1996 paper
        self.extremes = harris1996().fields.harris1996
        # Results using Lieblein methodology on harris 1996 paper
        self.modeLieblein = 272.9

    def test_results(self):
        # Results as provided by harris 1996
        lie = Lieblein(self.extremes, preconditioning=2)
        assert_almost_equal(lie.results["offset"], self.modeLieblein, decimal=0)

    def test_input(self):
        # Check if input is correct
        with pytest.raises(Exception):
            Lieblein()
        with pytest.raises(Exception):
            Lieblein(1)

    def test_plot_summary(self):
        lie = Lieblein(self.extremes)
        fig, ax1, ax2, ax3 = lie.plot_summary()
        assert len(fig.get_axes()) == 3
        assert ax1.has_data()
        assert ax2.has_data()
        assert ax3.has_data()

    def test_results_dict(self):
        lie = Lieblein(self.extremes)
        assert lie.ppp == "Lieblein"
        assert bool(lie.results.keys())


class TestPPPLiterature:
    def setup_method(self):
        # Input data from harris 1996 paper
        self.extremes = harris1996().fields.harris1996
        self.hows = [
            "Adamowski",
            "Beard",
            "Blom",
            "Chegodayev",
            "Cunnane",
            "Gringorten",
            "Hazen",
            "Hirsch",
            "IEC56",
            "Landwehr",
            "Laplace",
            "McClung and Mears",
            "Tukey",
            "Weibull",
        ]

    def test_results(self):
        # Check results against other tested methods
        har = Harris1996(self.extremes, preconditioning=2)
        lie = Lieblein(self.extremes, preconditioning=2)
        models = [har, lie]
        attrs = ["loc", "scale"]
        for how in self.hows:
            for model in models:
                for attr in attrs:
                    pli = PPPLiterature(
                        self.extremes, preconditioning=2, ppp=how
                    )
                    value = getattr(model, attr)
                    up = value + value * 0.01
                    do = value - value * 0.01
                    if (pli.loc > do) and (pli.loc < up):
                        result = True
                    assert result

    def test_input(self):
        # Check if input is correct
        with pytest.raises(Exception):
            PPPLiterature()
        with pytest.raises(Exception):
            PPPLiterature(1)

    def test_plot_summary(self):
        for how in self.hows:
            pli = PPPLiterature(self.extremes, ppp=how)
            fig, ax1, ax2, ax3 = pli.plot_summary()
            assert len(fig.get_axes()) == 3
            assert ax1.has_data()
            assert ax2.has_data()
            assert ax3.has_data()

    def test_results_dict(self):
        for how in self.hows:
            pli = PPPLiterature(self.extremes, ppp=how)
            assert pli.ppp == how
            assert bool(pli.results.keys())
