import numpy

from model.SerieTemporal import SerieTemporal
from model.Distancia import Distancia, distancia_manhattan, distancia_euclidiana, distancia_euclidiana_ao_quadrado


class ContinuousDynamicTimeWarping:
    """
    Implementação do algoritmo Continuous Dynamic Time Warping.
    """
    def __init__(self, janela_de_busca: int | None = None, distancia: Distancia = Distancia.EUCLIDIANA):

        """
        Inicializa o algoritmo Continuous Dynamic Time Warping.
        :param janela_de_busca: Tamanho da janela de busca.
        :param distancia: Tipo de distância a ser utilizado.
        """
        self.janela_de_busca = janela_de_busca
        self.distancia = None
        if distancia == Distancia.MANHATTAN:
            self.distancia = distancia_manhattan
        elif distancia == Distancia.EUCLIDIANA:
            self.distancia = distancia_euclidiana
        elif distancia == Distancia.EUCLIDIANA_AO_QUADRADO:
            self.distancia = distancia_euclidiana_ao_quadrado
        else:
            ValueError(f"Tipo de distância inválido: {distancia}")