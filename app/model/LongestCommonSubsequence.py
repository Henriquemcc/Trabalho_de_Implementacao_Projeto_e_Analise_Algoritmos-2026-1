import numpy

from model import SerieTemporal


class LongestCommonSubsequence:
    @staticmethod
    def lcs(serie1: SerieTemporal | list | numpy.ndarray, serie2: SerieTemporal | list | numpy.ndarray) -> int:
        """
        Realiza o cálculo do comprimento da LongestCommonSubsequence (Sequência Comum Mais Longa) utilizando sua implementação normal.
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
        if m == 0 or n == 0:
            return 0

        # Se os elementos de ambos arrays baterem
        if s1[m - 1] == s2[n - 1]:
            # Realizando outra recursão
            return 1 + LongestCommonSubsequence.__lcs_recursiva(s1, s2, m - 1, n - 1)

        # Se os elementos de ambos os arrays não baterem
        # Calculando o máximo do LCS de um com m e n-1 e outro com m-1 e n.
        else:
            return max(LongestCommonSubsequence.__lcs_recursiva(s1, s2, m, n - 1), LongestCommonSubsequence.__lcs_recursiva(s1, s2, m - 1, n))

    class LongestCommonSubsequenceProgramacaoDinamica:
        def __init__(self):
            # Variável que armazena os cálculos anteriores
            self.__programacao_dinamica = {}

        def lcs(self, serie1: SerieTemporal | list | numpy.ndarray, serie2: SerieTemporal | list | numpy.ndarray)-> int:
            """
            Realiza o cálculo do comprimento da LongestCommonSubsequence (Sequência Comum Mais Longa) utilizando sua implementação com programação dinâmica.
            :param serie1: Primeira série temporal
            :param serie2: Segunda série temporal
            :return: Número inteiro contendo o comprimento da LongestCommonSubsequence
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

            # Executando versão recursiva
            return self.__lcs_recursiva(s1, s2, m, n)

        def __lcs_recursiva(self, s1, s2, m, n) -> int:
            # Caso base: Se ambas os arrays tiverem sido percorridos, o tamanho da LCS seré 0
            if m == 0 or n == 0:
                return 0

            # Se os elementos de ambos arrays baterem
            if s1[m - 1] == s2[n - 1]:
                soma = 1
                parametros = (s1, s2, m - 1, n - 1)
                if parametros not in self.__programacao_dinamica:
                    self.__programacao_dinamica[parametros] = self.__lcs_recursiva(*parametros)
                return soma + self.__programacao_dinamica[parametros]

            # Se os elementos de ambos os arrays não baterem
            # Calculando o máximo do LCS de um com m e n-1 e outro com m-1 e n.
            else:
                parametros1 = (s1, s2, m, n - 1)
                # Executando recursão somente se ela não tiver sido executada anteriormente
                if parametros1 not in self.__programacao_dinamica:
                    self.__programacao_dinamica[parametros1] = self.__lcs_recursiva(*parametros1)

                parametros2 = (s1, s2, m - 1, n)
                # Executando recursão somente se ela não tiver sido executada anteriormente
                if parametros2 not in self.__programacao_dinamica:
                    self.__programacao_dinamica[parametros2] = self.__lcs_recursiva(*parametros2)

                return max(self.__programacao_dinamica[parametros1], self.__programacao_dinamica[parametros2])
