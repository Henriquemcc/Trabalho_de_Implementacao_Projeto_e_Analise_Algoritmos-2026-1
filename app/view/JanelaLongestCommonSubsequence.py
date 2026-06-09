import tkinter

from model.LongestCommonSubsequence import LongestCommonSubsequence
from model.SerieTemporal import SerieTemporal


class JanelaLongestCommonSubsequence(tkinter.Toplevel):
    """
    Janela utilizada para realizar a execução do Longest Common Subsequence
    """
    def __init__(self, serie_temporal1: SerieTemporal, serie_temporal2: SerieTemporal):
        """
        Constrói uma nova instância da JanelaLongestCommonSubsequence.
        :param serie_temporal1: Primeira série temporal.
        :param serie_temporal2: Segunda série temporal.
        """
        tkinter.Toplevel.__init__(self)

        # Definindo título
        self.title('Longest Common Subsequence')

        # Séries temporais
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
        Cria o frame do Longest Common Subsequence
        :return:
        """
        self.frame = tkinter.Frame(self)

        # Título do Frame
        tkinter.Label(self.frame, text='Algoritmo Longest Common Subsequence', font=('Calibre', 20)).pack()

        # Criando botão para executar o Longest Common Subsequence
        tkinter.Button(self.frame, text='Executar', command=self.executar).pack()

        # Criando label para mostrar a resposta do Longest Common Subsequence
        self.resposta_label = tkinter.Label(self.frame, text='Resposta:', font=('Calibre', 12))
        self.resposta_label.pack()

        self.frame.pack(fill=tkinter.BOTH, expand=True)

    def executar(self):
        """
        Realiza a execução do Longest Common Subsequence.
        :return:
        """
        try:
            resultado = LongestCommonSubsequence.lcs_normal(
                serie1=self.serie_temporal1,
                serie2=self.serie_temporal2
            )
            self.resposta_label.config(text=f'Resposta: {resultado}')
        except Exception as e:
            tkinter.messagebox.showerror(title='Erro ao executar o Longest Common Subsequence', message=str(e))
            print(e)