"""
Tests for classic module
"""

import pytest
from numpy.testing import assert_almost_equal, assert_array_almost_equal
from skextremes.models.classic import GEV, Gumbel
from skextremes.datasets import portpirie, fremantle

# Datasets to be used
datasets = [portpirie().fields.sea_level, fremantle().fields.sea_level]

# Expected results for GEV
# The following values are obtained using ismev and extRemes R packages
expected_mle_params = [(-0.0501, 3.8747, 0.1980), (-0.2174, 1.4823, 0.1413)]
expected_mle_nnlf = [-4.3391, -43.5667]
expected_mle_se = [(0.09826, 0.02793, 0.02025), (0.06377, 0.01671, 0.01149)]
# The following values are obtained using extRemes R package
expected_lmom_params = [(-0.0515, 3.8732, 0.2031), (-0.1963, 1.4807, 0.1391)]


class TestGEV:
    @pytest.mark.parametrize(
        "data, params, nnlf, se",
        [
            (d, p, n, s)
            for d, p, n, s in zip(
                datasets,
                expected_mle_params,
                expected_mle_nnlf,
                expected_mle_se,
            )
        ],
    )
    def test_mle_fit(self, data, params, nnlf, se):
        model = GEV(data, fit_method="mle", ci=0.05, ci_method="delta")
        _params = (-model.c, model.loc, model.scale)
        assert_array_almost_equal(_params, params, decimal=3)
        assert_almost_equal(model._nnlf(params), nnlf, decimal=3)
        assert_array_almost_equal(model._se, se, decimal=4)

    @pytest.mark.parametrize(
        "data, params", [(d, p) for d, p in zip(datasets, expected_lmom_params)]
    )
    def test_lmoments_fit(self, data, params):
        model = GEV(data, fit_method="lmoments")
        _params = (-model.c, model.loc, model.scale)
        assert_array_almost_equal(_params, params, decimal=3)

    @pytest.mark.parametrize("data", datasets)
    def test_plot_summary(self, data):
        model = GEV(data, fit_method="mle", ci=0.05, ci_method="delta")
        fig, ax1, ax2, ax3, ax4 = model.plot_summary()
        assert len(fig.get_axes()) == 4
        assert ax1.has_data()
        assert ax2.has_data()
        assert ax3.has_data()
        assert ax4.has_data()


# Expected results for Gumbel
# The following values are obtained using ismev and extRemes R packages
expected_mle_params = [(0, 3.8694, 0.1949), (0, 1.4663, 0.1394)]
expected_mle_nnlf = [-4.2177, -39.1909]
expected_mle_se = [(0.02549, 0.01885), (0.01593, 0.01084)]
# The following values are obtained using extRemes R package
expected_lmom_params = [(0, 3.8685, 0.1943), (0, 1.4690, 0.1195)]


class TestGumbel:
    @pytest.mark.parametrize(
        "data, params, nnlf, se",
        [
            (d, p, n, s)
            for d, p, n, s in zip(
                datasets,
                expected_mle_params,
                expected_mle_nnlf,
                expected_mle_se,
            )
        ],
    )
    def test_mle_fit(self, data, params, nnlf, se):
        model = Gumbel(data, fit_method="mle", ci=0.05, ci_method="delta")
        _params = (-model.c, model.loc, model.scale)
        assert_array_almost_equal(_params, params, decimal=4)
        assert_almost_equal(model._nnlf(params), nnlf, decimal=4)
        assert_array_almost_equal(model._se, se, decimal=4)

    @pytest.mark.parametrize(
        "data, params", [(d, p) for d, p in zip(datasets, expected_lmom_params)]
    )
    def test_lmoments_fit(self, data, params):
        model = Gumbel(data, fit_method="lmoments")
        _params = (-model.c, model.loc, model.scale)
        assert_array_almost_equal(_params, params, decimal=3)

    @pytest.mark.parametrize("data", datasets)
    def test_plot_summary(self, data):
        model = Gumbel(data, fit_method="mle", ci=0.05, ci_method="delta")
        fig, ax1, ax2, ax3, ax4 = model.plot_summary()
        assert len(fig.get_axes()) == 4
        assert ax1.has_data()
        assert ax2.has_data()
        assert ax3.has_data()
        assert ax4.has_data()
