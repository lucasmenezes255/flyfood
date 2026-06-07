import sys
import os
import time
import random
import memetico_V3

arquivos = {'matriz5.txt':[{
                'tempo': 0.0003,
                'rota': 'A C E D B',
                'custo': 18
                }],
            'matriz8.txt':[{
                'tempo': 0.0449,
                'rota': 'A B D G H F E C',
                'custo': 24
                }],
            'matriz10.txt':[{
                'tempo': 3.7273,
                'rota': 'A B D F G H J I E C',
                'custo': 30
                }],
            'matriz11.txt':[{
                'tempo': 32.7921,
                'rota': 'A B D F G H K J I E C',
                'custo': 30
                }],
            'matriz12.txt':[{
                'tempo': 442.8928,
                'rota': 'A B D F G H K L J I E C',
                'custo': 34
                }],
            'matriz13.txt':[{
                'tempo': 7618.0707,
                'rota': 'A B D F G H K L M J I E C',
                'custo': 34
                }],
            'matriz14.txt':[{
                'tempo': 90456.3126,
                'rota': 'A B D F G I L M N K J H E C',
                'custo': 50
                }]
}


def carregar_matriz_flyfood(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo {caminho_arquivo} não encontrado.")
    
    with open(caminho_arquivo, 'r') as f:
        linhas = f.read().splitlines()
        
    if not linhas:
        raise ValueError("O arquivo está vazio.")
        
    dim = linhas[0].split()
    r_dim = int(dim[0])
    c_dim = int(dim[1])
    
    elementos = []
    for l in linhas[1:]:
        elementos.extend(l.split())
        
    localizacao_cidades = {}
    for i in range(r_dim):
        for j in range(c_dim):
            idx = i * c_dim + j
            if idx < len(elementos):
                valor = elementos[idx]
                if valor != '0':
                    localizacao_cidades[valor] = (i, j)
            else:
                raise ValueError("Dimensões da matriz inconsistentes com os elementos fornecidos.")
                
    return localizacao_cidades

def converter_para_distancias_ag(localizacao_cidades, arquivo):
    # R + cidades ordenadas alfabeticamente
    cidades_entrega = sorted([c for c in localizacao_cidades.keys() if c != 'R'])
    lista_cidades = ['R'] + cidades_entrega

    # Mapeamento 1-based
    mapeamento_index = {i + 1: cidade for i, cidade in enumerate(lista_cidades)}
    mapeamento_cidade = {cidade: i + 1 for i, cidade in enumerate(lista_cidades)}
    n_cidades = len(lista_cidades)
    
    arquivos_distancias = {
        'matriz5.txt': 'matriz5_distances.txt',
        'matriz8.txt': 'matriz8_distances.txt',
        'matriz10.txt': 'matriz10_distances.txt',
        'matriz11.txt': 'matriz11_distances.txt',
        'matriz12.txt': 'matriz12_distances.txt',
        'matriz13.txt': 'matriz13_distances.txt',
        'matriz14.txt': 'matriz14_distances.txt',
    }
    
    distancias_ag = {}
    distancias = arquivos_distancias[arquivo]
    # Lê os arquivos com as distâncias
    with open(distancias, "r") as f:
        for i in range(1, n_cidades):
            linha = f.readline()
            lista = linha.split()
            for j in range(i + 1, n_cidades + 1):
                if lista:
                    peso = int(lista.pop(0))
                    distancias_ag[(i, j)] = peso
                    distancias_ag[(j, i)] = peso
                else:
                    raise ValueError(f"Erro na linha {i}: elementos insuficientes.")
    print(distancias_ag)
    return distancias_ag, mapeamento_index, mapeamento_cidade

def salvar_edges_tsp(distancias_ag, n_cidades, caminho_saida):
    with open(caminho_saida, 'w') as f:
        for i in range(1, n_cidades):
            linha = []
            for j in range(i + 1, n_cidades + 1):
                linha.append(str(distancias_ag[(i, j)]))
            f.write(" ".join(linha) + "\n")

def rodar_ag(distancias_ag, n_cidades, metodo_selecao_pais="torneio", tamanho_populacao=200, n_geracoes=2500, prob_busca_local=0.15, taxa_mutacao=0.35):
    populacao = memetico_V3.inicializar_populacao(tamanho_populacao, n_cidades)
    
    for _ in range(n_geracoes):
        # Selecionar pais
        pai1 = memetico_V3.selecionar_pai(populacao, distancias_ag, metodo=metodo_selecao_pais)
        pai2 = memetico_V3.selecionar_pai(populacao, distancias_ag, metodo=metodo_selecao_pais)
        
        # Crossover
        filhos = memetico_V3.crossover_ox(pai1, pai2)
        
        filhos_processados = []
        for filho in filhos:
            # Mutação
            if random.random() < taxa_mutacao:
                filho = memetico_V3.mutacao_inversao(filho)
            # Busca local 2-opt
            if random.random() < prob_busca_local:
                filho = memetico_V3.busca_local_2opt(filho, distancias_ag)
            filhos_processados.append(filho)
            
        # Seleção de sobreviventes
        populacao = memetico_V3.selecionar_sobreviventes_steady_state(populacao, filhos_processados, distancias_ag, tamanho_populacao)
        
    custos_finais = [memetico_V3.custo_caminho(ind, distancias_ag) for ind in populacao]
    melhor_custo_final = min(custos_finais)
    idx_melhor = custos_finais.index(melhor_custo_final)
    melhor_rota_final = populacao[idx_melhor]
    
    return melhor_custo_final, melhor_rota_final

def formatar_rota(rota_indices, mapeamento_index):
    # Encontra onde está R (indice 1) e rotaciona a rota para começar por 1
    idx_r = rota_indices.index(1)
    rota_rotacionada = rota_indices[idx_r:] + rota_indices[:idx_r]
    # Mapear de volta para caracteres
    rota_letras = [mapeamento_index[i] for i in rota_rotacionada]
    # Retornar apenas a ordem de entrega (sem R)
    retorno = " ".join([c for c in rota_letras if c != 'R'])
    return retorno

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 comparar_algoritmos.py <caminho_matriz_flyfood>")
        sys.exit(1)

    folder = 'forca_bruta'
    path_configurado = os.path.join(folder, sys.argv[1])
    caminho_arquivo = sys.argv[1]
    
    print(f"Lendo matriz de: {caminho_arquivo}")
    localizacao_cidades = carregar_matriz_flyfood(path_configurado)
    
    # R + cidades
    cidades_entrega = [c for c in localizacao_cidades.keys() if c != 'R']
    print(f"Total de pontos de entrega: {len(cidades_entrega)} ({', '.join(sorted(cidades_entrega))})")
    
    # Obeter as distâncias entre as cidades e o mapeamento entre cidade e índice
    distancias_ag, mapeamento_index, mapeamento_cidade = converter_para_distancias_ag(localizacao_cidades, caminho_arquivo)

    print("\n" + "="*60)
    print(f"{' COMPARANDO ALGORITMO GENÉTICO VS FORÇA BRUTA ':^60}")
    print("="*60)
    
    # Exibir os dados da Força Bruta
    print("\n\033[32mDados da força bruta com poda")
    print('-'*60)
    
    dados_fb = arquivos[caminho_arquivo] 
    print(f"  Força Bruta finalizada em \033[33m{dados_fb[0]['tempo']}\033[32m segundos.")
    print(f"  Melhor Rota (FB): \033[33m{dados_fb[0]['rota']}\033[32m")
    print(f"  Custo (FB):       \033[33m{dados_fb[0]['custo']}\033[m")
    
    # Executar Algoritmo Genético (V3) com torneio E roleta
    for metodo in ["torneio", "roleta"]:
        print(f"\n\033[36mExecutando Algoritmo Genético (V3) - Seleção de Pais: \033[31m{metodo.upper()}...\033[36m")
        print('-'*60)
        inicio_ag = time.perf_counter()
        custo_ag, rota_ag = rodar_ag(distancias_ag, len(localizacao_cidades), metodo_selecao_pais=metodo)
        fim_ag = time.perf_counter()
        tempo_ag = fim_ag - inicio_ag
        
        rota_ag_formatada = formatar_rota(rota_ag, mapeamento_index)
        print(f"Algoritmo Genético finalizado em \033[33m{tempo_ag:.4f}\033[36m segundos.")
        print(f"  Melhor Rota (AG): \033[33m{rota_ag_formatada}\033[36m")
        print(f"  Custo (AG):       \033[33m{custo_ag}\033[36m")
        diferenca_percentual = ((custo_ag - dados_fb[0]['custo']) / dados_fb[0]['custo']) * 100
        print(f"  Diferença de Custo vs FB: \033[33m{diferenca_percentual:.2f}%\033[m")