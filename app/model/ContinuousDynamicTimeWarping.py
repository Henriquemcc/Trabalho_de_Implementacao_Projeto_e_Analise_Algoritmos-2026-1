import numpy
from enum import Enum

from model.SerieTemporal import SerieTemporal
from model.Distancia import Distancia, distancia_manhattan, distancia_euclidiana, distancia_euclidiana_ao_quadrado

class TipoNoCdtw(Enum):
    """
    Representa o tipo de um Nó do algoritmo CDTW
    """
    NATIVO = 'Nativo'
    STEINER = 'Steiner'

class NoCdtw:
    pass

class CurvaCdtw:
    pass

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

    def cdtw_distance(self, serie1: SerieTemporal | list | numpy.ndarray, serie2: SerieTemporal | list | numpy.ndarray, interop= 0.3, num_stainer = 5, r = 100) -> float:

        # Retirando o array dados do objeto SerieTemporal da serie1
        if hasattr(serie1, 'dados'):
            c1 = serie1.dados
        else:
            c1 = serie1

        # Retirando o array dados do objeto SerieTemporal da serie2
        if hasattr(serie2, 'dados'):
            c2 = serie2.dados
        else:
            c2 = serie2