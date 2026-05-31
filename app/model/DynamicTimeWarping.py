from model.SerieTemporal import SerieTemporal
import math
from enum import Enum
import numpy

class Distancia(Enum):
    EUCLIDIANA = "euclidiana"
    EUCLIDIANA_AO_QUADRADO = "euclidiana ao quadrado"
    MANHATTAN = "manhattan"

def distancia_euclidiana_ao_quadrado(x: float, y: float) -> float:
    """
    Calcula a distância euclidiana ao quadrado entre x e y.
    :param x: Valor de x
    :param y: Valor de y
    :return: Distância euclidiana ao quadrado entre x e y.
    """
    return math.pow((x- y), 2)

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
    def __init__(self, janela_de_busca: int | None, distancia: Distancia):
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
        elif distancia == Distancia.EUCLIDIANA_AO_QUADRADO:
            self.distancia = distancia_euclidiana_ao_quadrado
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

        # Gerando matriz DTW
        matrix_dtw = self.gerar_matriz_dtw(serie1, serie2)

        # Retornando o elemento das últimas posições dos eixos x e y
        return matrix_dtw[n, m]

    def gerar_matriz_dtw(self, serie1: SerieTemporal, serie2: SerieTemporal) -> numpy.ndarray:
        """
        Cria uma matriz DTW a partir de duas séries temporais
        :param serie1: Primeira série temporal.
        :param serie2: Segunda série temporal.
        :param janela_de_busca: Tamanho da janela.
        :return: Matriz DTW.
        Fonte: https://en.wikipedia.org/wiki/Dynamic_time_warping#Implementation
        """
        s = serie1.dados
        t = serie2.dados
        n = len(s)
        m = len(t)

        # Inicializando a matriz dtw com as dimensões (n+1) por (m+1)
        matriz_dtw = numpy.full((n+1, m+1), numpy.inf)

        # Definindo a condição de contorno inicial
        matriz_dtw[0, 0] = 0

        # Adaptando a janela de busca
        if self.janela_de_busca is None:
            w = abs(n - m)
        else:
            w = max(self.janela_de_busca, abs(n - m))

        # Preenchendo a matriz respeitando a janela de restrição
        for i in range(1, n + 1):

            # Variando o j de acordo com o limite determinado pela janela w
            limite_inferior = max(1, i - w)
            limite_superior = min(m, i + w) + 1
            for j in range(limite_inferior, limite_superior):
                # Calculando o custo local
                custo_local = abs(s[i - 1] - t[j - 1])

                # Obtendo o menor vizinho
                menor_vizinho = min(matriz_dtw[i-1, j], # Deleção ou Inserção (a depender de onde está a série S: nas linhas ou nas colunas)
                                    matriz_dtw[i, j-1], # Inserção ou Deleção (a depender de onde está a série S: nas linhas ou nas colunas)
                                    matriz_dtw[i-1, j-1]) # Match

                # Definindo o valor da posição atual
                matriz_dtw[i, j] = custo_local + menor_vizinho

        return matriz_dtw

    def dtw_warping_path(self, serie1: SerieTemporal, serie2: SerieTemporal) -> list:
        """
        Obtém o warping path (caminho de alinhamento ótimo) entre as duas séries temporais.
        :param serie1: Primeira série temporal.
        :param serie2: Segunda série temporal.
        :return: Warping path (caminho de alinhamento ótimo).
        """
        s = serie1.dados
        t = serie2.dados
        n = len(s)
        m = len(t)

        # Gerando matriz DTW
        matrix_dtw = self.gerar_matriz_dtw(serie1, serie2)

        i = n
        j = m
        caminho = []

        # Caminhando do fim para o início
        while i > 0 and j > 0:
            caminho.append((i - 1, j - 1))

            # Encontrando o menor vizinho
            opcao_diagonal = matrix_dtw[i - 1, j - 1]
            opcao_cima = matrix_dtw[i - 1, j]
            opcao_esquerda = matrix_dtw[i, j - 1]

            menor_custo = min(opcao_esquerda, opcao_cima, opcao_diagonal)

            if menor_custo == opcao_diagonal:
                i -= 1
                j -= 1
            elif menor_custo == opcao_cima:
                i -= 1
            elif menor_custo == opcao_esquerda:
                j -= 1

            # Adicionando a borda restante se um dos eixos zerar antes do outro
            while i > 0:
                caminho.append((i - 1), 0)
                i -= 1
            while j > 0:
                caminho.append((0, j - 1))
                j -= 1

        # Retornando o caminho invertido
        return caminho[::-1]


