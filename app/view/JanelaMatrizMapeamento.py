import tkinter

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from model.DynamicTimeWarping import DynamicTimeWarping
from model.Distancia import Distancia
from model.MatrizMapeamento import MatrizMapeamento
from model.WarpingPathAlgorithm import WarpingPathAlgorithm


class JanelaMatrizMapeamento(tkinter.Toplevel):
    """
    Janela utilizada para exibir uma matriz de alinhamento.
    """

    def __init__(self, matriz_mapeamento: MatrizMapeamento, algoritmo: WarpingPathAlgorithm):
        tkinter.Toplevel.__init__(self)
        self.title("Matriz de Mapeamento {}".format(algoritmo.nome_algoritmo))
        self.matriz_mapeamento = matriz_mapeamento
        self.algoritmo = algoritmo

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
        self.frame.pack(fill=tkinter.BOTH, expand=True)

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111) # Cria eixo explicitamente

        # Obtendo os dados
        s1 = self.matriz_mapeamento.serie_1.dados
        s2 = self.matriz_mapeamento.serie_2.dados

        # Calculando o melhor caminho
        melhor_caminho = self.algoritmo.warping_path(s1, s2)

        # Plotando a série 1 no topo e a série 2 abaixo (com um offset vertical)
        offset = np.max(s2) + (np.max(s1) - np.min(s1))
        ax.plot(s1 + offset, label=self.matriz_mapeamento.serie_1.nome, color="blue", marker="o")
        ax.plot(s2, label=self.matriz_mapeamento.serie_2.nome, color="red", marker="o")

        # Desenhando as linhas de mapeamento (conexões)
        # O caminho contém tuplas (índice_s1, índice_s2)
        for (idx1, idx2) in melhor_caminho:
            # Desenha uma linha entre s1[idx1] e s2[idx2]
            # Coordenadas: [x1, x2], [y1, y2]
            ax.plot([idx1, idx2], [s1[idx1] + offset, s2[idx2]],
                    color='gray', linestyle='--', alpha=0.4, linewidth=1)

        ax.set_title("Mapeamento de Alinhamento (${})".format(self.algoritmo.nome_algoritmo))
        ax.set_yticks([np.mean(s2), np.mean(s1) + offset])
        ax.set_yticklabels([self.matriz_mapeamento.serie_2.nome, self.matriz_mapeamento.serie_1.nome])
        ax.legend()

        # Adicionando gráfico ao frame
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tkinter.BOTH, expand=True)

        self.frame.pack()
