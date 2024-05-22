import pyomo.environ as pyEnv

# definindo a função para resolver o problema
def resolver_problema_mochila_multipla(lucros, pesos, capacidades_mochilas):
    
    # definindo o número de itens e de mochilas
    m = len(lucros)
    n_mochilas = len(capacidades_mochilas)

    # criando o modelo
    modelo = pyEnv.ConcreteModel()

    # definindo o conjunto de itens e de mochilas
    modelo.I = range(m)
    modelo.J = range(n_mochilas)

    # criando as variaveis de decisão, e especificando que elas devem ser binárias
    modelo.x = pyEnv.Var(modelo.I, modelo.J, within=pyEnv.Binary)


    # definindo a função objetiva: maximizar o lucro total, considerando que agora existe mais de uma mochila
    modelo.objetivo = pyEnv.Objective(expr=sum(lucros[i] * modelo.x[i, j] for i in modelo.I for j in modelo.J),
                                       sense=pyEnv.maximize)

    # definindo a restrição do problema: a soma dos pesos colocados na mochila j deve ser <=  que a capacidade da mochila j
    modelo.rest = pyEnv.ConstraintList()
    for j in modelo.J:
        modelo.rest.add(
            sum(pesos[i] * modelo.x[i, j] for i in modelo.I) <= capacidades_mochilas[j])

    # tenho que definir uma outra restrição: cada item so pode ser colocado em uma única mochila
    modelo.rest_unicidade_item = pyEnv.ConstraintList()
    for i in modelo.I:
        modelo.rest_unicidade_item.add(sum(modelo.x[i,j] for j in modelo.J) <=1)



    # indicando o solver resolvedor do problema
    solver = pyEnv.SolverFactory('glpk')

    # mostrando na tela o log do server (para não mostrar, basta fazer tee=False)
    resultado = solver.solve(modelo, tee=True)

    # obtendo o valor objetivo da solução
    resultado_objetivo = pyEnv.value(modelo.objetivo)
    mochilas = {}
    for j in modelo.J:
        mochilas[j] = [i for i in modelo.I if modelo.x[i, j]() == 1]
    return resultado_objetivo, mochilas
    

# exemplo de instanciação

# valores dos itens
lucros = [92, 57, 49, 68, 60, 43, 67, 84, 87, 70]
# pesos dos itens
pesos = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
# capacidade das mochilas
capacidades_mochilas = [100, 100, 100]

resultado_objetivo, distribuicao_mochilas = resolver_problema_mochila_multipla(lucros, pesos, capacidades_mochilas)
if resultado_objetivo is not None:
    print("Valor objetivo:", resultado_objetivo)
    print("Distribuição das mochilas:")
    for mochila, itens in distribuicao_mochilas.items():
        print(f"Mochila {mochila + 1}: {itens}")

