from math import gamma

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

    def softmin(self, r0, r1, r2):
        """
        Realiza o cálculo do operador soft-min.
        """

        # Encontrando o valor de estabilização
        rmin = min(r0, r1, r2)

        # Calculando as exponenciais estabilizadoras
        e0 = numpy.exp(-(r0 - rmin) / self.gamma)
        e1 = numpy.exp(-(r1 - rmin) / self.gamma)
        e2 = numpy.exp(-(r2 - rmin) / self.gamma)

        # Retornando soft-min
        return rmin - self.gamma * numpy.log(e0 + e1 + e2)

    def soft_dtw_forward(self, D):
        """
        Realiza a passagem para frente (Forward) do algoritmo Soft Dynamic Time Warping.
        :param D: Matriz de distâncias locais de tamanho N por M.
        :return: Tupla com a distância Soft-DTW final, e a matriz de custos acumulados de tamanho N+2 por M+2 usada no backward.
        """

        # Obtendo o tamanho das séries temporais
        n, m = D.shape

        # Criando matriz R com bordas extras para simplificar os índices (tamanho N+2 por M+2)
        R = numpy.full((n + 2, m + 2), numpy.inf)

        # Definindo o primeiro valor da matriz como 0
        R[0, 0] = 0.0

        # Realizando o preenchimento da matriz de custos acumulados de esquerda-superior para a direita-inferior
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                # Calculando os vizinhos: esquerda, cima, diagonal superior esquerda
                r0 = R[i, j - 1]
                r1 = R[i - 1, j]
                r2 = R[i - 1, j - 1]

                # Calculando o custo atual
                # custo atual = distância local + softmin dos vizinhos
                R[i, j] = D[i - 1, j - 1] + self.softmin(r0, r1, r2)

        # Obtendo a distância final
        distancia_final = R[n, m]

        # Retornando a distância final e a matriz de custos acumulados
        return distancia_final, R

    def warping_paths(self, serie1, serie2) -> tuple[float | int, numpy.ndarray]:
        pass