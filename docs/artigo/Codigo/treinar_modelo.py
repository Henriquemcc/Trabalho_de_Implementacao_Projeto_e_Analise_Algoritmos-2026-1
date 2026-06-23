def treinar_modelo(planilha: pandas.DataFrame) -> tuple[dict[Any, Any], dict[Any, Any]]:
    """
    Treina modelos e obtem as metricas
    :param planilha: DataFrame contendo as series temporais
    :return: Dicionario contendo as metricas de cada algoritmo
    """

    # Dicionários com as métricas e modelos dos algoritmos
    metricas = {}
    modelos = {}

    lista_nomes_datasets = planilha.iloc[:]['Name']

    with ThreadPoolExecutor() as executor:
        resultados = list(
            executor.map(processar_dataset, lista_nomes_datasets)
        )

        for modelos_i, metricas_i in resultados:
            modelos.update(modelos_i)
            metricas.update(metricas_i)

    return modelos, metricas