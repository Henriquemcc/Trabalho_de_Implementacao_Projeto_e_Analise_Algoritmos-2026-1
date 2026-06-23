def formatar_dataset(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Realiza a formatacao do dataset.
    :param df: Dataset a ser formatado.
    :return: Dataset formatado.
    """
    classe = df.iloc[:, 0]
    series = df.iloc[:, 1:]

    df_novo = pandas.DataFrame({
        'classe': classe,
        'SerieTemporal': list(series.to_numpy())
    })

    return df_novo