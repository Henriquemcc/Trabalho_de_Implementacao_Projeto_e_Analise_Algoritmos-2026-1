import collections
from typing import Any

import numpy

from model.SerieTemporal import SerieTemporal


class DerivativeDynamicTimeWarping:
    """
    Implementação do algoritmo Derivative Dynamic Time Warping
    """

    @staticmethod
    def __estimar_derivadas(serie: numpy.ndarray) -> numpy.ndarray:
        """
        Realiza o cálculo das derivadas.
        :param serie: Dados da série temporal.
        :return: Derivada dos dados da série temporal.
        """
        if len(serie) < 3:
            raise ValueError('O tamanho da série temporal deve ser maior que 3 elementos')

        if type(serie) != numpy.ndarray:
            raise ValueError('O tipo do parâmetro `serie` deve ser um numpy array')

        # Calculando as derivadas
        derivada_0 = serie[:-2]
        derivada_1 = serie[1:-1]
        derivada_2 = serie[2:]
        derivada_serie = ((derivada_1 - derivada_0) + (derivada_2 - derivada_0)/2)/2

        return derivada_serie

    @staticmethod
    def __gerar_janela(tamanho_derivada_s1: int, tamanho_derivada_s2: int, K: int):
        """
        Gera a janela do espaço de busca reduzido
        :param tamanho_derivada_s1: Tamanho da série temporal 1
        :param tamanho_derivada_s2: Tamanho de série temporal 2
        :param K: Largura da janela de restrição global, também conhecido como Janela de Sakoe-Chiba.
        :return: Janela do espaço de busca reduzido.
        """
        for i in range(tamanho_derivada_s1):

            # Calculando os limites superior e inferior
            limite_inferior = i - K
            limite_superior = i + K

            if limite_inferior < 0 and limite_superior < tamanho_derivada_s2:
                for j in range(limite_superior):
                    yield (i + 1, j + 1)
            elif limite_inferior >= 0 and limite_superior < tamanho_derivada_s2:
                for j in range(limite_inferior, limite_superior):
                    yield (i + 1, j + 1)
            elif limite_inferior < 0 and limite_superior >= tamanho_derivada_s2:
                for j in range(tamanho_derivada_s2):
                    yield (i + 1, j + 1)
            elif limite_inferior >= 0 and limite_superior >= tamanho_derivada_s2:
                for j in range(limite_inferior, tamanho_derivada_s2):
                    yield (i + 1, j + 1)

    @staticmethod
    def ddtw(serie1: SerieTemporal | list | numpy.ndarray, serie2: SerieTemporal | list | numpy.ndarray, K: int = 10) -> tuple[float, list[Any]]:
        """
        Realiza o cálculo da distância de duas séries temporais através do algoritmo Derivative Dynamic Time Warping.
        :param serie1: Primeira série temporal.
        :param serie2: Segunda série temporal.
        :param K: Largura da janela de restrição global, também conhecido como Janela de Sakoe-Chiba.
        :return: Custo acumulado e matriz de rastreamento.
        Fonte: https://github.com/z2e2/fastddtw/blob/master/_fastddtw.py
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

        # Calculando as derivadas de s1 e s2
        derivada_s1 = DerivativeDynamicTimeWarping.__estimar_derivadas(s1)
        derivada_s2 = DerivativeDynamicTimeWarping.__estimar_derivadas(s2)

        # Obtendo o tamanho das derivadas
        tamanho_derivada_s1 = len(derivada_s1)
        tamanho_derivada_s2 = len(derivada_s2)

        # Alterando o valor de K
        if K <= abs(tamanho_derivada_s1 - tamanho_derivada_s2):
            K = 2 * abs(tamanho_derivada_s1 - tamanho_derivada_s2)
            print('O valor de K foi alterado para {}'.format(K))

        # Definido o valor da janela
        janela = DerivativeDynamicTimeWarping.__gerar_janela(tamanho_derivada_s1, tamanho_derivada_s2, K)

        # Criando a matriz de custo acumulado com os valores iguais a infinito
        matriz_custo_acumulado = collections.defaultdict(lambda: (float('inf'),))

        # Definindo o primeiro valor da matriz
        matriz_custo_acumulado[0, 0] = (0, 0, 0)

        # Interando pelo tamanho da janela
        for i, j in janela:
            derivada_t = abs(derivada_s1[i - 1] - derivada_s2[j - 1])
            matriz_custo_acumulado[i, j] = min((matriz_custo_acumulado[i - 1, j][0]+derivada_t, i-1, j),
                                               (matriz_custo_acumulado[i, j - 1][0]+derivada_t, i, j-1),
                                               (matriz_custo_acumulado[i-1, j-1][0]+derivada_t, i-1, j-1), key=lambda a: a[0]
                                               )

        # Matriz de rastreamento
        matriz_rastreamento = []

        # Definindo os novos valores para i e j
        i =  tamanho_derivada_s1
        j = tamanho_derivada_s2
        while not(i == j == 0):
            matriz_rastreamento.append((i - 1, j - 1))

            # Definindo os novos valores para i e j
            i, j = matriz_custo_acumulado[i, j][1], matriz_custo_acumulado[i, j][2]

        # Invertendo a ordem dos elementos
        matriz_rastreamento.reverse()

        return matriz_custo_acumulado[tamanho_derivada_s1, tamanho_derivada_s2][0], matriz_rastreamento
