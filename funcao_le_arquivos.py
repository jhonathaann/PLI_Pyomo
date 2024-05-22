
# função para ler os dados de entrada
def ler_arquivo(nome_arquivo):

    # abrindo o arquivo especificado pelo nome em modo de leitura
    # o with é para garantir que o arquivo seja fechado corretamente
    with open(nome_arquivo, 'r') as arquivo:

        # le a primeira linha do arquivo e converte para int
        # capacidade da mochila
        capacidade = int(arquivo.readline()) 

        # le a segunda linha do arquivo e converte para int
        # numero de itens
        m = int(arquivo.readline())

        # inicializa duas listas para armazenar os lucros e os pesos dos itens
        lucros = []
        peso = []

        for i in range(m):

            # le a linha seguinte do arquivo
            txt = arquivo.readline()

            # divide a string em uma lista de substrings, separadas pelo espaço
            x = txt.split()

            # adiciona o primeiro elemento de x (que é o lucro) na lista lucros
            lucros.append(int(x[0]))

            # adiciona o segundo elemento de x (que é o peso) na lista pesos
            peso.append(int(x[1]))

    # retorna a capacidade da mochila, a lista com os lucros e os pesos dos itens        
    return capacidade, lucros, peso

# exemplo de uso da função
nome_arquivo = 'arquivo.txt'
capacidade, lucros, peso = ler_arquivo(nome_arquivo)
print("Capacidade:", capacidade)
print("Lucros:", lucros)
print("Pesos:", peso)