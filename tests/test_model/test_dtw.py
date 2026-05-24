import unittest
from os import mkdir
from pathlib import Path
from app.model.SerieTemporal import SerieTemporal
from app.model.DynamicTimeWarping import DynamicTimeWarping
from app.model.DynamicTimeWarping import Distancia
import dtaidistance
import os
import urllib.request
import pandas as pd



class TestDTW(unittest.TestCase):
    """
    Realiza testes de unidades na implementação do algoritmo Dynamic time warping.
    """
    def download_extract_time_series_data_2018(self):
        """
        Realiza download da base de dados de série temporal
        :return:
        """
        url = "https://www.cs.ucr.edu/%7Eeamonn/time_series_data_2018/UCRArchive_2018.zip"
        download_path = "Dataset/UCRArchive_2018.zip"
        extraction_dir = "Dataset"
        senha = "someone"
        if not os.path.isdir(extraction_dir):
            Path(extraction_dir).mkdir(parents=True)

            # Baixando dataset
            if not os.path.exists(download_path):
                urllib.request.urlretrieve(url, download_path)

            # Extraíndo dataset
            import zipfile
            with zipfile.ZipFile(download_path, 'r') as arquivo_zip:
                arquivo_zip.extractall(path=extraction_dir, pwd=senha.encode('utf-8'))

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

    def test_dtw_distance_comparar_implementacao_com_biblioteca(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 1")
        serie2 = SerieTemporal([12, 14, 16, 18], "Série Temporal 2")
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.dtw_distance(serie1, serie2)
        resultado_biblioteca = dtaidistance.dtw.distance(serie1.dados, serie2.dados, window=10, inner_dist='euclidean')
        self.assertEqual(resultado, resultado_biblioteca)

    def test_dtw_warping_path_duas_series_temporais_iguais_comparar_implementacao_com_biblioteca(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 1")
        serie2 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 2")
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.dtw_warping_path(serie1, serie2)
        resultado_biblioteca = dtaidistance.dtw.warping_path(serie1.dados, serie2.dados, window=10, inner_dist='euclidean')
        self.assertEqual(resultado, resultado_biblioteca)

    def test_dtw_warping_path_duas_series_temporais_diferentes_comparar_implementacao_com_biblioteca(self):
        serie1 = SerieTemporal([1, 2, 3, 4, 5], "Série Temporal 1")
        serie2 = SerieTemporal([12, 14, 16, 18], "Série Temporal 2")
        dtw = DynamicTimeWarping(10, Distancia.EUCLIDIANA)
        resultado = dtw.dtw_warping_path(serie1, serie2)
        resultado_biblioteca = dtaidistance.dtw.warping_path(serie1.dados, serie2.dados, window=10, inner_dist='euclidean')
        self.assertEqual(resultado, resultado_biblioteca)

    def test_dtw_warping_path_base_dados_umd_comparar_implementacao_com_biblioteca(self):
        self.download_extract_time_series_data_2018()
        test_df = pd.read_csv('Dataset/UCRArchive_2018/UMD/UMD_TEST.tsv', sep='\t')
        train_df = pd.read_csv('Dataset/UCRArchive_2018/UMD/UMD_TRAIN.tsv', sep='\t')
        dados_teste = test_df.iloc[0, 1:].values
        dados_treino = train_df.iloc[0, 1:].values

        # Testando implementação manual
        dynamic_time_warping = DynamicTimeWarping(janela_de_busca=None, distancia=Distancia.EUCLIDIANA)
        distancia_impl, matriz_custo_impl = dynamic_time_warping.dtw_warping_paths(dados_teste, dados_treino)

        # Testando biblioteca
        distancia_bib, matriz_custo_bib = dtaidistance.dtw.warping_paths(dados_teste, dados_treino)

        self.assertEqual(distancia_impl, distancia_bib)
        self.assertEqual(matriz_custo_impl.tolist(), matriz_custo_bib.tolist())