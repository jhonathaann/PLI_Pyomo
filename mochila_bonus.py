import pyomo.environ as pyEnv

caminho = r"C:\Users\jhona\anaconda3\Library\bin\glpsol.exe"

def mochila_bonus(nome_arquivo):

    # lendo as instancias do arquivo
    with open(nome_arquivo, 'r') as file:

        # lendo o nome da intancia
        referencia = file.readline().strip()

        # lendo a quantidade de variaveis
        n = int(file.readline().strip())

        # lendo os valores do n itens
        valores_itens = list(map(int, file.readline().strip().split()))

         # inicializando a matriz de bonus com 0
        bonus_ij = [[0] * n for _ in range(n)]

        # lendo os coeficientes quadraticos
        for i in range(n - 1):
            linha = list(map(int, file.readline().strip().split()))
            for j, valor in enumerate(linha):
                bonus_ij[i][i + j + 1] = valor
                #bonus_ij[i + j + 1][i] = valor  # completa a simetria

        # le a linha em branco
        file.readline()

        # le o tipo de restricao
        tipo_restricao = int(file.readline().strip())

        # lendo a capacidade da mochila
        capacidade = int(file.readline().strip())

        # lendo os pesos dos itens
        pesos_itens = list(map(int, file.readline().strip().split()))


    # =================== REALIZANDO A MODELAGEM ======================== #

    # criando o modelo
    modelo = pyEnv.ConcreteModel()

    # definindo o conjunto de itens
    modelo.I = range(n)

    # definindo as variaveis de decisao
    modelo.x = pyEnv.Var(modelo.I, within=pyEnv.Binary)

    # funcao objetivo: maximizar a soma dos valores lieres + valores quadraticos
    modelo.objetivo = pyEnv.Objective(expr=sum(valores_itens[i] * modelo.x[i] for i in modelo.I),
                                    sense=pyEnv.maximize)
    

    # restricoes
    modelo.rest = pyEnv.Constraint(expr=sum(pesos_itens[i] * modelo.x[i] for i in modelo.I) <= capacidade)

    # ------------------ RESOLUCAO DO MODELO ----------------------- #
    solver = pyEnv.SolverFactory('glpk')

    # mostrando na tela o log do server
    solver = solver.solve(modelo, tee=True)


    # ------------------- IMPRIMINDO AS VARIAVEIS DE DECISAO --------------------
    lista = list(modelo.x.keys())
    for i in lista:
        print(i, '--', modelo.x[i]())
    

    print('Valor objetivo = ', modelo.objetivo())

    

mochila_bonus("teste.txt")
