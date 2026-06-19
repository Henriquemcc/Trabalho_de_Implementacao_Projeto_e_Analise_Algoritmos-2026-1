import tkinter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from model.SerieTemporal import SerieTemporal


class JanelaSerieTemporal(tkinter.Tk):
    """
    Janela utilizada para exibir uma série temporal.
    """

    def __init__(self, serie_temporal: SerieTemporal):
        tkinter.Tk.__init__(self)
        self.title(serie_temporal.nome)
        self.serie_temporal = serie_temporal

        # Configurando o tamanho da janela
        screen_width = 1200
        screen_height = 600
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Criando frame
        self.criar_frame()

    def criar_frame(self):
        """
        Cria o frame da série temporal.
        :return:
        """
        self.frame = tkinter.Frame(self, bg="white")

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Plotando os dados
        dados = self.serie_temporal.dados
        ax.plot(dados, marker="o", linestyle="-", color="#2c3e50")
        ax.set_title(self.serie_temporal.nome)
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Valor")

        # Adicionando gráfico ao frame
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)

        self.frame.pack()
