from model.SerieTemporal import SerieTemporal


class MatrizMapeamento:
    """
    Estrutura de dados para armazenamento de uma matriz de mapeamento.
    """

    def __init__(self, serie_1: SerieTemporal, serie_2: SerieTemporal):
        """
        Constrói uma nova instância da MatrizMapeamento.
        :param serie_1: Primeira série temporal (eixo x).
        :param serie_2: Segunda série temporal (eixo y).
        """
        self.serie_1 = serie_1
        self.serie_2 = serie_2
