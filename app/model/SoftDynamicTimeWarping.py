from math import gamma
from typing import Any

import numpy
from numpy import dtype, float64, ndarray

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
        WarpingPathAlgorithm.__init__(self, nome_algoritmo='Soft Dynamic Time Warping')
        self.gamma = gamma

    def calcular_distancia_euclidiana_ao_quadrado(self, serie1: numpy.ndarray, serie2: numpy.ndarray) -> numpy.ndarray:
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

    def soft_dtw_forward(self, d: numpy.ndarray):
        """
        Realiza a passagem para frente (Forward) do algoritmo Soft Dynamic Time Warping.
        :param d: Matriz de distâncias locais de tamanho n por m.
        :return: Tupla com a distância Soft-DTW final, e a matriz de custos acumulados de tamanho n+2 por m+2 usada no backward.
        """

        # Obtendo o tamanho das séries temporais
        n, m = d.shape

        # Criando matriz r com bordas extras para simplificar os índices (tamanho n+2 por m+2)
        r = numpy.full((n + 2, m + 2), numpy.inf)

        # Definindo o primeiro valor da matriz como 0
        r[0, 0] = 0.0

        # Realizando o preenchimento da matriz de custos acumulados de esquerda-superior para a direita-inferior
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                # Calculando os vizinhos: esquerda, cima, diagonal superior esquerda
                r0 = r[i, j - 1]
                r1 = r[i - 1, j]
                r2 = r[i - 1, j - 1]

                # Calculando o custo atual
                # custo atual = distância local + softmin dos vizinhos
                r[i, j] = d[i - 1, j - 1] + self.softmin(r0, r1, r2)

        # Obtendo a distância final
        distancia_final = r[n, m]

        # Retornando a distância final e a matriz de custos acumulados
        return distancia_final, r

    def soft_dtw_backward(self, d: numpy.ndarray, r: numpy.ndarray):
        """
        Realiza a passagem para trás (Backward) do algoritmo Soft Dynamic Time Warping.
        :param d: Matriz de distâncias locais de tamanho n por m.
        :param r: Matriz de custos acumulados gerada no Forward (de tamanho n+2 por m+2).
        :return: Matriz de alinhamento suave (de tamanho n por m).
        """
        # Obtendo o tamanho das séries temporais
        n, m = d.shape

        # Criando uma matriz inicializada com bordas extras (de tamanho n+2 por m+2)
        e = numpy.zeros((n + 2, m + 2))

        # Inicializando o primeiro elemento dessa matriz (canto inferior direito) com 1
        e[n, m] = 1.0

        # Adicionando uma linha e uma coluna fantasma em r
        r[n + 1, :] = numpy.inf
        r[:, m + 1] = numpy.inf
        r[n + 1, m + 1] = r[n, m]

        # Iterando da direita canto inferior para a esquerda canto superior
        for j in range(m, 0, -1):
            for i in range(n, 0, -1):
                # Contribuição vinda do vizinho direito
                a = numpy.exp((r[i, j + 1] - r[i, j] - d[i - 1, j]) / self.gamma) if j < m else 0.0

                # Contribuição vinda do vizinho de baixo
                b = numpy.exp((r[i + 1, j] - r[i, j] - d[i, j - 1]) / self.gamma) if i < n else 0.0

                # Contribuição vinda do vizinho da diagonal do canto inferior direito
                c = numpy.exp(r[i + 1, j + 1] - r[i, j] - d[i, j] / self.gamma) if (i < n and j < m) else 0.0

                # Atualizando o alinhamento esperado da célula atual baseado no fluxo reverso
                if i == n and j == m:
                    e[i, j] = 1.0
                else:
                    e[i, j] = e[i, j + 1] * a + e[i + 1, j] * b + e[i + 1, j + 1] * c

        # Retornando a matriz sem as bordas extras
        return e[1:(n + 1), 1:(m + 1)]

    def warping_paths(self, serie1, serie2) -> tuple[
        ndarray[tuple[Any, ...], dtype[Any]], ndarray[tuple[Any, ...], dtype[float64]]]:
        """
        Realiza o cálculo da distância de duas séries temporais através do algoritmo Soft Dynamic Time Warping.
        :param serie1: Primeira série temporal.
        :param serie2: Segunda série temporal.
        :return: Custo acumulado e matriz de rastreamento.
        """

        # Retirando o array dados do objeto SerieTemporal da serie1
        if type(serie1).__name__ == 'SerieTemporal':
            s1 = numpy.array(serie1.dados)
        else:
            s1 = numpy.array(serie1)

        # Retirando o array dados do objeto SerieTemporal da serie2
        if type(serie2).__name__ == 'SerieTemporal':
            s2 = numpy.array(serie2.dados)
        else:
            s2 = numpy.array(serie2)

        # Calculando a distância euclidiana ao quadrado
        d = self.calcular_distancia_euclidiana_ao_quadrado(serie1, serie2)

        # Executando o Forward
        distancia, r = self.soft_dtw_forward(d)

        # Executando o Backward
        e = self.soft_dtw_backward(d, r)

        return distancia, e