def processar_dataset(nome_dataset: str):
    """
    Realiza o processamento de um dataset em um processo
    :param nome_dataset: Nome do dataset.
    :return:
    """
    # Obtendo os caminhos do dataset de treino e teste
    print('Obtendo os caminhos do dataset de treino e teste')
    diretorio_dataset = os.path.join('../Dataset/UCRArchive_2018', nome_dataset)
    caminho_arquivo_treino = os.path.join(diretorio_dataset, '{}_TRAIN.tsv'.format(nome_dataset))
    caminho_arquivo_teste = os.path.join(diretorio_dataset, '{}_TEST.tsv'.format(nome_dataset))

    # Abrindo datasets
    print('Abrindo datasets')
    dataset_treino = pandas.read_csv(caminho_arquivo_treino, sep='\t', header=None)
    dataset_teste = pandas.read_csv(caminho_arquivo_teste, sep='\t', header=None)

    # Formatando datasets
    print('Formatando datasets')
    dataset_treino = formatar_dataset(dataset_treino)
    dataset_teste = formatar_dataset(dataset_teste)

    # Criando conjunto de treino e teste
    print('Criando conjunto de treino e teste')
    x_train, y_train = separar_x_y(dataset_treino)
    x_test, y_test = separar_x_y(dataset_teste)

    # Instanciando algoritmos
    print('Instanciando algoritmos')
    modelos_i = {}
    modelos_i[('dtw', nome_dataset)] = onn_dtw = OneNearestNeighbour(DynamicTimeWarping())
    modelos_i[('ddtw', nome_dataset)] = onn_ddtw = OneNearestNeighbour(DerivativeDynamicTimeWarping())
    modelos_i[('lcs', nome_dataset)] = onn_lcs = OneNearestNeighbour(LongestCommonSubsequence())
    modelos_i[('soft-dtw', nome_dataset)] = onn_soft_dtw = OneNearestNeighbour(SoftDynamicTimeWarping())

    # Treinando algoritmos
    print('Treinando algoritmos')
    onn_dtw.fit(x_train, y_train)
    onn_ddtw.fit(x_train, y_train)
    onn_lcs.fit(x_train, y_train)
    onn_soft_dtw.fit(x_train, y_train)

    # Testando algoritmos
    print('Testando algoritmos')
    try:
        y_dtw = [onn_dtw.predict(xi_test) for xi_test in x_test]
    except Exception as e:
        print(e)
    try:
        y_ddtw = [onn_ddtw.predict(xi_test) for xi_test in x_test]
    except Exception as e:
        print(e)
    try:
        y_lcs = [onn_lcs.predict(xi_test) for xi_test in x_test]
    except Exception as e:
        print(e)
    try:
        y_soft_dtw = [onn_soft_dtw.predict(xi_test) for xi_test in x_test]
    except Exception as e:
        print(e)

    # Obtendo acuracia
    print('Obtendo acuracia')
    acuracia_dtw = accuracy_score(y_test, y_dtw)
    acuracia_ddtw = accuracy_score(y_test, y_ddtw)
    acuracia_lcs = accuracy_score(y_test, y_lcs)
    acuracia_soft_dtw = accuracy_score(y_test, y_soft_dtw)
    print('Acuracia DTW: {}'.format(acuracia_dtw))
    print('Acuracia DDTW: {}'.format(acuracia_ddtw))
    print('Acuracia LCS: {}'.format(acuracia_lcs))
    print('Acuracia Soft DTW: {}'.format(acuracia_soft_dtw))

    # Salvando as metricas no dicionario
    print('Salvando as metricas no dicionario')
    metricas_i = {}
    metricas_i[(nome_dataset, 'dtw')] = acuracia_dtw
    metricas_i[(nome_dataset, 'ddtw')] = acuracia_ddtw
    metricas_i[(nome_dataset, 'lcs')] = acuracia_lcs
    metricas_i[(nome_dataset, 'soft-dtw')] = acuracia_soft_dtw

    return modelos_i, metricas_i