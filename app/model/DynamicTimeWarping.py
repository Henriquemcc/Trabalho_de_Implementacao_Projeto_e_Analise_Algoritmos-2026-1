from model.SerieTemporal import SerieTemporal
import math
from enum import Enum

class Distancia(Enum):
    EUCLIDIANA = "euclidiana"
    MANHATTAN = "manhattan"

def distancia_euclidiana(x: float, y: float) -> float:
    """
    Calcula a distância euclidiana entre x e y.
    :param x: Valor de x.
    :param y: Valor de y.
    :return: Distância euclidiana entre x e y.
    """
    return math.sqrt(math.pow((x - y), 2))

def distancia_manhattan(x: float, y: float) -> float:
    """
    Calcula a distância de manhattan entre x e y.
    :param x: Valor de x.
    :param y: Valor de y.
    :return: Distância de manhattan entre x e y.
    """
    return math.fabs(x - y)


class DynamicTimeWarping:
    """
    Implementação do algoritmo Dynamic Time Warping com a opção janela de busca.
    """
    def __init__(self, janela_de_busca: int, distancia: Distancia):
        """
        Inicializa o algoritmo Dynamic Time Warping.
        :param janela_de_busca: Tamanho da janela de busca.
        :param distancia: Tipo de distância a ser utilizado.
        """
        self.janela_de_busca = janela_de_busca
        self.distancia = None
        if distancia == Distancia.MANHATTAN:
            self.distancia = distancia_manhattan
        elif distancia == Distancia.EUCLIDIANA:
            self.distancia = distancia_euclidiana
        else:
            ValueError(f"Tipo de distância inválido: {distancia}")

    def dtw_distance(self, serie1: SerieTemporal, serie2: SerieTemporal):
        """
        Realiza o cálculo da distância de duas séries temporais através do algoritmo Dynamic Time Warping.
        :param serie1: Primeira série temporal.
        :param serie2: Segunda série temporal.
        Fonte: https://en.wikipedia.org/wiki/Dynamic_time_warping#Implementation
        """
        s = serie1.dados
        t = serie2.dados
        n = len(s)
        m = len(t)

        # Matriz com n+1 por m+1 para acomodar a linha/coluna zero (vazia)
        dtw = {}

        # Adaptando a janela de busca
        w = max(self.janela_de_busca, abs(n-m))

        # Inicialização: Colocando infinito para todos
        for i in range(0, n+1):
            for j in range(0, m+1):
                dtw[i, j] = float('inf')

        # Ponto de partida
        dtw[0, 0] = 0

        # Calculando o custo e o dtw
        for i in range(1, n + 1):
            for j in range(max(1, i-w), min(m, i+w) + 1):
                custo = self.distancia(s[i-1], t[j-1])
                dtw[i, j] = custo + min(dtw[i-1, j], # inserção
                                        dtw[i, j-1], # deleção
                                        dtw[i-1, j-1]) # match

        return dtw[n, m]