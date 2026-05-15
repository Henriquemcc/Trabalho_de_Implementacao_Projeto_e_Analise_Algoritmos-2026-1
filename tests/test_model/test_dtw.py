import unittest
from app.model.SerieTemporal import SerieTemporal
from app.model.DynamicTimeWarping import DynamicTimeWarping
from app.model.DynamicTimeWarping import Distancia


class TestDTW(unittest.TestCase):
    """
    Realiza testes de unidades na implementação do algoritmo Dynamic time warping.
    """
    def test_duas_series_temporais_iguais(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 1")
        serie2 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 2")
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.processar(serie1, serie2)
        self.assertEqual(resultado, 0)