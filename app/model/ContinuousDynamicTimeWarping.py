import numbers

import numpy
from enum import Enum

from model.SerieTemporal import SerieTemporal
from model.Distancia import Distancia, distancia_manhattan, distancia_euclidiana, distancia_euclidiana_ao_quadrado

class TipoNoCdtw(Enum):
    """
    Representa o tipo de um Nó do algoritmo CDTW
    """
    NATIVO = 'Nativo'
    STEINER = 'Steiner'

class NoCdtw:
    """
    Representa um ponto no espaço euclidiano para o algoritmo CDTW.
    Fonte: https://github.com/gregwood-db/cdtw/blob/master/cdtw_classes.py
    """
    def __init__(self, x, y, tipo: TipoNoCdtw = TipoNoCdtw.NATIVO):

        # A distância inicial deve ser 0
        self.distancia = 0

        # Tipo de nó
        self.tipo = tipo

        # Convertendo os valores de x e y para float
        try:
            self.x = float(x)
            self.y = float(y)
        except ValueError as e:
            raise ValueError('Coordenadas precisam ser números')

        # Estado se o nó foi visitado
        self.visitado = False

        # ID único do nó
        self.id = id(self)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return 'Nó com id {}'.format(self.id)

    def __add__(self, other):
        return NoCdtw(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return NoCdtw(self.x - other.x, self.y - other.y)

    def mostrar(self):
        print('Nó CDTW com as seguintes propriedades:')
        print('Localização: ({};{})'.format(self.x, self.y))
        print('Distância: {}'.format(self.distancia))
        print('Tipo de nó: {}'.format(self.tipo.name))

    def calcular_distancia(self, other: NoCdtw) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** (1/2)


class CurvaCdtw:
    """
    Representa uma curva 2D de N de largura composta de Nós CDTW.
    Fonte: https://github.com/gregwood-db/cdtw/blob/master/cdtw_classes.py
    """
    def __init__(self, lista_x: list | None = None, lista_y: list | None = None, no: NoCdtw | None = None, array_no: list | None = None):

        # Criando lista de nós
        self.lista_nos = []

        # Verificando se o tamanho de lista_x e lista_y são iguais
        if lista_x is not None and lista_y is not None:
            if len(lista_x) != len(lista_y):
                raise ValueError('O tamanho de lista_x e lista_y precisam ser iguais')

        # Para cada nó de x e y, adicionando na curva
        if lista_x is not None and lista_y is not None:
            for x, y in zip(lista_x, lista_y):
                self.adicionar_no(x=x, y=y)

        # Adicionando nó á curva
        if no is not None and isinstance(no, NoCdtw):
            self.adicionar_no(no=no)

        # Adicionando nós do array de nós
        if array_no is not None:
            for no in array_no:
                self.adicionar_no(novo_no=no)

    def __getitem__(self, item: int) -> NoCdtw:
        return self.lista_nos[item]

    def __len__(self) -> int:
        return int(len(self.list_nos))

    def __repr__(self) -> str:
        return 'Curva com {} pontos. Use o método show() para listar os pontos.'.format(len(self))

    def __add__(self, other) -> CurvaCdtw:
        if not isinstance(other, CurvaCdtw):
            raise ValueError('Tentou adicionar um não Nó á lista de nós.')
        return CurvaCdtw(self.lista_nos + other.lista_nos)

    def trim(self, inicio: int, fim: int) -> CurvaCdtw:
        if inicio < 0 or inicio > len(self) or inicio > fim or fim > len(self):
            raise ValueError('Índice fora dos limites para a CurvaCdtw')
        return CurvaCdtw(self.lista_nos[inicio:fim])

    def adicionar_no(self, novo_no: NoCdtw):
        if not isinstance(novo_no, NoCdtw):
            raise ValueError('Tentou adicionar um não Nó á lista de nós.')
        self.lista_nos.append()

    def mostrar(self):
        print('Curva com {} pontos. Os pontos são: {}'.format(len(self), self.lista_nos))

    def dividir_ao_meio(self) -> CurvaCdtw:
        return CurvaCdtw([(self[i].x + self[i + 1].x) / 2 for i in range(0, len(self) - len(self) % 2, 2)], [(self[i].y + self[i + 1].y) / 2 for i in range(0, len(self) % 2, 2)])

    @staticmethod
    def from_serie_temporal(serie: SerieTemporal) -> CurvaCdtw:

        # Convertendo os dados da SerieTemporal para um array numpy
        y = numpy.asarray(serie.dados).flatten()
        x = numpy.arange(len(y))

        # Criando nova instância de CurvaCdtw
        curva = CurvaCdtw()

        # Adicionando cada elemento á CurvaCdtw
        for xi, yi in zip(x, y):
            curva.adicionar_no(NoCdtw(x=xi, y=yi))

        # Retornando CurvaCdtw
        return curva

    @staticmethod
    def from_array(dados: list) -> CurvaCdtw:

        # Convertendo os dados para um array numpy
        y = numpy.asarray(dados).flatten()
        x = numpy.arange(len(y))

        # Criando nova instância de CurvaCdtw
        curva = CurvaCdtw()

        # Adicionando cada elemento á CurvaCdtw
        for xi, yi in zip(x, y):
            curva.adicionar_no(NoCdtw(x=xi, y=yi))

        # Retornando CurvaCdtw
        return curva

    @staticmethod
    def simplificar_curva(curva: CurvaCdtw, epsilon: float | int) -> CurvaCdtw:
        """
        Simplifica uma CurvaCdtw usando o algoritmo Douglas-Peuker.
        :param epsilon: Limiar de tolerância geométrica para simplificação.
        :param curva: Curva a ser simplificada.
        :return: Curva simplificada
        Fonte: https://github.com/gregwood-db/cdtw/blob/master/cdtw.py
        """

        # Verificando se o epsilon é menor que zero
        if epsilon < 0:
            raise ValueError('O valor de epsilon não pode ser menor de que zero')

        distancia_maxima = 0
        indice = 0
        for i in range(1, len(curva)):
            distancia = CurvaCdtw.distancia_linha(curva[i], curva[0], curva[-1])
            if distancia > distancia_maxima:
                indice = i
                distancia_maxima = distancia

        if distancia_maxima > epsilon:
            recursao1 = CurvaCdtw.simplificar_curva(CurvaCdtw(no=curva[:indice + 1]), epsilon)
            recursao2 = CurvaCdtw.simplificar_curva(CurvaCdtw(no=curva[indice:]), epsilon)
            return CurvaCdtw(no=recursao1[:-1]) + recursao2
        else:
            return CurvaCdtw(array_no=[curva[0], curva[-1]])

class MetodoStainer(Enum):
    UNIFORME='Uniforme'
    PONDERADO='PONDERADO'

class BlocoCdtw:
    """
    Representa uma únidade geométrica onde ocorrem os cálculos locais do algoritmo CDTW.
    Fonte: https://github.com/gregwood-db/cdtw/blob/master/cdtw_classes.py
    """
    def __init__(self, lista_nos: list[NoCdtw]):
        self.lista_nos = lista_nos
        self.topo_esquerdo = self.lista_nos[0]
        self.topo_direito = self.lista_nos[1]
        self.canto_inferior_esquerdo = self.lista_nos[2]
        self.canto_inferior_direito = self.lista_nos[3]
        self.esquerda = [self.topo_esquerdo, self.canto_inferior_esquerdo]
        self.topo = [self.topo_esquerdo, self.topo_direito]
        self.direita = [self.topo_direito, self.canto_inferior_direito]
        self.canto_inferior = [self.canto_inferior_esquerdo, self.canto_inferior_direito]

    def __getitem__(self, item: int) -> NoCdtw:
        if not isinstance(item, int):
            raise ValueError('O item precisa ser inteiro')
        return self.lista_nos[item]

    def __setitem__(self, chave: int, valor: NoCdtw):
        if not isinstance(chave, int):
            raise ValueError('A chave precisa ser inteiro')
        if not isinstance(valor, NoCdtw):
            raise ValueError('O valor precisa ser uma instância de NoCdtw')
        self.lista_nos[chave] = valor

    def __repr__(self):
        return 'Bloco com id {}'.format(sum([no.id for no in self.lista_nos]))

    def adicionar_no(self, no: NoCdtw):
        if not isinstance(no, NoCdtw):
            raise ValueError('O no precisa ser uma instância de NoCdtw')
        self.lista_nos.append(no)

    def __resetar_nos(self):
        self.topo_esquerdo = self.topo[0]
        self.topo_direito = self.topo[-1]
        self.canto_inferior_esquerdo = self.canto_inferior[0]
        self.canto_inferior_direito = self.canto_inferior[-1]
        self.esquerda = [self.topo_esquerdo, self.canto_inferior_esquerdo]
        self.topo = [self.topo_esquerdo, self.topo_direito]
        self.direita = [self.topo_direito, self.canto_inferior_direito]
        self.canto_inferior = [self.canto_inferior_esquerdo, self.canto_inferior_direito]
        self.lista_nos = [self.topo_esquerdo, self.topo_direito, self.canto_inferior_esquerdo, self.canto_inferior_direito]

    def atualizar_nos(self):
        self.esquerda[0] = self.topo_esquerdo
        self.esquerda[-1] = self.canto_inferior_esquerdo
        self.direita[0] = self.topo_direito
        self.direita[-1] = self.canto_inferior_direito
        self.topo[0] = self.topo_esquerdo
        self.topo[-1] = self.topo_direito
        self.canto_inferior[0] = self.canto_inferior_esquerdo
        self.canto_inferior[-1] = self.canto_inferior_direito
        self.lista_nos = ([self.topo_esquerdo] + self.topo[1:-1] +
                          [self.topo_direito] + self.direita[1:-1] +
                          [self.canto_inferior_esquerdo] + self.canto_inferior[1:-1] +
                          [self.canto_inferior_direito] + self.esquerda[1:-1])

    def definir_distancia(self):
        for j in self.esquerda + self.topo:
            if j.visitado:
                continue

            # A distância do nó é o mínimo entre a direita/canto inferior
            distancias = [j.calcular_distancia(no) + no.distancia for no in self.direita + self.canto_inferior]
            j.distancia = min(distancias)
            j.visitado = True

    def inicializar_distancias(self):
        for no in self.canto_inferior + self.direita:
            if no.visitado:
                continue
            else:
                no.distancia = no.calcular_distancia(self.canto_inferior_direito) + self.canto_inferior_direito.distancia
                no.visitado = True

    def adicionar_steiner(self, metodo: MetodoStainer, numero: int):
        # Verificando se numero é inteiro
        if not isinstance(numero, int):
            raise ValueError('O parâmetro numero precisa ser inteiro')

        # Verificando se o metodo é uma instância de MetodoStainer
        if not isinstance(metodo, MetodoStainer):
            raise ValueError('O parâmetro metodo precisa ser uma instância do enum MetodoStainer')

        # Define o tamanho fixo padrão que um segmento de aresta deve ter ao usar o método ponderado de inserção de nós
        # de stainer
        unidade_peso = 0.25

        # Atualizando a lista de nós para eliminar stainers existentes
        self.__resetar_nos()

        # Iterando para cada borda para adicionar pontos
        bordas = [self.topo, self.direita, self.canto_inferior, self.esquerda]
        for indice, borda in enumerate(bordas):
            if metodo == MetodoStainer.PONDERADO:
                comprimento = borda[1].calcular_distancia(borda[0])
                numero = numpy.ceil(comprimento / unidade_peso)

            dx = (borda[1].x - borda[0].x) / (numero + 1)
            dy = (borda[1].y - borda[0].y) / (numero + 1)
            novo_x = numpy.linspace(borda[0].x + dx, borda[1].x - dx, numero)
            novo_y = numpy.linspace(borda[0].y + dy, borda[1].y - dy, numero)
            novos_nos = [NoCdtw(x, y, tipo=TipoNoCdtw.STEINER) for x, y in zip(novo_x, novo_y)]

            if indice == 0:
                self.topo = [bordas[indice][0]] + novos_nos + [bordas[indice][-1]]
            elif indice == 1:
                self.direita = [bordas[indice][0]] + novos_nos + [bordas[indice][-1]]
            elif indice == 2:
                self.canto_inferior = [bordas[indice][0]] + novos_nos + [bordas[indice][-1]]
            else:
                self.esquerda = [bordas[indice][0]] + novos_nos + [bordas[indice][-1]]

        self.atualizar_nos()

class ContinuousDynamicTimeWarping:
    """
    Implementação do algoritmo Continuous Dynamic Time Warping.
    """
    def __init__(self, janela_de_busca: int | None = None, distancia: Distancia = Distancia.EUCLIDIANA):

        """
        Inicializa o algoritmo Continuous Dynamic Time Warping.
        :param janela_de_busca: Tamanho da janela de busca.
        :param distancia: Tipo de distância a ser utilizado.
        """
        self.janela_de_busca = janela_de_busca
        self.distancia = None
        if distancia == Distancia.MANHATTAN:
            self.distancia = distancia_manhattan
        elif distancia == Distancia.EUCLIDIANA:
            self.distancia = distancia_euclidiana
        elif distancia == Distancia.EUCLIDIANA_AO_QUADRADO:
            self.distancia = distancia_euclidiana_ao_quadrado
        else:
            ValueError(f"Tipo de distância inválido: {distancia}")

    def cdtw_distance(self, serie1: SerieTemporal | list | numpy.ndarray, serie2: SerieTemporal | list | numpy.ndarray, interpolacao= 0.3, num_stainer = 5, r = 100) -> float:
        """
        Realiza o cálculo da distância de duas séries temporais através do algoritmo Continuous Dynamic Time Warping.
        :param serie1: Primeira série temporal
        :param serie2: Segunda série temporal
        :param interpolacao: Limiar de tolerância geométrica para simplificação.
        :param num_stainer: Número de Steiner, quantidade de pontos extras de interpolação adicionados artificialmente ao
        longo das arestas de cada bloco estrutural da malha de alinhamento.
        :param r: Raio da Janela de Sakoe-Chiba.
        :return: Número real contendo a distância entre as duas séries temporais.
        """

        # Verificando se o parâmetro interpolacao é numérico
        if not isinstance(interpolacao, numbers.Number):
            raise ValueError('O parâmetro interpolacao precisa ser numérico')

        # Verificando se o parâmetro interpolacao é maior ou igual a zero
        if interpolacao < 0:
            raise ValueError('O parâmetro interpolacao precisa ser maior ou igual a zero')

        # Verificando se o parâmetro num_stainer é inteiro
        if not isinstance(num_stainer, int):
            raise ValueError('O parâmetro num_stainer precisa ser inteiro')

        # Verificando se o raio é inteiro
        if not isinstance(r, int):
            raise ValueError('O parâmetro r precisa ser inteiro')

        # Retirando o array dados do objeto SerieTemporal da serie1
        if type(serie1).__name__ == 'SerieTemporal':
            c1 = CurvaCdtw.from_serie_temporal(serie1)
        elif isinstance(serie1, list):
            c1 = CurvaCdtw.from_array(serie1)

        # Retirando o array dados do objeto SerieTemporal da serie2
        if type(serie2).__name__ == 'SerieTemporal':
            c2 = CurvaCdtw.from_serie_temporal(serie2)
        elif isinstance(serie2, list):
            c2 = CurvaCdtw.from_array(serie2)

        # Se o parâmetro interpolação for maior do que 0, realizando simplificação das curvas
        if interpolacao > 0:
            c1 = CurvaCdtw.simplificar_curva(c1, interpolacao)
            c2 = CurvaCdtw.simplificar_curva(c2, interpolacao)

        # Obtendo os tamanhos das curvas
        h = len(c1)
        w = len(c2)

        # Construindo a Janela de Sakoe-Chiba
        if r == 0:
            janela_sakoe_chiba = numpy.zeros((2, w))
            janela_sakoe_chiba[0, :] = h
        else:
            janela_sakoe_chiba = numpy.zeros((2, w))
            escala = h / w
            for i in range(0, w):
                h_preencher_centro = int(numpy.ceil(i * escala))
                h_preencher_cima = min(h, h_preencher_centro + r)
                h_preencher_baixo = max(0, h_preencher_centro - r)
                janela_sakoe_chiba[0, i] = h_preencher_cima
                janela_sakoe_chiba[1, i] = h_preencher_baixo

        distancia, _ = self._cdtw(c1, c2, mascara=janela_sakoe_chiba, num_stainer=num_stainer)

        return distancia

    @staticmethod
    def __construir_bloco(curva1: CurvaCdtw, curva2: CurvaCdtw, indice_c1: int, indice_c2: int):
        return BlocoCdtw([curva2(indice_c2 + 1) - curva1(indice_c1 + 1),
                          curva2(indice_c2 + 1) - curva1(indice_c1),
                          curva2(indice_c2) - curva1(indice_c1 + 1),
                          curva2(indice_c2) - curva1(indice_c1)])

    def _cdtw(self, curva1: CurvaCdtw, curva2: CurvaCdtw, mascara: numpy.ndarray, num_stainer: int) -> tuple[float, dict]:
        """
        Realiza o cálculo da distância de duas curvas através do algoritmo Continuous Dynamic Time Warping.
        :param curva1: Primeira curva.
        :param curva2: Segunda curva.
        :param mascara: Uma matriz 2*n que contém os limites superior e inferior para a região de distorção válida.
        :param num_stainer: Número de Steiner, quantidade de pontos extras de interpolação adicionados artificialmente ao
        longo das arestas de cada bloco estrutural da malha de alinhamento.
        :return: Um número real contendo a distância entre as duas curvas e um dicionário contendo a warping distance para cada nó.
        """
        # Verificando se os valores de c1 e c2 são instâncias de CurvaCdtw
        if (not isinstance(curva1, CurvaCdtw)) or (not isinstance(curva2, CurvaCdtw)):
            raise ValueError('Os parâmetros c1 e c2 precisam ser instâncias de CurvaCdtw')

        # Inicializando as variáveis de loop
        w = len(curva1) - 1
        h = len(curva2) - 1

        # Matriz que armazena os valores da programação dinâmica
        matriz_de_baixo = numpy.zeros((w, num_stainer + 2))

        # Bloco ou célula da malha geométrica que o algoritmo está a processar e a calcular no exato momento da iteração
        # dentro do duplo loop
        bloco_atual = []

        # Guarda o bloco completo calculado imediatamente á direita do bloco atual
        bloco_direita = []

        # Guarda todas as distâncias acumuladas calculadas para os nós principais da malha geométrica
        mapa_distancias = {}

        # Interando do canto inferior direito para o canto superior esquerdo da matriz
        for i in range(h - 1, -1, -1):
            for j in range(w - 1, -1, -1):

                # Caso esteja fora da máscara, podemos pular este elemento
                mascara_superior = mascara[0, j]
                mascara_inferior = mascara[1, j]
                if i < mascara_inferior or i > mascara_superior:
                    matriz_de_baixo[j][0:num_stainer + 2] = numpy.inf
                    continue

                # Constuindo blocos com stainers
                bloco_atual = self.__construir_bloco(curva1, curva2, j, i)
                bloco_atual.adicionar_steiner(MetodoStainer.UNIFORME, num_stainer)

