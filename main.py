import tkinter
from tkinter import filedialog

class FramePrincipal(tkinter.Frame):
    """
    Frame principal da interface gráfica.
    """
    def __init__(self, parent, controller):
        """
        Constrói uma nova instância do FramePrincipal.
        :param parent: Widget pai.
        :param controller: Controlador que instanciou esta classe.
        """
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        titulo = tkinter.Label(self, text="Trabalho de Implementação - Projeto e Análise de Algoritmos - Mestrado em Informática - PUC Minas")
        titulo.pack(side="top", fill="x", pady=10)
        autor = tkinter.Label(self, text="Henrique Mendonça Castelar Campos")
        autor.pack(side="top", fill="x", pady=10)

class JanelaPrincipal(tkinter.Tk):
    """
    Janela principal de interface gráfica.
    """

    def __init__(self, controller, *args, **kwargs):
        """
        Constrói uma nova instância da JanelaPrincipal.
        :param controller: Controlador que instanciou esta classe.
        """
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.controller = controller

        # Definindo o título
        self.title("Trabalho de Implementação - Projeto e Análise de Algoritmos - Mestrado em Informática - PUC Minas")

        # Configurando o tamanho da janela
        screen_width = 500
        screen_height = 350
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Barra de Menu
        barra_menu = tkinter.Menu(self)

        # Menu arquivo
        menu_arquivo = tkinter.Menu(barra_menu, tearoff=0)
        menu_arquivo.add_command(
            label="Abrir série temporal",
            command=lambda: controller.abrir_arquivo_serie_temporal(),
        )
        barra_menu.add_cascade(label="Arquivo", menu=menu_arquivo)

        # Adicionando menu
        self.config(menu=barra_menu)

class Controlador:
    """
    Controlador principal do programa.
    """
    def __init__(self):
        """
        Constrói uma nova instância de Controlador.
        """

        # Tipos de arquivos de série temporal
        self.tipos_arquivos_serie_temporal = [
            ("Todos os arquivos compatíveis", [".txt"]),
            ("Arquivos de séries temporais", ".txt" ),
        ]

        self.janela = JanelaPrincipal(self)
        self.janela.mainloop()

    def abrir_arquivo_serie_temporal(self):
        """
        Realiza a abertura de um arquivo de uma séria temporal.
        :return:
        """
        caminho = filedialog.askopenfilename(filetypes=self.tipos_arquivos_serie_temporal)


if __name__ == "__main__":
    controller = Controlador()