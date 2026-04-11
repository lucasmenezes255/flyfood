import sys
import itertools
import time

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

entrada_bruta = sys.stdin.read() # Formatação de entrada
lista_entrada = entrada_bruta.replace('\\n', ' ') # Garantia que \n não vá atrapalhar na criação da matriz
elementos = lista_entrada.split()
elementos_puros = elementos[2:] # Guarda os elementos da matriz, zeros (0) e cidades (A, B, C..)
linha = int(elementos[0]) # Número de linhas da matriz
coluna = int(elementos[1]) # Número de colunas da matriz
# Declaração de variáveis e estruturas necessárias
matriz = []
localizacao_cidades = {}
distancia_cidades = {}
menor_distancia = None
melhor_rota = None

inicio = time.perf_counter()
# Formatação da matriz de entrada
for i in range(linha):
    linha_matriz = []
    for j in range(coluna):
        valor = elementos_puros[i * coluna + j]
        linha_matriz.append(valor)
        if valor != '0':
            localizacao_cidades[valor] = (i, j)
    matriz.append(linha_matriz)

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

# Tamanho da distância da menor rota de entregas
print(menor_distancia)

# Saída OFICIAL do programa. Essa é a rota de menor custo que o drone precisa efetuar
print(resultado)
print()
print(f'Demorou: {fim-inicio}')