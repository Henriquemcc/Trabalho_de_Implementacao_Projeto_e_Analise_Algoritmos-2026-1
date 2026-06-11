import tkinter
import tkinter.messagebox

from model.ContinuousDynamicTimeWarping import ContinuousDynamicTimeWarping
from model.SerieTemporal import SerieTemporal


class JanelaDistanciaContinuousDynamicTimeWarping(tkinter.Toplevel):
    """
    Janela utilizada para realizar a execução da distância do Continuous Dynamic Time Warping
    """
    def __init__(self, serie_temporal1: SerieTemporal, serie_temporal2: SerieTemporal):
        """
        Constrói uma nova instância da JanelaDistanciaContinuousDynamicTimeWarping.
        :param serie_temporal1: Primeira série temporal.
        :param serie_temporal2: Segunda série temporal.
        """
        tkinter.Toplevel.__init__(self)

        # Definindo título
        self.title("Continuous Dynamic Time Warping")

        # Séries temporais
        self.serie_temporal1 = serie_temporal1
        self.serie_temporal2 = serie_temporal2

        # Variáveis
        self.variavel_interpolacao = tkinter.StringVar(value=0.3)
        self.variavel_num_stainer = tkinter.StringVar(value=5)
        self.variavel_r = tkinter.StringVar(value=100)

        # Configurando o tamanho da janela
        screen_width = 800
        screen_height = 600
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Criando frame
        self.resposta_label = None
        self.criar_frame()

    def criar_frame(self):
        """
        Cria o frame do Continuous Dynamic Time Warping
        :return:
        """
        self.frame = tkinter.Frame(self)

        # Título do Frame
        tkinter.Label(self.frame, text='Algoritmo Continuous Dynamic Time Warping', font=('Calibre', 20)).pack()

        # Criando entradas de texto para escolher os valores de interpolação, num_stainer e r
        ## Interpolação
        tkinter.Label(self.frame, text='Interpolação:', font=('Calibre', 12)).pack()
        tkinter.Entry(self.frame, textvariable=self.variavel_interpolacao).pack()

        ## num_stainer
        tkinter.Label(self.frame, text='num_stainer:', font=('Calibre', 12)).pack()
        tkinter.Entry(self.frame, textvariable=self.variavel_num_stainer).pack()

        ## r
        tkinter.Label(self.frame, text='r:', font=('Calibre', 12)).pack()
        tkinter.Entry(self.frame, textvariable=self.variavel_r).pack()

        # Criando botão para executar o Continuous Dynamic Time Warping
        tkinter.Button(self.frame, text="Executar", command=self.executar).pack()

        # Criando label para mostrar a resposta do Continuous Dynamic Time Warping
        self.resposta_label = tkinter.Label(self.frame, text="Resposta:", font=("Calibre", 12))
        self.resposta_label.pack()

        self.frame.pack(fill=tkinter.BOTH, expand=True)

    def executar(self):
        """
        Realiza a execução do Continuous Dynamic Time Warping.
        :return:
        """
        try:
            cdtw = ContinuousDynamicTimeWarping(interpolacao=float(self.variavel_interpolacao.get()),
                num_stainer=int(self.variavel_num_stainer.get()),
                r=int(self.variavel_r.get()))
            resultado = cdtw.cdtw_distance(
                serie1=self.serie_temporal1,
                serie2=self.serie_temporal2,
            )
            self.resposta_label.config(text=f"Resposta: {resultado}")
        except Exception as e:
            tkinter.messagebox.showerror(title='Erro ao executar o Continuous Dynamic Time Warping', message=str(e))
            print(e)

