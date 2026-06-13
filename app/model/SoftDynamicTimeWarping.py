import numpy

from model.Distancia import distancia_euclidiana_ao_quadrado
from model.WarpingPathAlgorithm import WarpingPathAlgorithm


class SoftDynamicTimeWarping(WarpingPathAlgorithm):
    """
    Implementação do algoritmo Soft Dynamic Time Warping.
    """
    def __init__(self, gamma: float |  int = 1.0):
        """
        Constrói uma nova instância da classe SoftDynamicTimeWarping.
        :param gamma: Parâmetro de regularização.
        """
        self.gamma = gamma

    def distancia_euclidiana_ao_quadrado(self, serie1: numpy.ndarray, serie2: numpy.ndarray) -> numpy.ndarray:
        """
        Calcula a distância euclidiana ao quadrado entre duas séries temporais.
        :param serie1: Primeira série temporal.
        :param serie2: Segunda série temporal.
        :return: Numpy array contendo a distância euclidiana.
        """
        # Obtendo o tamanho das séries temporais
        n = len(serie1)
        m = len(serie2)

        # Criando matriz vazia
        distancia = numpy.zeros((n, m))

        # Preenchendo matriz com a distância euclidiana ao quadrado de cada elemento
        for i in range(n):
            for j in range(m):
                distancia[i, j] = (serie1[i] - serie2[j]) ** 2

        return distancia

    def warping_paths(self, serie1, serie2) -> tuple[float | int, numpy.ndarray]:
        pass