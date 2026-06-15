import os
from pathlib import Path
from tkinter import filedialog
from tkinter import simpledialog

from model.ContinuousDynamicTimeWarping import ContinuousDynamicTimeWarping
from model.DerivativeDynamicTimeWarping import DerivativeDynamicTimeWarping
from model.DynamicTimeWarping import DynamicTimeWarping
from model.LongestCommonSubsequence import LongestCommonSubsequence
from model.MatrizAlinhamento import MatrizAlinhamento
from model.MatrizMapeamento import MatrizMapeamento
from model.SerieTemporal import SerieTemporal
from model.SoftDynamicTimeWarping import SoftDynamicTimeWarping
from model.WarpingPathAlgorithm import WarpingPathAlgorithm
from view.JanelaDistanciaContinuousDynamicTimeWarping import JanelaDistanciaContinuousDynamicTimeWarping
from view.JanelaDistanciaDerivativeDynamicTimeWarping import JanelaDistanciaDerivativeDynamicTimeWarping
from view.JanelaDistanciaDynamicTimeWarping import JanelaDistanciaDynamicTimeWarping
from view.JanelaDistanciaSoftDynamicTimeWarping import JanelaDistanciaSoftDynamicTimeWarping
from view.JanelaDistanciaLongestCommonSubsequence import JanelaLongestCommonSubsequence
from view.JanelaMatrizAlinhamento import JanelaMatrizAlinhamento
from view.JanelaMatrizMapeamento import JanelaMatrizMapeamento
from view.JanelaPrincipal import JanelaPrincipal
from view.JanelaSelecionarSerieTemporal import JanelaSelecionarSerieTemporal
from view.JanelaSerieTemporal import JanelaSerieTemporal


class Controlador:
    """
    Controlador principal do programa.
    """

    def __init__(self):
        """
        Constrói uma nova instância de Controlador.
        """

        # Tipos de arquivos de série temporal
        self.tipos_arquivos_serie_temporal = [
            ("Todos os arquivos compatíveis", [".txt", ".tsv"]),
            ("Arquivos de séries temporais", ".txt"),
            ("Arquivos de séries temporais", ".tsv")
        ]

        # Array que armazena as séries temporais
        self.series_temporais = []

        # Criando janela principal
        self.janela_principal = JanelaPrincipal(self)
        self.janela_principal.mainloop()

    def abrir_arquivo_serie_temporal(self):
        """
        Realiza a abertura de um arquivo de uma séria temporal.
        :return:
        """
        caminho = filedialog.askopenfilename(filetypes=self.tipos_arquivos_serie_temporal)
        if Path(caminho).suffix == ".txt":
            serie_temporal = SerieTemporal.abrir_arquivo_txt(caminho)
        elif Path(caminho).suffix == ".tsv":
            indice = simpledialog.askinteger(os.path.basename(caminho), "Digite o índice da série temporal")
            serie_temporal = SerieTemporal.abrir_arquivo_tsv(caminho, indice)
        self.series_temporais.append(serie_temporal)
        janela_interna_serie_temporal = JanelaSerieTemporal(serie_temporal)

    def obter_algoritmo(self, nome: str) -> WarpingPathAlgorithm | None:
        """
        Obtém um algoritmo a partir de uma string.
        :param nome: Nome do algoritmo.
        :return: Algoritmo escolhido.
        """
        algoritmo = None
        if nome == 'DTW':
            algoritmo = DynamicTimeWarping()
        elif nome == 'DDTW':
            algoritmo = DerivativeDynamicTimeWarping()
        elif nome == 'CDTW':
            algoritmo = ContinuousDynamicTimeWarping()
        elif nome == 'Soft-DTW':
            algoritmo = SoftDynamicTimeWarping()
        elif nome == 'LCS':
            algoritmo = LongestCommonSubsequence()

        return algoritmo

    def gerar_matriz_alinhamento(self, algoritmo: str):
        """
        Realiza a geração de uma matriz de alinhamento para um algoritmo especificado.
        :param algoritmo: Algoritmo especificado.
        :return:
        """
        # Verificando se há pelo menos duas séries temporais
        if len(self.series_temporais) < 2:
            return

        # Obtendo as séries temporais
        serie_temporal_1 = None
        while serie_temporal_1 is None:
            serie_temporal_1 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 1",
                                                             "Selecione a primeira série temporal",
                                                             self.series_temporais).mostrar()

        serie_temporal_2 = None
        while serie_temporal_2 is None:
            serie_temporal_2 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 2",
                                                             "Selecione a segunda série temporal",
                                                             self.series_temporais).mostrar()

        # Criando algoritmo
        algoritmo = self.obter_algoritmo(algoritmo)

        # Criando matriz de alinhamento
        matriz_alinhamento = MatrizAlinhamento(serie_temporal_1, serie_temporal_2)

        # Exibindo matriz de alinhamento
        janela = JanelaMatrizAlinhamento(matriz_alinhamento, algoritmo)

    def gerar_matriz_mapeamento(self, algoritmo: str):
        """
        Gera uma matriz de mapeamento para um algoritmo especificado.
        :param algoritmo: Algoritmo especificado.
        :return:
        """
        # Verificando se há pelo menos duas séries temporais
        if len(self.series_temporais) < 2:
            return

        # Obtendo as séries temporais
        serie_temporal_1 = None
        while serie_temporal_1 is None:
            serie_temporal_1 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 1",
                                                             "Selecione a primeira série temporal",
                                                             self.series_temporais).mostrar()

        serie_temporal_2 = None
        while serie_temporal_2 is None:
            serie_temporal_2 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 2",
                                                             "Selecione a segunda série temporal",
                                                             self.series_temporais).mostrar()

        # Criando algoritmo
        algoritmo = self.obter_algoritmo(algoritmo)

        # Criando matriz de mapeamento
        matriz_mapeamento = MatrizMapeamento(serie_temporal_1, serie_temporal_2)

        # Exibindo matriz de mapeamento
        janela = JanelaMatrizMapeamento(matriz_mapeamento, algoritmo)

    def executar_distancia_dynamic_time_warping(self):
        """
        Realiza a execução da distância Dynamic Time Warping
        :return:
        """
        # Verificando se há pelo menos duas séries temporais
        if len(self.series_temporais) < 2:
            return

        # Obtendo as séries temporais
        serie_temporal_1 = None
        while serie_temporal_1 is None:
            serie_temporal_1 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 1",
                                                             "Selecione a primeira série temporal",
                                                             self.series_temporais).mostrar()

        serie_temporal_2 = None
        while serie_temporal_2 is None:
            serie_temporal_2 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 2",
                                                             "Selecione a segunda série temporal",
                                                             self.series_temporais).mostrar()

        # Abrindo janela para execução do Dynamic Time Warping
        janela_dynamic_time_warping = JanelaDistanciaDynamicTimeWarping(serie_temporal_1, serie_temporal_2)

    def executar_distancia_continuous_dynamic_time_warping(self):
        """
        Realiza a execução da distância Continuous Dynamic Time Warping
        :return:
        """
        # Verificando se há pelo menos duas séries temporais
        if len(self.series_temporais) < 2:
            return

        # Obtendo as séries temporais
        serie_temporal_1 = None
        while serie_temporal_1 is None:
            serie_temporal_1 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 1",
                                                             "Selecione a primeira série temporal",
                                                             self.series_temporais).mostrar()

        serie_temporal_2 = None
        while serie_temporal_2 is None:
            serie_temporal_2 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 2",
                                                             "Selecione a segunda série temporal",
                                                             self.series_temporais).mostrar()

        # Abrindo janela para execução do Dynamic Time Warping
        JanelaDistanciaContinuousDynamicTimeWarping(serie_temporal_1, serie_temporal_2)

    def executar_distancia_longest_common_subsequence(self):
        """
        Realiza a execução do Longest Common Subsequence
        :return:
        """
        # Verificando se há pelo menos duas séries temporais
        if len(self.series_temporais) < 2:
            return

        # Obtendo as séries temporais
        serie_temporal_1 = None
        while serie_temporal_1 is None:
            serie_temporal_1 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 1",
                                                             "Selecione a primeira série temporal",
                                                             self.series_temporais).mostrar()

        serie_temporal_2 = None
        while serie_temporal_2 is None:
            serie_temporal_2 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 2",
                                                             "Selecione a segunda série temporal",
                                                             self.series_temporais).mostrar()

        # Abrindo janela para execução do Longest Common Subsequence
        janela_longest_common_subsequence = JanelaLongestCommonSubsequence(serie_temporal_1, serie_temporal_2)

    def executar_distancia_derivative_dynamic_time_warping(self):
        """
        Realiza a execução do algoritmo Derivative Dynamic Time Warping.
        :return:
        """
        # Verificando se há pelo menos duas séries temporais
        if len(self.series_temporais) < 2:
            return

        # Obtendo as séries temporais
        serie_temporal_1 = None
        while serie_temporal_1 is None:
            serie_temporal_1 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 1",
                                                             "Selecione a primeira série temporal",
                                                             self.series_temporais).mostrar()

        serie_temporal_2 = None
        while serie_temporal_2 is None:
            serie_temporal_2 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 2",
                                                             "Selecione a segunda série temporal",
                                                             self.series_temporais).mostrar()

        # Abrindo janela para execução do Derivative Dynamic Time Warping
        janela_derivative_dynamic_time_warping = JanelaDistanciaDerivativeDynamicTimeWarping(serie_temporal_1, serie_temporal_2)

    def executar_distancia_soft_dynamic_time_warping(self):
        # Verificando se há pelo menos duas séries temporais
        if len(self.series_temporais) < 2:
            return

        # Obtendo as séries temporais
        serie_temporal_1 = None
        while serie_temporal_1 is None:
            serie_temporal_1 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 1",
                                                             "Selecione a primeira série temporal",
                                                             self.series_temporais).mostrar()

        serie_temporal_2 = None
        while serie_temporal_2 is None:
            serie_temporal_2 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 2",
                                                             "Selecione a segunda série temporal",
                                                             self.series_temporais).mostrar()

        # Abrindo janela para execução do Derivative Dynamic Time Warping
        janela_soft_dynamic_time_warping = JanelaDistanciaSoftDynamicTimeWarping(serie_temporal_1, serie_temporal_2)
