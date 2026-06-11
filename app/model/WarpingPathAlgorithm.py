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