import os
from pathlib import Path
from tkinter import filedialog
from tkinter import simpledialog

from model.DynamicTimeWarping import DynamicTimeWarping
from model.MatrizAlinhamento import MatrizAlinhamento
from model.MatrizMapeamento import MatrizMapeamento
from model.SerieTemporal import SerieTemporal
from view.JanelaDistanciaContinuousDynamicTimeWarping import JanelaDistanciaContinuousDynamicTimeWarping
from view.JanelaDistanciaDerivativeDynamicTimeWarping import JanelaDistanciaDerivativeDynamicTimeWarping
from view.JanelaDistanciaDynamicTimeWarping import JanelaDistanciaDynamicTimeWarping
from view.JanelaLongestCommonSubsequence import JanelaLongestCommonSubsequence
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

    def gerar_matriz_alinhamento_dtw(self):
        """
        Realiza a geração de uma matriz de alinhamento.
        :return:
        """

        # Verificando se há pelo menos duas séries temporais
        if len(self.series_temporais) < 2:
            return

        # Obtendo as séries temporais
        serie_temporal_1 = None
        while serie_temporal_1 is None:
            serie_temporal_1 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 1", "Selecione a primeira série temporal", self.series_temporais).mostrar()

        serie_temporal_2 = None
        while serie_temporal_2 is None:
            serie_temporal_2 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 2", "Selecione a segunda série temporal", self.series_temporais).mostrar()

        # Criando algoritmo
        dtw = DynamicTimeWarping()

        # Criando matriz de alinhamento
        matriz_alinhamento = MatrizAlinhamento(serie_temporal_1, serie_temporal_2)

        # Exibindo matriz de alinhamento
        janela_matriz_alinhamento = JanelaMatrizAlinhamento(matriz_alinhamento, dtw)

    def gerar_matriz_mapeamento_dtw(self):
        """
        Realiza a geração de uma matriz de mapeamento.
        :return:
        """

        # Verificando se há pelo menos duas séries temporais
        if len(self.series_temporais) < 2:
            return

        # Obtendo as séries temporais
        serie_temporal_1 = None
        while serie_temporal_1 is None:
            serie_temporal_1 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 1", "Selecione a primeira série temporal", self.series_temporais).mostrar()

        serie_temporal_2 = None
        while serie_temporal_2 is None:
            serie_temporal_2 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 2", "Selecione a segunda série temporal", self.series_temporais).mostrar()

        # Criando algoritmo
        dtw = DynamicTimeWarping()

        # Criando matriz de mapeamento
        matriz_mapeamento = MatrizMapeamento(serie_temporal_1, serie_temporal_2)

        # Exibindo matriz de mapeamento
        janela_matriz_mapeamento = JanelaMatrizMapeamento(matriz_mapeamento, dtw)

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

    def executar_longest_common_subsequence(self):
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

    def executar_derivative_dynamic_time_warping(self):
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
