"""
Tests for datasets module
"""

import unittest

import numpy as np

from skextremes.datasets import (
    dowjones,
    engine,
    euroex,
    exchange,
    fremantle,
    glass,
    portpirie,
    rain,
    venice,
    wavesurge,
    wind,
    wooster,
    harris1996,
)

datasets = (
    dowjones,
    engine,
    euroex,
    exchange,
    fremantle,
    glass,
    portpirie,
    rain,
    venice,
    wavesurge,
    wind,
    wooster,
    harris1996,
)


def test_dataset_has_description():
    for dataset in datasets:
        assert isinstance(dataset().description.__str__(), str)

def test_dataset_asarray():
    for dataset in datasets:
        assert isinstance(dataset().asarray(), np.ndarray)

def test_dataset_has_fields():
    for dataset in datasets:
        assert hasattr(dowjones(), "fields")
