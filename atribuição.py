# resolvendo o problema da atribuição com um algoritmo guloso

def aloca_trabalhos(custos):
    n = len(custos)
    trabalhos_alocados = [None] * n
    pessoas_usadas = [False] * n

    for i in range(n):
        menor_custo = float('inf')
        melhor_pessoa = None

        for j in range(n):
            if not pessoas_usadas[j] and custos[i][j] < menor_custo:
                menor_custo = custos[i][j]
                melhor_pessoa = j

        trabalhos_alocados[i] = melhor_pessoa
        pessoas_usadas[melhor_pessoa] = True

    return trabalhos_alocados

# exemplo de custos
custos = [
    [1, 5, 2],
    [2, 7, 4],
    [8, 3, 6]
]

trabalhos_alocados = aloca_trabalhos(custos)

for i in range(3):
    for j in range(3):
        print(f"Custo de atribuição da pessoa {i+1} para o trabalho {j+1}: {custos[i][j]}")

print("Trabalhos alocados para cada pessoa:")
for i, trabalho in enumerate(trabalhos_alocados):
    print(f"Pessoa {i+1} -> Trabalho {trabalho+1}")