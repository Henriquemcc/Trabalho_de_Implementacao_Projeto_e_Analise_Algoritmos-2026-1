import tkinter

import numpy as np
import matplotlib.pyplot as plt
from dtaidistance import dtw
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from model.MatrizMapeamento import MatrizMapeamento


class JanelaMatrizMapeamento(tkinter.Toplevel):
    """
    Janela utilizada para exibir uma matriz de alinhamento.
    """

    def __init__(self, matriz_mapeamento: MatrizMapeamento):
        tkinter.Toplevel.__init__(self)
        self.title("Matriz de Mapeamento")
        self.matriz_mapeamento = matriz_mapeamento

        # Configurando o tamanho da janela
        screen_width = 800
        screen_height = 600
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Criando frame
        self.criar_frame()

    def criar_frame(self):
        """
        Cria o frame da matriz de mapeamento.
        :return:
        """
        self.frame = tkinter.Frame(self, bg="white")

        fig = Figure(figsize=(6, 4), dpi=100)

        # Obtendo os dados
        s1 = self.matriz_mapeamento.serie_1.dados
        s2 = self.matriz_mapeamento.serie_2.dados

        # Calculando o melhor caminho
        melhor_caminho = dtw.warping_path(s1, s2)

        # Plotando a série 1 no topo e a série 2 abaixo (com um offset vertical)
        offset = 5
        plt.plot(s1 + offset, label="Série A", color="blue", marker="o")
        plt.plot(s2, label="Série B", color="red", marker="o")

        # Desenhando as linhas de mapeamento (conexões)
        # O caminho contém tuplas (índice_s1, índice_s2)
        for (idx1, idx2) in melhor_caminho:
            # Desenha uma linha entre s1[idx1] e s2[idx2]
            # Coordenadas: [x1, x2], [y1, y2]
            plt.plot([idx1, idx2], [s1[idx1] + offset, s2[idx2]], color='gray', linestyle='--', alpha=0.4, linewidth=1)

        plt.title("Mapeamento de Alinhamento (DTW Warping)")
        plt.yticks([0, offset], [self.matriz_mapeamento.serie_2.nome, self.matriz_mapeamento.serie_1.nome])
        plt.legend()
        plt.grid(axis='x', alpha=0.2)
        plt.show()

        # Adicionando gráfico ao frame
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)

        self.frame.pack()
