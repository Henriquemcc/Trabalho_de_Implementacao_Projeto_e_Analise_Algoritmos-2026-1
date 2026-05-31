import unittest

import dtaidistance
import numpy

from app.model.DynamicTimeWarping import Distancia
from app.model.DynamicTimeWarping import DynamicTimeWarping
from app.model.SerieTemporal import SerieTemporal


class TestDTW(unittest.TestCase):
    """
    Realiza testes de unidades na implementação do algoritmo Dynamic time warping.
    """
    def test_dtw_distance_duas_series_temporais_iguais(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 1")
        serie2 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 2")
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.dtw_distance(serie1, serie2)
        self.assertEqual(resultado, 0)

    def test_dtw_distance_duas_series_temporais_diferentes(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 1")
        serie2 = SerieTemporal([12, 14, 16, 18], "Série Temporal 2")
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.dtw_distance(serie1, serie2)
        self.assertNotEqual(resultado, 0)

    def test_dtw_distance_implementacao_com_biblioteca(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 1")
        serie2 = SerieTemporal([12, 14, 16, 18], "Série Temporal 2")
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.dtw_distance(serie1, serie2)
        resultado_biblioteca = dtaidistance.dtw.distance(serie1.dados, serie2.dados, window=10, inner_dist='euclidean')
        self.assertEqual(resultado, resultado_biblioteca)

    def test_dtw_distance_implementacao_com_biblioteca_dataset_umd(self):
        test = SerieTemporal.abrir_arquivo_tsv('Dataset/UCRArchive_2018/UMD/UMD_TEST.tsv', 0)
        train = SerieTemporal.abrir_arquivo_tsv('Dataset/UCRArchive_2018/UMD/UMD_TRAIN.tsv', 0)
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.dtw_distance(test, train)
        resultado_biblioteca = dtaidistance.dtw.distance(test.dados, train.dados, window=10, inner_dist='euclidean')
        self.assertEqual(resultado, resultado_biblioteca)

    def test_dtw_distance_implementacao_com_biblioteca_dataset_smooth_subspace(self):
        test = SerieTemporal.abrir_arquivo_tsv('Dataset/UCRArchive_2018/SmoothSubspace/SmoothSubspace_TEST.tsv', 0)
        train = SerieTemporal.abrir_arquivo_tsv('Dataset/UCRArchive_2018/SmoothSubspace/SmoothSubspace_TRAIN.tsv', 0)
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.dtw_distance(test, train)
        resultado_biblioteca = dtaidistance.dtw.distance(test.dados, train.dados, window=10, inner_dist='euclidean')
        self.assertEqual(resultado, resultado_biblioteca)

    def test_dtw_distance_implementacao_com_biblioteca_dataset_shake_gesture_wiimote_z(self):
        test = SerieTemporal.abrir_arquivo_tsv('Dataset/UCRArchive_2018/ShakeGestureWiimoteZ/ShakeGestureWiimoteZ_TEST.tsv', 0)
        train = SerieTemporal.abrir_arquivo_tsv('Dataset/UCRArchive_2018/ShakeGestureWiimoteZ/ShakeGestureWiimoteZ_TRAIN.tsv', 0)
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.dtw_distance(test, train)
        resultado_biblioteca = dtaidistance.dtw.distance(test.dados, train.dados, window=10, inner_dist='euclidean')
        if numpy.isnan(resultado) and numpy.isnan(resultado_biblioteca):
            pass
        else:
            self.assertEqual(resultado, resultado_biblioteca)

    def test_warping_path_implementacao_com_biblioteca_duas_series_temporais_iguais(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 1")
        serie2 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 2")
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.dtw_warping_path(serie1, serie2)
        resultado_biblioteca = dtaidistance.dtw.warping_path(serie1.dados, serie2.dados, window=10)
        self.assertEqual(resultado, resultado_biblioteca)

