import pyomo.environ as pyEnv
path = r"C:\Users\jhona\anaconda3\Library\bin\glpsol.exe"

# custo de realizar o transporte da fabrica i para o cliente j
# definindo a matriz Cij
cij = [[162, 247],
       [117, 193],
       [131, 185]]

# definindo a capacidade das fabricas
capacidades = [1000, 1500, 1200]

# definindo a demanda dos clientes
demandas = [2300, 1400]

# obtendo o numero de fabricas (m) e o numero de cliente (n)
m = len(capacidades)
n = len(demandas)

## DECLARAÇÃO DO MODELO E SEUS PARAMETROS ##

## ------- DECLARANDO O MODELO E SEUS PARAMETROS -------- ##
# modelo
modelo = pyEnv.ConcreteModel()

# definindo o indice para as fabricas
modelo.I = pyEnv.RangeSet(m)

# definindo o indice para os clientes
modelo.J = pyEnv.RangeSet(n)

# definindo as variaveis de decisao Xij
modelo.x = pyEnv.Var(modelo.I, modelo.J, within=pyEnv.NonNegativeReals)

# definindo o custo de transporte da fabrica i para o cliente j
modelo.c = pyEnv.Param(modelo.I, modelo.J, initialize=lambda modelo, i, j: cij[i-1][j-1])


# definindo a capacidade de cada fabrica i
modelo.b = pyEnv.Param(modelo.I, initialize=lambda modelo, i: capacidades[i-1])

# definindo a demanda de cada cliente j
modelo.d = pyEnv.Param(modelo.J, initialize=lambda modelo, j: demandas[j-1])


## ---------- DECLARANDO A FUNÇÃO OBJETIVA  ##
def func_objetivo(modelo):
    return sum(modelo.x[i, j] * modelo.c[i, j] for i in modelo.I for j in modelo.J)

# definindo que a função objetiva é de minimização (minimizar o custo de transporte)
modelo.objetivo = pyEnv.Objective(rule=func_objetivo, sense=pyEnv.minimize)


## -------- RESTRIÇÕES --------------- ##
# cada fabrica não exceder sua capacidade
def rule_rest1(modelo, i):
    return sum(modelo.x[i, j] for j in modelo.J) <= modelo.b[i]


# primeira restrição: não pode exceder a capacidade da fábrica
modelo.rest1 = pyEnv.Constraint(modelo.I, rule=rule_rest1)

# cada cliente ter sua demanda atendida
def rule_rest2(modelo, j):
    return sum(modelo.x[i, j] for i in modelo.I) >= modelo.d[j]

# segunda restrição: cada cliente deve ter sua demanda atendida
modelo.rest2 = pyEnv.Constraint(modelo.J, rule=rule_rest2)


## -------------- RESOLUÇÃO DO MODELO ---------------- ##
# resolve o modelo usando o solver glpk
solver = pyEnv.SolverFactory('glpk', executable=path)
resultado = solver.solve(modelo, tee=False)

# avalia a função objetiva e imprime o resultado da solução
print('\n------------------------\n')
# modelo.pprint()
modelo.objetivo()
print(resultado)

## -------------- PRINT DAS VARIAVEIS DE DECISAO ESCOLHIDAS ------------------- ##
## (fábrica, cliente)
lista = list(modelo.x.keys())
for i in lista:
    if modelo.x[i]() != 0:
        print(i, '−−', modelo.x[i]())