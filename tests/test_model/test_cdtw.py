import unittest
from app.model.ContinuousDynamicTimeWarping import ContinuousDynamicTimeWarping

from model.SerieTemporal import SerieTemporal


class TestCdtw(unittest.TestCase):
    def test_ddtw_distance_duas_series_temporais_iguais(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 1")
        serie2 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 2")
        resultado = ContinuousDynamicTimeWarping.cdtw_distance(serie1, serie2)
        self.assertEqual(resultado, 0)

    def test_dtw_distance_duas_series_temporais_diferentes(self):
        serie1 = SerieTemporal([1, 2, 3, 4], "Série Temporal 1")
        serie2 = SerieTemporal([12, 14, 16, 18], "Série Temporal 2")
        resultado = ContinuousDynamicTimeWarping.cdtw_distance(serie1, serie2, interpolacao=0)
        self.assertNotEqual(resultado, 0)