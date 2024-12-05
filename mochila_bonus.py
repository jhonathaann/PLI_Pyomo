import pyomo.environ as pyEnv
import pulp


caminho = r"C:\Users\jhona\anaconda3\Library\bin\glpsol.exe"

def mochila_bonus(nome_arquivo):

    # lendo as instancias do arquivo
    with open(nome_arquivo, 'r') as file:

        # lendo o nome da intancia
        referencia = file.readline().strip()

        # lendo a quantidade de itens
        n = int(file.readline().strip())

        # lendo os valores do n itens
        valor_i = list(map(int, file.readline().strip().split()))

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

        '''print(valor_i)
        print(capacidade)
        print(pesos_itens)
        print(bonus_ij)'''


    ############################ REALIZANDO A MODELAGEM DO PROBLEMA ############################

    # ==== CRIANDO O MODELO
    modelo = pyEnv.ConcreteModel()

    modelo.I = range(n)
    modelo.J = range(n)
    modelo.ab = [(i,j) for i in modelo.I for j in modelo.I if i < j]

    # criando as variavei de decisao do problema
    modelo.x = pyEnv.Var(modelo.I, within=pyEnv.Binary)
    modelo.y = pyEnv.Var(modelo.ab, within=pyEnv.Binary)

    # passando os valores lidos para o modelo
    modelo.p = pyEnv.Param(modelo.I, initialize=lambda modelo, i: pesos_itens[i]) # peso de cada item
    modelo.v = pyEnv.Param(modelo.I, initialize=lambda modelo, i: valor_i[i])  # valor de cada item
    modelo.b = pyEnv.Param(modelo.I, modelo.J, initialize=lambda modelo, i, j: bonus_ij[i][j])  # bonus do item i com o item j

    # ==== FUNCAO OBJETIVO

    # primeiro somatorio (pegando apenas o valor do item i que esta na solucao)
    soma_x = sum(modelo.v[i] * modelo.x[i] for i in modelo.I)

    # segundo somatorio (pegando o bonus do item i com o item j casos ambos estejam na solucao)
    soma_y = sum(modelo.b[i,j] * modelo.y[i,j] for i,j in modelo.ab)

    # adicionando a funcao objetivo ao modelo
    modelo.objetivo = pyEnv.Objective(rule=(soma_x+soma_y), sense=pyEnv.maximize)

    # ==== RESTRICOES

    # restricao 1: os itens colocados na mochila devem ter um peso total <= capacidade da mochila
    def restricao_um(modelo, i):
        return sum(modelo.p[i] * modelo.x[i] for i in modelo.I) <= capacidade
    
    modelo.rest1 = pyEnv.Constraint(modelo.J, rule=restricao_um)

    # restricao 2: sistemas de equacoes que garante que o bonus so seja colocado na solucao quando ambos os itens estivem na solucao
    def restricao_dois(modelo,i,j):
        return modelo.y[i,j] <= modelo.x[i]
    
    modelo.rest2 = pyEnv.Constraint(modelo.ab, rule=restricao_dois)
    
    def restricao_tres(modelo,i,j):
        return modelo.y[i,j] <= modelo.x[j]

    modelo.rest3 = pyEnv.Constraint(modelo.ab, rule=restricao_tres)

    def restricao_quatro(modelo,i,j):
        return  modelo.y[i,j] >= modelo.x[i] + modelo.x[j] - 1
    modelo.rest4 = pyEnv.Constraint(modelo.ab, rule=restricao_quatro)

    # ==== SOLVER
    solver = pyEnv.SolverFactory('glpk')
    resultado = solver.solve(modelo, tee=True)

    # obtendo o valor da solucao
    resultado_funcao = pyEnv.value(modelo.objetivo)

    mochila = []

    # guardando na mochila os itens colocados na solucao
    for i in modelo.I:
        mochila.append(modelo.x[i]())

    return resultado_funcao, mochila, n, pesos_itens

resultado_funcao, mochila, n, pesos_itens = mochila_bonus("teste.txt")

print("valor da funcao objetivo:", resultado_funcao)

print("itens que foram colocados na mochila:")

peso = 0
for i in range(n):
  print(f"item {i}: {mochila[i]}")
  if mochila[i] == 0:
    peso = peso + pesos_itens[i]

print("peso total dos itens: ", peso)

