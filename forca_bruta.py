import itertools
import os
import time

# Formatação da matriz de entrada
def formatacao_matriz(entrada, row, column):
    for i in range(row):
        linha_matriz = []
        for j in range(column):
            valor = elementos_puros[i * column + j]
            linha_matriz.append(valor)
            if valor != '0':
                localizacao_cidades[valor] = (i, j)
        entrada.append(linha_matriz)
    return entrada

# Função que calcula a distância entre 2 cidades da matriz
def calculo_distancia(cidades, distancia_cidades):
    for c1, c2 in itertools.combinations(cidades, 2):
        pos1 = cidades[c1]
        pos2 = cidades[c2]
        distancia = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        distancia_cidades[(c1, c2)] = distancia
        distancia_cidades[(c2, c1)] = distancia

# Função que calcula uma rota permultada
def calculo_tamanho_rota(rota, distancia, limite_atual):
    total = 0
    for c in range(len(rota) - 1):
        total += distancia[(rota[c], rota[c+1])]
        # Faz a poda da rota se ela for maior que a menor rota já verificada
        if limite_atual is not None and total >= limite_atual:
            return None
    total += distancia[rota[-1], rota[0]]
    return total

arquivos = ['matriz5.txt', 'matriz8.txt', 'matriz10.txt', 'matriz11.txt', 'matriz12.txt', 'matriz13.txt', 'matriz14.txt']

for nome_arquivo in arquivos:
# Declaração de variáveis e estruturas necessárias
    matriz = []
    localizacao_cidades = {}
    distancia_cidades = {}
    menor_distancia = None
    melhor_rota = None

    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r') as entrada:
            entrada_bruta = entrada.read() 
            lista_matriz = entrada_bruta.replace('\\n', ' ')  # Garantia que \n não vá atrapalhar na criação da matriz
            elementos = lista_matriz.split()
            elementos_puros = elementos[2:] # Guarda os elementos da matriz, zeros (0) e cidades (A, B, C..)
            linha = int(elementos[0]) # Número de linhas da matriz
            coluna = int(elementos[1])
            print('='*50) # Número de colunas da matriz
            print(f"{' MATRIZ DE ENTRADA ':^50}")
            print('='*50)
            print(f"{' PARA INTERROMPER DURANTE A EXECUÇÃO: CTRL + C ':^50}\n")
            print(entrada_bruta)
        if nome_arquivo == 'matriz11.txt':
            print('\nATENÇÃO, MATRIZ COM 11 CIDADES. SOLUÇÃO PREVISTA EM 1 MINUTO')
        elif nome_arquivo == 'matriz12.txt':
            print('\nATENÇÃO, MATRIZ COM 12 CIDADES. SOLUÇÃO PREVISTA EM 11 MINUTOS')
        elif nome_arquivo == 'matriz13.txt':
            print('\nATENÇÃO, MATRIZ COM 13 CIDADES. SOLUÇÃO PREVISTA EM 2 HORAS')
        elif nome_arquivo == 'matriz14.txt':
            print('\nATENÇÃO, MATRIZ COM 14 CIDADES. SOLUÇÃO PREVISTA EM 25 HORAS')

        inicio = time.perf_counter()

        matriz = formatacao_matriz(matriz, linha, coluna)
        calculo_distancia(localizacao_cidades, distancia_cidades)
        lista_cidades = list(localizacao_cidades.keys())
        cidade_origem = 'R'
        lista_cidades = [c for c in lista_cidades if c != 'R']

        # Geração de todas as n! rotas da matriz 
        for permuta in itertools.permutations(lista_cidades, len(lista_cidades)):
            rota = [cidade_origem] + list(permuta)
            tamanho_rota = calculo_tamanho_rota(rota, distancia_cidades, menor_distancia)

            if tamanho_rota is None: 
                continue  # Passa direto pra próxima rota no caso da atual ser maior que a menor rota já verificada
            elif menor_distancia is None or tamanho_rota < menor_distancia:
                menor_distancia = tamanho_rota
                melhor_rota = rota

        fim = time.perf_counter()
        
        # Formatação da saída de lista para string
        resultado = " ".join([cid for cid in melhor_rota if cid != 'R'])

        # Saída OFICIAL do programa. Essa é a rota de menor custo que o drone precisa efetuar
        print(f"\nMenor rota: {resultado}")

        # Tamanho da distância da menor rota de entregas
        print(f"\nTamanho da rota: {menor_distancia}")
        print(f'\nDemorou: {fim-inicio:.2f} segundos\n')
    else:
        print('\nArquivo não encontrado!')