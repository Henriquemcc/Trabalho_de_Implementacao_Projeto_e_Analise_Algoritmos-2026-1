def separar_x_y(dataset: pandas.DataFrame) -> tuple[list, list]:
    """
    Separa o conjunto de treino do conjunto de teste
    :param dataset: Dataset de entrada.
    :return: Tupla com os cunjuntos de treino e teste.
    """
    x = dataset['SerieTemporal'].tolist()
    y = dataset['classe'].tolist()

    return x, y