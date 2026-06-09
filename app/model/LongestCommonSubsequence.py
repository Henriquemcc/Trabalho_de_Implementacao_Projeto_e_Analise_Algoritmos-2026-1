import numpy

from model import SerieTemporal


class LongestCommonSubsequence:
    @staticmethod
    def lcs(serie1: SerieTemporal | list | numpy.ndarray, serie2: SerieTemporal | list | numpy.ndarray) -> int:
        """
        Realiza o cálculo do comprimento da LongestCommonSubsequence (Sequência Comum Mais Longa).
        :param serie1: Primeira série temporal.
        :param serie2: Segunda série temporal.
        :return: Número inteiro contendo o comprimento da LongestCommonSubsequence
        Fonte: https://www.geeksforgeeks.org/dsa/longest-common-subsequence-dp-4/
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

        # Realizando recursão
        return LongestCommonSubsequence.__lcs_recursiva(s1, s2, m, n)

    @staticmethod
    def __lcs_recursiva(s1, s2, m, n) -> int:
        # Caso base: Se ambas os arrays tiverem sido percorridos, o tamanho da LCS seré 0
        if m == 0 and n == 0:
            return 0

        # Se os elementos de ambos arrays baterem
        if s1[m - 1] == s2[n - 1]:
            # Realizando outra recursão
            return 1 + LongestCommonSubsequence.__lcs_recursiva(s1, s2, m - 1, n - 1)

        # Se os elementos de ambos os arrays não baterem
        # Calculando o máximo do LCS de um com m e n-1 e outro com m-1 e n.
        else:
            return max(LongestCommonSubsequence.__lcs_recursiva(s1, s2, m, n - 1), LongestCommonSubsequence.__lcs_recursiva(s1, s2, m - 1, n))


