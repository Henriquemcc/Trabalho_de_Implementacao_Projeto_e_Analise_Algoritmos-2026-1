import tkinter
import tkinter.messagebox

from model.DerivativeDynamicTimeWarping import DerivativeDynamicTimeWarping
from model.SerieTemporal import SerieTemporal


class JanelaDistanciaDerivativeDynamicTimeWarping(tkinter.Toplevel):
    """
    Janela para realizar a execução da distância do Derivative Dynamic Time Warping.
    """
    def __init__(self, serie1: SerieTemporal, serie2: SerieTemporal):
        """
        Constrói uma nova instância da JanelaDerivativeDyanamicTimeWarping.
        :param serie1: Primeira série temporal.
        :param serie2: Segunda série temporal.
        """
        tkinter.Toplevel.__init__(self)
        self.title("Derivative Dynamic Time Warping")
        self.serie1 = serie1
        self.serie2 = serie2
        self.variavel_janela_de_busca = tkinter.StringVar(value='10')

        # Configurando o tamanho da janela
        screen_width = 1200
        screen_height = 600
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Criando frame
        self.resposta_label = None
        self.criar_frame()

    def criar_frame(self):
        """
        Cria o frame do Derivative Dynamic Time Warping
        :return:
        """
        self.frame = tkinter.Frame(self)

        # Título do Frame
        tkinter.Label(self.frame, text="Algoritmo Derivative Dynamic Time Warping", font=("Calibre", 20)).pack()

        # Criando entrada de texto para escolher a janela de busca
        tkinter.Label(self.frame, text="Janela de Busca:", font=("Calibre", 12)).pack()
        tkinter.Entry(self.frame, textvariable=self.variavel_janela_de_busca).pack()

        # Criando botão para executar o Derivative Dynamic Time Warping
        tkinter.Button(self.frame, text="Executar", command=self.executar).pack()

        # Criando label para mostrar a resposta do Derivative Dynamic Time Warping
        self.resposta_label = tkinter.Label(self.frame, text='Resposta:', font=('Calibre', 12))
        self.resposta_label.pack()

        self.frame.pack(fill=tkinter.BOTH, expand=True)

    def executar(self):
        """
        Realiza a execução do Derivative Dynamic Time Warping.
        :return:
        """
        try:
            janela_de_busca = int(self.variavel_janela_de_busca.get())
            ddtw = DerivativeDynamicTimeWarping(janela_de_busca)
            resultado, _ = ddtw.warping_paths(self.serie1, self.serie2)
            self.resposta_label.config(text=f'Resposta: {resultado}')
        except Exception as e:
            tkinter.messagebox.showerror(title='Erro ao executar o Derivative Dynamic Time Warping', message=str(e))
            print(e)