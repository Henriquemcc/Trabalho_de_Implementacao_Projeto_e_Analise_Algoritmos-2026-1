from jedi.plugins.django import mapping

from model.SerieTemporal import SerieTemporal
import math
from enum import Enum
import numpy

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
    def __init__(self, janela_de_busca: int | None = None, distancia: Distancia = Distancia.EUCLIDIANA):
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

    def dtw_distance(self, serie1: SerieTemporal | list | numpy.ndarray, serie2: SerieTemporal | list | numpy.ndarray) -> float:
        """
        Realiza o cálculo da distância de duas séries temporais através do algoritmo Dynamic Time Warping.
        :param serie1: Primeira série temporal.
        :param serie2: Segunda série temporal.
        Fonte: https://en.wikipedia.org/wiki/Dynamic_time_warping#Implementation
        """
        if hasattr(serie1, 'dados'):
            s = serie1.dados
        else:
            s = serie1

        if hasattr(serie2, 'dados'):
            t = serie2.dados
        else:
            t = serie2

        n = len(s)
        m = len(t)

        # Gerando matriz DTW
        matrix_dtw = self.gerar_matriz_dtw(serie1, serie2)

        # Retornando o elemento das últimas posições dos eixos x e y
        return matrix_dtw[n, m]

    def gerar_matriz_dtw(self, serie1: SerieTemporal | list | numpy.ndarray, serie2: SerieTemporal | list | numpy.ndarray) -> numpy.ndarray:
        """
        Cria uma matriz DTW a partir de duas séries temporais
        :param serie1: Primeira série temporal.
        :param serie2: Segunda série temporal.
        :param janela_de_busca: Tamanho da janela.
        :return: Matriz DTW.
        Fonte: https://en.wikipedia.org/wiki/Dynamic_time_warping#Implementation
        """
        if hasattr(serie1, 'dados'):
            s = serie1.dados
        else:
            s = serie1

        if hasattr(serie2, 'dados'):
            t = serie2.dados
        else:
            t = serie2

        n = len(s)
        m = len(t)

        # Inicializando a matriz dtw com as dimensões (n+1) por (m+1)
        matriz_dtw = numpy.full((n+1, m+1), numpy.inf)

        # Definindo a condição de contorno inicial
        matriz_dtw[0, 0] = 0

        # Adaptando a janela de busca
        if self.janela_de_busca is None:
            janela_de_busca = max(n, m)
        else:
            janela_de_busca = max(self.janela_de_busca, abs(n - m))

        # Preenchendo a matriz respeitando a janela de restrição
        for i in range(1, n + 1):

            # Variando o j de acordo com o limite determinado pela janela janela_de_busca
            j_inicio = max(1, i - janela_de_busca)
            j_fim = min(m, i + janela_de_busca) + 1
            for j in range(j_inicio, j_fim):
                # Calculando o custo local
                custo_local = self.distancia(s[i - 1], t[j - 1])

                # Obtendo o menor vizinho
                menor_vizinho = min(matriz_dtw[i-1, j], # Deleção ou Inserção (a depender de onde está a série S: nas linhas ou nas colunas)
                                    matriz_dtw[i, j-1], # Inserção ou Deleção (a depender de onde está a série S: nas linhas ou nas colunas)
                                    matriz_dtw[i-1, j-1]) # Match

                # Definindo o valor da posição atual
                matriz_dtw[i, j] = custo_local + menor_vizinho

        return matriz_dtw

    def dtw_warping_paths(self, serie1: SerieTemporal | list | numpy.ndarray, serie2: SerieTemporal | list | numpy.ndarray) -> tuple[int, numpy.ndarray]:
        """
        Obtém o warping path (caminhos de alinhamento ótimo) entre as duas séries temporais.
        :param serie1: Primeira série temporal.
        :param serie2: Segunda série temporal.
        :return: Warping path (caminhos de alinhamento ótimo), a distância final, estruturas de alinhamento e matrix dtw.
        Fonte: https://github.com/wannesm/dtaidistance/blob/master/src/dtaidistance/dtw.py
        """
        if hasattr(serie1, 'dados'):
            s = serie1.dados
        else:
            s = serie1

        if hasattr(serie2, 'dados'):
            t = serie2.dados
        else:
            t = serie2

        n = len(s)
        m = len(t)

        # Ajustando janela de busca
        if self.janela_de_busca is None:
            janela_busca = max(n, m)
        else:
            janela_busca = max(self.janela_de_busca, abs(n - m))

        # Inicializando matriz dtw
        matriz_dtw = numpy.full((n + 1, m + 1), numpy.inf)

        # Definindo condição de contorno inicial
        matriz_dtw[0, 0] = 0

        # Preenchendo a matriz por Programação dinâmica
        for i in range(1, n + 1):
            # Definindo os limites inferior e superior
            j_inicio = max(0, i - janela_busca)
            j_fim = min(m, i + janela_busca) + 1

            for j in range(j_inicio, j_fim):
                # Calculando o custo local
                custo_local = self.distancia(s[i - 1], t[j - 1])

                # Obtendo o menor vizinho
                menor_vizinho = min(matriz_dtw[i-1, j], # Deleção ou Inserção (a depender de onde está a série S: nas linhas ou nas colunas)
                                    matriz_dtw[i, j-1], # Inserção ou Deleção (a depender de onde está a série S: nas linhas ou nas colunas)
                                    matriz_dtw[i-1, j-1]) # Match

                # Definindo o valor da posição atual
                matriz_dtw[i, j] = custo_local + menor_vizinho

        # Distância final
        distancia = matriz_dtw[n, m]

        # Retornando a distância e a matriz dtw
        return distancia, matriz_dtw

    def dtw_warping_path(self, serie1: SerieTemporal | list | numpy.ndarray, serie2: SerieTemporal | list | numpy.ndarray) -> list:
        """
        Obtém o warping path (caminho de alinhamento ótimo) entre duas séries temporais.
        :param serie1: Primeira série temporal.
        :param serie2: Segunda série temporal.
        :return: Warping path (caminho de alinhamento ótimo) entre as duas séries temporais.
        Fonte: https://github.com/wannesm/dtaidistance/blob/master/src/dtaidistance/dtw.py
        """

        # Obtendo os caminhos
        _, caminhos = self.dtw_warping_paths(serie1, serie2)

        # Obtendo os melhores caminhos
        caminhos = self.obter_melhor_caminho(caminhos)
        
        # Retornando caminhos
        return caminhos
    
    def obter_melhor_caminho(self, caminhos):
        """
        Obtém o caminho ótimo a partir de uma matrix dtw.
        :param caminhos: Matriz DTW.
        :return Array representando o melhor caminho.
        """
        # Definindo o ponto de partida: canto inferior direito
        i = int(caminhos.shape[0] - 1)
        j = int(caminhos.shape[1] - 1)

        # Inicializando a lista que guardará as coordenadas do caminho
        caminho_otimo = []

        # Adicionando o ponto final á lista
        caminho_otimo.append((i - 1, j - 1))

        # Caminhando do fim para o começo
        while i > 0 and j > 0:
            vizinhos = [
                caminhos[i - 1, j - 1], # Diagonal -> Match
                caminhos[i - 1, j], # Cima -> Deleção
                caminhos[i, j - 1] # Esquerda -> Inserção
            ]

            # Selecionando o índice de direção que possui o menor custo acumulado
            opcao_escolhida = numpy.argmin(vizinhos)

            # Movimentando os ponteiros na matriz de acordo com a direção escolhida
            if opcao_escolhida == 0:
                i = i - 1
                j = j - 1
            elif opcao_escolhida == 1:
                i = i - 1
            else:
                j = j - 1

            
            # Adicionando a coordenada atual á lista do caminho ótimo
            caminho_otimo.append((i - 1, j - 1))

        # Removendo o último elemento residual para evitar o estouro de borda (-1, -1)
        caminho_otimo.pop()

        # Invertendo a ordem da lista
        caminho_otimo.reverse()

        # Retornando o caminho ótimo
        return caminho_otimo

