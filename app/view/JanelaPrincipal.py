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
        screen_width = 1000
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
            label="Gerar matriz de alinhamento Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_alinhamento_dtw(),
        )
        menu_transformar.add_command(
            label="Gerar matriz de alinhamento Derivative Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_alinhamento_ddtw()
        )
        menu_transformar.add_command(
            label="Gerar matriz de alinhamento Continuous Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_alinhamento_cdtw()
        )
        menu_transformar.add_command(
            label="Gerar matriz de alinhamento Soft Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_alinhamento_softdtw()
        )
        menu_transformar.add_command(
            label="Gerar matriz de mapeamento Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_mapeamento_dtw(),
        )
        menu_transformar.add_command(
            label="Gerar matriz de mapeamento Derivative Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_mapeamento_ddtw()
        )
        menu_transformar.add_command(
            label="Gerar matriz de mapeamento Continuous Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_mapeamento_cdtw()
        )
        menu_transformar.add_command(
            label="Gerar matriz de mapeamento Soft Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_mapeamento_softdtw()
        )
        barra_menu.add_cascade(label="Transformar", menu=menu_transformar)

        # Menu algoritmo
        menu_algoritmo = tkinter.Menu(barra_menu, tearoff=0)
        menu_algoritmo.add_command(
            label="Distância Dynamic Time Warping",
            command=lambda: controller.executar_distancia_dynamic_time_warping(),
        )
        menu_algoritmo.add_command(
            label="Distância Continuous Dynamic Time Warping",
            command=lambda: controller.executar_distancia_continuous_dynamic_time_warping(),
        )
        menu_algoritmo.add_command(
            label='Longest Common Subsequence',
            command=lambda: controller.executar_longest_common_subsequence(),
        )
        menu_algoritmo.add_command(
            label='Distância Derivative Dynamic Time Warping',
            command=lambda: controller.executar_derivative_dynamic_time_warping(),
        )
        barra_menu.add_cascade(label="Algoritmo", menu=menu_algoritmo)

        # Adicionando menu
        self.config(menu=barra_menu)

        # Criando frame
        self.criar_frame()

    def criar_frame(self):
        self.frame = tkinter.Frame(self)
        titulo = tkinter.Label(self.frame, text="Trabalho de Implementação - Projeto e Análise de Algoritmos - 2026-1")
        titulo.pack(side="top", fill="x", pady=10)
        autor = tkinter.Label(self.frame, text="Henrique Mendonça Castelar Campos")
        autor.pack(side="top", fill="x", pady=10)
        self.frame.pack()

