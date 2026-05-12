import tkinter


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

        # Menu transformar
        menu_transformar = tkinter.Menu(barra_menu, tearoff=0)
        menu_transformar.add_command(
            label="Gerar matriz de alinhamento",
            command=lambda: controller.gerar_matriz_alinhamento(),
        )
        barra_menu.add_cascade(label="Transformar", menu=menu_transformar)

        # Adicionando menu
        self.config(menu=barra_menu)
