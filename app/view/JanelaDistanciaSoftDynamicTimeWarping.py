import tkinter

from model.SerieTemporal import SerieTemporal
from model.SoftDynamicTimeWarping import SoftDynamicTimeWarping


class JanelaDistanciaSoftDynamicTimeWarping(tkinter.Toplevel):
    """
    Janela utilizada para realizar a execução da distância do Soft Dynamic Time Warping.
    """
    def __init__(self, serie_temporal1: SerieTemporal, serie_temporal2: SerieTemporal):
        """
        Constrói uma nova instância da JanelaDistanciaSoftDynamicTimeWarping.
        :param serie_temporal1: Primeira série temporal.
        :param serie_temporal2: Segunda série temporal.
        """
        tkinter.Toplevel.__init__(self)
        self.title('Soft Dynamic Time Warping')
        self.serie_temporal1 = serie_temporal1
        self.serie_temporal2 = serie_temporal2
        self.variavel_gamma = tkinter.StringVar(value='1.0')

        # Configurando o tamanho da janela
        creen_width = 800
        screen_height = 600
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Criando frame
        self.resposta_label = None
        self.criar_frame()

    def criar_frame(self):
        """
        Cria o frame do Soft Dynamic Time Warping.
        :return:
        """
        self.frame = tkinter.Frame(self)

        # Título do Frame
        tkinter.Label(self.frame, text='Algoritmo Soft Dynamic Time Warping', font=('Calibre', 20)).pack()

        # Criando entrada de texto para escolher a gamma
        tkinter.Label(self.frame, text='Gamma', font=('Calibre', 12)).pack()
        tkinter.Entry(self.frame, textvariable=self.variavel_gamma).pack()

        # Criando botão para executar o Soft Dynamic Time Warping
        tkinter.Button(self.frame, text='Executar', command=self.executar).pack()

        # Criando label para mostrar a resposta do Soft Dynamic Time Warping
        self.resposta_label = tkinter.Label(self.frame, text='Reposta:', font=('Calibre', 12))
        self.resposta_label.pack()

        self.frame.pack(fill=tkinter.BOTH, expand=True)

    def executar(self):
        """
        Realiza a execução do Soft Dynamic Time Warping.
        :return:
        """
        try:
            gamma = float(self.variavel_gamma.get())
            soft_dtw = SoftDynamicTimeWarping(gamma=gamma)
            _, resultado = soft_dtw.warping_paths(self.serie_temporal1, self.serie_temporal2)
            self.resposta_label.config(text=f'Resposta: {resultado}')
        except Exception as e:
            tkinter.messagebox.showerror(title='Erro ao executar o Soft Dynamic Time Warping', message=str(e))
            print(e)
