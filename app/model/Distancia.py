import math
from enum import Enum


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
