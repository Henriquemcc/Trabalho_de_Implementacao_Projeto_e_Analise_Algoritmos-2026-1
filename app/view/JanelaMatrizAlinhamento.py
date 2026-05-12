import tkinter
from matplotlib.figure import Figure
from model.MatrizAlinhamento import MatrizAlinhamento

class JanelaMatrizAlinhamento(tkinter.Tk):
    """
    Janela utilizada para exibir uma matriz de alinhamento.
    """
    def __init__(self, matriz_alinhamento: MatrizAlinhamento):
        tkinter.Tk.__init__(self)
        self.title("Matriz de Alinhamento")
        self.matriz_alinhamento = matriz_alinhamento

        # Configurando o tamanho da janela
        screen_width = 500
        screen_height = 350
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
        ax = fig.add_subplot(111)

        # Plotando matriz de alinhamento



        self.frame.pack()

