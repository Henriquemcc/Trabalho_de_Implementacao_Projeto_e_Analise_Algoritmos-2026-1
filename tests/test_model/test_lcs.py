import unittest

from model.LongestCommonSubsequence import LongestCommonSubsequence
from model.SerieTemporal import SerieTemporal


class TestLongestCommonSubsequence(unittest.TestCase):
    def test_lcs_pd_duas_series_temporais_iguais(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série 1")
        serie2 = SerieTemporal([1, 2, 3, 4, 5], "Série 2")
        lcs = LongestCommonSubsequence()
        resultado, _ = lcs.warping_paths(serie1, serie2)
        self.assertEqual(resultado, 5)

    def test_lcs_pd_duas_series_temporais_completamente_diferentes(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série 1")
        serie2 = SerieTemporal([6, 7, 8, 9, 10], "Série 2")
        lcs = LongestCommonSubsequence()
        resultado, _ = lcs.warping_paths(serie1, serie2)
        self.assertEqual(resultado, 0)