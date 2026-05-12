from pathlib import Path
from tkinter import filedialog

from model.MatrizAlinhamento import MatrizAlinhamento
from model.SerieTemporal import SerieTemporal
from view.FramePrincipal import FramePrincipal
from view.JanelaMatrizAlinhamento import JanelaMatrizAlinhamento
from view.JanelaPrincipal import JanelaPrincipal
from view.JanelaSerieTemporal import JanelaSerieTemporal
from view.JanelaSelecionarSerieTemporal import JanelaSelecionarSerieTemporal


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
        self.frame_principal = FramePrincipal(self.janela_principal, self)
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
            serie_temporal = SerieTemporal.abrir_arquivo_tsv(caminho)
        self.series_temporais.append(serie_temporal)
        janela_interna_serie_temporal = JanelaSerieTemporal(serie_temporal)

    def gerar_matriz_alinhamento(self):
        """
        Realiza a geração de uma matriz de alinhamento.
        :return:
        """

        # Obtendo as séries temporais
        serie_temporal_1 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 1", "Selecione a primeira série temporal", self.series_temporais).mostrar()
        serie_temporal_2 = JanelaSelecionarSerieTemporal("Selecionar Série Temporal 2", "Selecione a segunda série temporal", self.series_temporais).mostrar()

        # Criando matriz de alinhamento
        matriz_alinhamento = MatrizAlinhamento(serie_temporal_1, serie_temporal_2)

        # Exibindo matriz de alinhamento
        janela_matriz_alinhamento = JanelaMatrizAlinhamento(matriz_alinhamento)
