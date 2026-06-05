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
    """
    Representa um ponto no espaço euclidiano para o algoritmo CDTW.
    Fonte: https://github.com/gregwood-db/cdtw/blob/master/cdtw_classes.py
    """
    def __init__(self, x, y, tipo: TipoNoCdtw = TipoNoCdtw.NATIVO):

        # A distância inicial deve ser 0
        self.distancia = 0

        # Tipo de nó
        self.tipo = tipo

        # Convertendo os valores de x e y para float
        try:
            self.x = float(x)
            self.y = float(y)
        except ValueError as e:
            raise ValueError('Coordenadas precisam ser números')

        # Estado se o nó foi visitado
        self.visitado = False

        # ID único do nó
        self.id = id(self)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return 'Nó com id {}'.format(self.id)

    def __add__(self, other):
        return NoCdtw(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return NoCdtw(self.x - other.x, self.y - other.y)

    def mostrar(self):
        print('Nó CDTW com as seguintes propriedades:')
        print('Localização: ({};{})'.format(self.x, self.y))
        print('Distância: {}'.format(self.distancia))
        print('Tipo de nó: {}'.format(self.tipo.name))

    def calcular_distancia(self, other: NoCdtw) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** (1/2)


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