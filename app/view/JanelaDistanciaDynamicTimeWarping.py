import tkinter

from model.DynamicTimeWarping import Distancia, DynamicTimeWarping
from model.SerieTemporal import SerieTemporal


class JanelaDistanciaDynamicTimeWarping(tkinter.Toplevel):
    """
    Janela utilizada para realizar execução da distância do Dynamic Time Warping
    """
    def __init__(self, serie_temporal1: SerieTemporal, serie_temporal2: SerieTemporal):
        """
        Constrói uma nova instância da JanelaDynamicTimeWarping.
        :param serie_temporal1: Primeira série temporal.
        :param serie_temporal2: Segunda série temporal.
        """
        tkinter.Toplevel.__init__(self)
        self.variavel_janela_de_busca = None
        self.title("Dynamic Time Warping")
        self.serie_temporal1 = serie_temporal1
        self.serie_temporal2 = serie_temporal2
        self.mapa_distancias = {d.value: d for d in Distancia}
        self.variavel_distancia = tkinter.StringVar(value=Distancia.EUCLIDIANA.value)

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
        self.frame = tkinter.Frame(self)

        # Título do Frame
        tkinter.Label(self.frame, text="Algoritmo Dynamic Time Warping", font=("Calibre", 20)).pack()

        # Criando radiobuttons para escolher a distância utilizada
        tkinter.Label(self.frame, text="Distância:", font=("Calibre", 12)).pack()
        tkinter.Radiobutton(self.frame, text="Distância Euclidiana", variable=self.variavel_distancia, value=Distancia.EUCLIDIANA.value).pack()
        tkinter.Radiobutton(self.frame, text="Distância de Manhattan", variable=self.variavel_distancia, value=Distancia.MANHATTAN.value).pack()

        # Criando entrada de texto para escolher a janela de busca
        tkinter.Label(self.frame, text="Janela de Busca:", font=("Calibre", 12)).pack()
        self.variavel_janela_de_busca = tkinter.StringVar()
        tkinter.Entry(self.frame, textvariable=self.variavel_janela_de_busca).pack()

        # Criando botão para executar o Dynamic Time Warping
        tkinter.Button(self.frame, text="Executar", command=self.executar).pack()

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
        nome_distancia = self.variavel_distancia.get()
        distancia_enum = self.mapa_distancias.get(nome_distancia)
        if distancia_enum is None:
            raise ValueError(f"Distância '{nome_distancia}' não mapeada.")
        janela_de_busca = int(self.variavel_janela_de_busca.get())
        dtw = DynamicTimeWarping(janela_de_busca, distancia_enum)
        resultado = dtw.dtw_distance(self.serie_temporal1, self.serie_temporal2)
        self.resposta_label.config(text=f"Resposta: {resultado}")