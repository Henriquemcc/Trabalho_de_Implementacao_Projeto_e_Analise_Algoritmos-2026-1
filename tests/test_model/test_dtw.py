import unittest
from app.model.SerieTemporal import SerieTemporal
from app.model.DynamicTimeWarping import DynamicTimeWarping
from app.model.DynamicTimeWarping import Distancia
import dtaidistance


class TestDTW(unittest.TestCase):
    """
    Realiza testes de unidades na implementação do algoritmo Dynamic time warping.
    """
    def test_duas_series_temporais_iguais(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 1")
        serie2 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 2")
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.dtw_distance(serie1, serie2)
        self.assertEqual(resultado, 0)

    def test_duas_series_temporais_diferentes(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 1")
        serie2 = SerieTemporal([12, 14, 16, 18], "Série Temporal 2")
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.dtw_distance(serie1, serie2)
        self.assertNotEqual(resultado, 0)

    def test_comparar_implementacao_dtw_com_biblioteca(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 1")
        serie2 = SerieTemporal([12, 14, 16, 18], "Série Temporal 2")
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.dtw_distance(serie1, serie2)
        resultado_biblioteca = dtaidistance.dtw.distance(serie1.dados, serie2.dados, window=10, inner_dist='euclidean')
        self.assertEqual(resultado, resultado_biblioteca)