import tkinter

from pandas.core.reshape import tile


class JanelaSelecionarSerieTemporal(tkinter.Tk):
    def __init__(self, titulo, mensagem, series_temporais: list, confirmar):
        """
        Janela utilizada para selecionar uma série temporal.
        """
        tkinter.Tk.__init__(self)
        self.series_temporais = series_temporais
        self.titulo = titulo
        self.mensagem = mensagem
        self.confirmar = confirmar
        self.title(titulo)
        self.geometry("300x200")

        # Criando frame
        self.criar_botoes()

    def criar_botoes(self):
        """
        Cria o frame da série temporal.
        :return:
        """
        variavel_serie_temporal = tkinter.StringVar(value="Série Temporal")
        tkinter.Label(self, text=self.mensagem, font=("Calibre", 12))

        # Criando um radiobutton para cada série temporal
        for serie_temporal in self.series_temporais:
            tkinter.Radiobutton(self, text=serie_temporal.nome, variable=variavel_serie_temporal, value=serie_temporal.nome)

        # Criando um botão de confirmar
        btn_confirmar = tkinter.Button(self, text="Confirmar", command=self.confirmar)


