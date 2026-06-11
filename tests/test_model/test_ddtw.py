import unittest

from model.DerivativeDynamicTimeWarping import DerivativeDynamicTimeWarping
from model.SerieTemporal import SerieTemporal


class TestDDTW(unittest.TestCase):
    """
    Realiza testes de unidades na implementação do algoritmo Derivative Dynamic Time Warping.
    """
    def test_ddtw_distancia_duas_series_temporais_iguais(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 1")
        serie2 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 2")
        ddtw = DerivativeDynamicTimeWarping()
        resultado, _ = ddtw.warping_paths(serie1, serie2)
        self.assertEqual(resultado, 0)