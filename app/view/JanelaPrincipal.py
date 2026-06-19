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

        # Menu matriz de alinhamento
        menu_matriz_alinhamento = tkinter.Menu(barra_menu, tearoff=0)
        menu_matriz_alinhamento.add_command(
            label="Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_alinhamento('DTW'),
        )
        menu_matriz_alinhamento.add_command(
            label="Derivative Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_alinhamento('DDTW')
        )
        menu_matriz_alinhamento.add_command(
            label="Continuous Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_alinhamento('CDTW')
        )
        menu_matriz_alinhamento.add_command(
            label='Longest Common Subsequence',
            command=lambda: controller.gerar_matriz_alinhamento('LCS')
        )
        menu_matriz_alinhamento.add_command(
            label="Soft Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_alinhamento('Soft-DTW')
        )
        barra_menu.add_cascade(label='Matriz de Alinhamento', menu=menu_matriz_alinhamento)

        # Menu matriz_mapeamento
        menu_matriz_mapeamento = tkinter.Menu(barra_menu, tearoff=0)
        menu_matriz_mapeamento.add_command(
            label="Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_mapeamento('DTW'),
        )
        menu_matriz_mapeamento.add_command(
            label="Derivative Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_mapeamento('DDTW')
        )
        menu_matriz_mapeamento.add_command(
            label="Continuous Dynamic Time Warping",
            command=lambda: controller.gerar_matriz_mapeamento('CDTW')
        )
        menu_matriz_mapeamento.add_command(
            label='Longest Common Subsequence',
            command=lambda: controller.gerar_matriz_mapeamento('LCS')
        )
        menu_matriz_mapeamento.add_command(
            label='Soft Dynamic Time Warping',
            command=lambda: controller.gerar_matriz_mapeamento('Soft-DTW')
        )
        barra_menu.add_cascade(label='Matriz de Mapeamento', menu=menu_matriz_mapeamento)

        # Menu distância
        menu_distancia = tkinter.Menu(barra_menu, tearoff=0)
        menu_distancia.add_command(
            label="Dynamic Time Warping",
            command=lambda: controller.executar_distancia_dynamic_time_warping(),
        )
        menu_distancia.add_command(
            label="Continuous Dynamic Time Warping",
            command=lambda: controller.executar_distancia_continuous_dynamic_time_warping(),
        )
        menu_distancia.add_command(
            label='Longest Common Subsequence',
            command=lambda: controller.executar_distancia_longest_common_subsequence(),
        )
        menu_distancia.add_command(
            label='Derivative Dynamic Time Warping',
            command=lambda: controller.executar_distancia_derivative_dynamic_time_warping(),
        )
        menu_distancia.add_command(
            label='Soft Dynamic Time Warping',
            command=lambda: controller.executar_distancia_soft_dynamic_time_warping(),
        )
        barra_menu.add_cascade(label="Distância", menu=menu_distancia)

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

