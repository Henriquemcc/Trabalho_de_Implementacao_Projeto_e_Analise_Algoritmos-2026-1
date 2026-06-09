import unittest
from app.model.LongestCommonSubsequence import LongestCommonSubsequence

from model.SerieTemporal import SerieTemporal


class TestLongestCommonSubsequence(unittest.TestCase):
    def test_lcs_duas_series_temporais_iguais(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série 1")
        serie2 = SerieTemporal([1, 2, 3, 4, 5], "Série 2")
        resultado = LongestCommonSubsequence.lcs(serie1, serie2)
        self.assertEqual(resultado, 5)