import tkinter

import matplotlib.pyplot as plt
import numpy as np
from dtaidistance import dtw
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from model.DynamicTimeWarping import DynamicTimeWarping, Distancia

from model.MatrizAlinhamento import MatrizAlinhamento


class JanelaMatrizAlinhamento(tkinter.Toplevel):
    """
    Janela utilizada para exibir uma matriz de alinhamento.
    """

    def __init__(self, matriz_alinhamento: MatrizAlinhamento):
        tkinter.Toplevel.__init__(self)
        self.title("Matriz de Alinhamento")
        self.matriz_alinhamento = matriz_alinhamento

        # Configurando o tamanho da janela
        screen_width = 800
        screen_height = 600
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Criando frame
        self.criar_frame()

    def criar_frame(self):
        """
        Cria o frame da matriz de alinhamento.
        :return:
        """
        self.frame = tkinter.Frame(self, bg="white")

        fig = Figure(figsize=(6, 4), dpi=100)

        # Obtendo os dados
        s1 = self.matriz_alinhamento.serie_1.dados
        s2 = self.matriz_alinhamento.serie_2.dados

        # Criando uma nova instância de Dynamic Time Warping
        dynamic_time_warping = DynamicTimeWarping(None, Distancia.EUCLIDIANA)

        # Plotando matriz de alinhamento
        distancia, matriz_custo = dynamic_time_warping.dtw_warping_paths(s1, s2)
        melhor_caminho = dynamic_time_warping.obter_melhor_caminho(matriz_custo)
        gs = fig.add_gridspec(2, 2, width_ratios=[1, 4], height_ratios=[1, 4],
                              wspace=0.05, hspace=0.05)

        # Subplot 1: Série Superior (Eixo X)
        ax_x = fig.add_subplot(gs[0, 1])
        ax_x.plot(s1, color='g')
        ax_x.set_axis_off()

        # Subplot 2: Série Lateral (Eixo Y)
        ax_y = fig.add_subplot(gs[1, 0])
        ax_y.plot(s2, np.arange(len(s2)), color='r')
        ax_y.invert_xaxis()  # Inverter para ficar de frente para a matriz
        ax_y.set_axis_off()

        # Subplot 3: A Matriz de Alinhamento
        ax_matriz = fig.add_subplot(gs[1, 1])
        ax_matriz.imshow(matriz_custo, interpolation='nearest', cmap='viridis', origin='lower')

        # Plotar o caminho de alinhamento (a linha branca/preta na diagonal)
        path_x, path_y = zip(*melhor_caminho)
        ax_matriz.plot(path_y, path_x, color='white', linewidth=2)

        ax_matriz.set_xlabel("Série B")
        ax_matriz.set_ylabel("Série A")

        # Adicionando gráfico ao frame
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)

        self.frame.pack()
