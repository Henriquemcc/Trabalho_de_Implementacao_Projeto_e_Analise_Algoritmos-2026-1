class OneNearestNeighbour:
    def __init__(self, algoritmo_distancia):
        self.algoritmo = algoritmo_distancia

    def fit(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    def predict(self, serie):
        melhor_distancia = float('inf')
        melhor_classe = None

        for xi_train, yi_train in zip(self.x_train, self.y_train):
            distancia = self.algoritmo.obter_distancia(serie, xi_train)

            if distancia < melhor_distancia:
                melhor_distancia = distancia
                melhor_classe = yi_train

        return melhor_classe