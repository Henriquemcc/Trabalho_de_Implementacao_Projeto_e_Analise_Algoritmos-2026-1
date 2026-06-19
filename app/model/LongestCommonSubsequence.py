import numpy

from model import SerieTemporal
from model.WarpingPathAlgorithm import WarpingPathAlgorithm


class LongestCommonSubsequence(WarpingPathAlgorithm):
    """
    Implementação do algoritmo Longest Common Subsequence.
    """
    def __init__(self):
        """
        Constrói uma nova instância de LongestCommonSubsequence.
        """
        WarpingPathAlgorithm.__init__(self, nome_algoritmo='Longest Common Subsequence')

    def warping_paths(self, serie1: SerieTemporal | list | numpy.ndarray, serie2: SerieTemporal | list | numpy.ndarray)-> tuple[float | int, numpy.ndarray]:
        """
        Realiza o cálculo do comprimento da LongestCommonSubsequence (Sequência Comum Mais Longa) utilizando sua implementação com programação dinâmica.
        :param serie1: Primeira série temporal
        :param serie2: Segunda série temporal
        :return: Número inteiro contendo o comprimento da LongestCommonSubsequence
        Fonte: https://www.programiz.com/dsa/longest-common-subsequence
        """

        # Retirando o array dados do objeto SerieTemporal da serie1
        if type(serie1).__name__ == 'SerieTemporal':
            s1 = serie1.dados
        else:
            s1 = serie1

        # Retirando o array dados do objeto SerieTemporal da serie2
        if type(serie2).__name__ == 'SerieTemporal':
            s2 = serie2.dados
        else:
            s2 = serie2

        # Obtendo o tamanho das séries
        m = len(s1)
        n = len(s2)

        # Iniciando uma matriz de zeros com dimensões (m + 1) por (n + 1)
        matriz_lcs = [[0 for x in range(n + 1)] for x in range(m + 1)]

        # Construindo a matriz utilizando Programação Dinâmica
        for i in range(m + 1):
            for j in range(n + 1):
                # Caso base: Se ambos os arrays tiverm sido percorridos, o tamanho da LCS será 0
                if i == 0 or j == 0:
                    matriz_lcs[i][j] = 0

                # Se os elementos de ambos os arrays baterem
                elif s1[i - 1] == s2[j - 1]:
                    # Incrementando 1 da diagonal superior esquerda
                    matriz_lcs[i][j] = matriz_lcs[i - 1][j - 1] + 1

                # Se os elementos de ambos arrays não baterem
                else:
                    # Obtendo o maior valor possível entre os seus dois vizinhos
                    matriz_lcs[i][j] = max(matriz_lcs[i - 1][j], matriz_lcs[i][j - 1])

        # O valor contido na última célula da matriz é o tamanho da maior subsequência comum encontrada
        tamanho_maior_subsequencia = matriz_lcs[m][n]

        # Criando um array para armazenar a maior subsequência
        maior_subsequencia = []

        # Realizando o Backtracking da matriz utilizada na programação dinâmica
        i = m
        j = n
        while i > 0 and j > 0:
            # Se o elemento da primeira série for igual ao elemento da segunda série na posição atual
            if s1[i - 1] == s2[j - 1]:
                maior_subsequencia.insert(0, [i - 1, j - 1])
                i -= 1
                j -= 1

            # Se o elemento da primeira série for diferente do elemento da segunda série na posição atual, será analisado o maior valor
            elif matriz_lcs[i - 1][j] > matriz_lcs[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return tamanho_maior_subsequencia, numpy.array(maior_subsequencia)
