import pyomo.environ as pyEnv

path = r"C:\Users\jhona\anaconda3\Library\bin\glpsol.exe"

##------------------DADOS------------------##
lucros = [92, 57, 49, 68, 60, 43, 67, 84, 87, 70]
pesos = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
capacidade = 165
m = len(lucros)

##---------------DECLARACAO DO MODELO---------------##
modelo = pyEnv.ConcreteModel()  
modelo.I = range(m)

modelo.x = pyEnv.Var(modelo.I, within=pyEnv.Binary)

modelo.objetivo = pyEnv.Objective(expr=sum(lucros[i] * modelo.x[i] for i in modelo.I),
                                   sense=pyEnv.maximize)

modelo.rest = pyEnv.Constraint(expr=sum(pesos[i] * modelo.x[i] for i in modelo.I) <= capacidade)

##-----------------RESOLUCAO DO MODELO-----------------##
solver = pyEnv.SolverFactory('glpk', executable=path)
#solver = pyEnv.SolverFactory('cplex', executable=path, validate=False)
resultado_objetivo = solver.solve(modelo, tee=True)

##-----------------PRINT DAS VARIAVEIS DE DECISAO-----------------##
lista = list(modelo.x.keys())
for i in lista:
    print(i, '--', modelo.x[i]())

print('Valor objetivo =', modelo.objetivo())
