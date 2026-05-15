import tkinter

from model.DynamicTimeWarping import Distancia, DynamicTimeWarping
from model.SerieTemporal import SerieTemporal


class JanelaDynamicTimeWarping(tkinter.Toplevel):
    """
    Janela utilizada para realizar execução do algoritmo Dynamic Time Warping
    """
    def __init__(self, serie_temporal1: SerieTemporal, serie_temporal2: SerieTemporal):
        """
        Constrói uma nova instância da JanelaDynamicTimeWarping.
        :param serie_temporal1: Primeira série temporal.
        :param serie_temporal2: Segunda série temporal.
        """
        tkinter.Toplevel.__init__(self)
        self.title("Dynamic Time Warping")
        self.serie_temporal1 = serie_temporal1
        self.serie_temporal2 = serie_temporal2

        # Configurando o tamanho da janela
        screen_width = 800
        screen_height = 600
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Criando frame
        self.resposta_label = None
        self.criar_frame()

    def criar_frame(self):
        """
        Cria o frame do Dynamic Time Warping
        :return:
        """
        self.frame = tkinter.Frame(self, bg="white")

        # Título do Frame
        tkinter.Label(self.frame, text="Algoritmo Dynamic Time Warping", font=("Calibre", 20))

        # Criando radiobuttons para escolher a distância utilizada
        self.variavel_distancia = tkinter.StringVar()
        tkinter.Radiobutton(self.frame, text="Distância Euclidiana", variable=self.variavel_distancia, value=Distancia.EUCLIDIANA).pack()
        tkinter.Radiobutton(self.frame, text="Distância de Manhattan", variable=self.variavel_distancia, value=Distancia.MANHATTAN).pack()

        # Criando entrada de texto para escolher a janela de busca
        tkinter.Label(self.frame, text="Janela de Busca:", font=("Calibre", 12)).pack()
        self.variavel_janela_de_busca = tkinter.StringVar()
        tkinter.Entry(self.frame, textvariable=self.variavel_janela_de_busca).pack()

        # Criando botão para executar o Dynamic Time Warping
        tkinter.Button(self.frame, text="Executar", command=lambda: self.executar).pack()

        # Criando label para mostrar a resposta do Dynamic Time Warping
        self.resposta_label = tkinter.Label(self.frame, text="Resposta:", font=("Calibre", 12))
        self.resposta_label.pack()

        self.frame.pack(fill=tkinter.BOTH, expand=True)

    def executar(self):
        """
        Realiza a execução do Dynamic Time Warping.
        :return:
        """
        janela_de_busca = int(self.variavel_janela_de_busca.get())
        distancia = Distancia(self.variavel_distancia.get())
        dtw = DynamicTimeWarping(janela_de_busca, distancia)
        resultado = dtw.processar(self.serie_temporal1, self.serie_temporal2)
        self.resposta_label.config(text=f"Resposta: {resultado}")