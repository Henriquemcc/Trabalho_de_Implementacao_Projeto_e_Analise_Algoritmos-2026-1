import tkinter

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
        titulo = tkinter.Label(self, text="Trabalho de Implementação - Projeto e Análise de Algoritmos - 2026-1")
        titulo.pack(side="top", fill="x", pady=10)
        autor = tkinter.Label(self, text="Henrique Mendonça Castelar Campos")
        autor.pack(side="top", fill="x", pady=10)
        self.pack()