from abc import ABC, abstractmethod

import numpy


class WarpingPathAlgorithm(ABC):
    """
    Classe abstrata utilizada para padronizar os métodos comuns entre os algoritmos que implementam warping paths.
    """
    @abstractmethod
    def warping_paths(self, serie1, serie2) -> tuple[int, numpy.ndarray]:
        """
        Obtém o warping path (caminhos de alinhamento ótimo) entre as duas séries temporais.
        :param serie1: Primeira série temporal.
        :param serie2: Segunda série temporal.
        :return: Tupla contendo a distância DTW e a matriz DTW.
        """
        pass


    def warping_path(self, serie1, serie2) -> list:
        """
        Obtém o warping path (caminho de alinhamento ótimo) entre duas séries temporais.
        :param serie1: Primeira série.
        :param serie2: Segunda série.
        :return: Warping path (caminho de alinhamento ótimo) entre duas séries temporais.
        Fonte: https://github.com/wannesm/dtaidistance/blob/master/src/dtaidistance/dtw.py
        """
        # Obtendo os caminhos
        _, caminhos = self.warping_paths(serie1, serie2)

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