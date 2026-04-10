import sys
import itertools

# Função que calcula a distância entre 2 cidades da matriz
def calculo_distancia(cidades, distancia_cidades):
    for c1, c2 in itertools.combinations(cidades, 2):
        pos1 = cidades[c1]
        pos2 = cidades[c2]
        distancia = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        distancia_cidades[(c1, c2)] = distancia
        distancia_cidades[(c2, c1)] = distancia

# Função que calcula uma rota permultada
def calculo_tamanho_rota(rota, distancia, dist_parcial):
    total = 0
    for c in range(len(rota) - 1):
        total += distancia[(rota[c], rota[c+1])]
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
melhor_rota = None
menor_distancia = None
linha_matriz = []
# Formatação da matriz de entrada
for i in range(linha):
    for j in range(coluna):
        valor = elementos_puros[i * coluna + j]
        linha_matriz.append(valor)
        if valor != '0':
            localizacao_cidades[valor] = (i, j)
    matriz.append(linha_matriz)

calculo_distancia(localizacao_cidades, distancia_cidades)
lista_cidades = list(localizacao_cidades.keys())
for cidade in lista_cidades:
    if cidade == 'R':
        cidade_origem = cidade
        lista_cidades.remove('R')
        break
# Geração de todas as n! rotas da matriz 
for permuta in itertools.permutations(lista_cidades, len(lista_cidades)):
    rota = [cidade_origem] + list(permuta)
    tamanho_rota = calculo_tamanho_rota(rota, distancia_cidades, distancia_parcial)

    if menor_distancia == None:
        menor_distancia = tamanho_rota
        melhor_rota = rota + [cidade_origem]
    elif tamanho_rota <= menor_distancia:
        menor_distancia = tamanho_rota
        melhor_rota = rota + [cidade_origem]

# Formatação da saída de lista para string
resultado = " ".join([cid for cid in melhor_rota if cid != 'R'])

# Tamanho da distância da menor rota de entregas
print(menor_distancia)

# Saída OFICIAL do programa. Essa é a rota de menor custo que o drone precisa efetuar
print(resultado)