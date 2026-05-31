import os

import pandas as pd


class SerieTemporal:
    """
    Estrutura de dados para armazenamento de uma série temporal.
    """

    def __init__(self, dados, nome: str):
        """
        Constrói uma nova instância da SerieTemporal.
        :param dados: Dados da série temporal.
        :param nome: Nome da série temporal.
        """
        self.dados = dados
        self.nome = nome

    @staticmethod
    def abrir_arquivo_txt(caminho) -> SerieTemporal:
        """
        Realiza a abertura de um arquivo de uma série temporal em txt.
        :param caminho: Caminho do arquivo da série temporal em txt.
        :return: SerieTemporal obtida a partir do arquivo.
        """
        dados = []
        nome = os.path.basename(caminho)
        with open(caminho, "r") as arquivo:
            for linha in arquivo:
                dados.append(float(linha.strip()))
        return SerieTemporal(dados, nome)

    @staticmethod
    def abrir_arquivo_tsv(caminho, indice) -> SerieTemporal:
        """
        Realiza a abertura de um arquivo de uma série temporal em tsv.
        :param caminho: Caminho do arquivo da série temporal em tsv.
        :param indice: Índice da série temporal.
        :return: SerieTemporal obtida a partir do arquivo.
        """
        df = pd.read_csv(caminho, sep='\t').iloc[indice, 1:].values
        nome = "{}:{}".format(os.path.basename(caminho), indice)
        return SerieTemporal(df, nome)
