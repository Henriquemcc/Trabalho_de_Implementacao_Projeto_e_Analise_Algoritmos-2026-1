import tkinter


class JanelaSelecionarSerieTemporal(tkinter.Toplevel):
    def __init__(self, titulo, mensagem, series_temporais: list):
        """
        Janela utilizada para selecionar uma série temporal.
        """
        tkinter.Toplevel.__init__(self)
        self.series_temporais = series_temporais
        self.mapa_series = {s.nome: s for s in series_temporais}
        self.resultado = None
        self.titulo = titulo
        self.mensagem = mensagem

        # Definindo janela
        self.title(titulo)
        self.geometry("300x200")
        self.grab_set()

        self.variavel_serie_temporal = tkinter.StringVar(value=series_temporais[0].nome if series_temporais else "")

        self.criar_widgets()

    def confirmar(self):
        nome_escolhido = self.variavel_serie_temporal.get()
        self.resultado = self.mapa_series.get(nome_escolhido)
        self.destroy()

    def criar_widgets(self):
        """
        Cria o frame da série temporal.
        :return:
        """
        tkinter.Label(self, text=self.mensagem, font=("Calibre", 12))

        # Criando um radiobutton para cada série temporal
        for serie_temporal in self.series_temporais:
            tkinter.Radiobutton(self, text=serie_temporal.nome, variable=self.variavel_serie_temporal, value=serie_temporal.nome).pack(anchor='w', padx=20)

        # Criando um botão de confirmar
        tkinter.Button(self, text="Confirmar", command=self.confirmar).pack(pady=20)

    def mostrar(self):
        self.wait_window()
        return self.resultado

