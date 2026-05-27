import sys
import os
import time
import random
import itertools
import memetico_V3

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

def converter_para_distancias_ag(localizacao_cidades):
    # R + cidades ordenadas alfabeticamente
    cidades_entrega = sorted([c for c in localizacao_cidades.keys() if c != 'R'])
    lista_cidades = ['R'] + cidades_entrega
    
    # Mapeamento 1-based
    mapeamento_index = {i + 1: cidade for i, cidade in enumerate(lista_cidades)}
    mapeamento_cidade = {cidade: i + 1 for i, cidade in enumerate(lista_cidades)}
    
    n_cidades = len(lista_cidades)
    distancias_ag = {}
    
    # Calcular Manhattan distances
    for i in range(1, n_cidades + 1):
        for j in range(1, n_cidades + 1):
            if i != j:
                c1 = mapeamento_index[i]
                c2 = mapeamento_index[j]
                pos1 = localizacao_cidades[c1]
                pos2 = localizacao_cidades[c2]
                dist = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
                distancias_ag[(i, j)] = dist
                distancias_ag[(j, i)] = dist
            else:
                distancias_ag[(i, j)] = 0
                
    return distancias_ag, mapeamento_index, mapeamento_cidade

def salvar_edges_tsp(distancias_ag, n_cidades, caminho_saida):
    with open(caminho_saida, 'w') as f:
        for i in range(1, n_cidades):
            linha = []
            for j in range(i + 1, n_cidades + 1):
                linha.append(str(distancias_ag[(i, j)]))
            f.write(" ".join(linha) + "\n")

def rodar_ag(distancias_ag, n_cidades, metodo_selecao_pais="torneio", tamanho_populacao=20, n_geracoes=1000, prob_busca_local=0.3, taxa_mutacao=0.2):
    populacao = memetico_V3.inicializar_populacao(tamanho_populacao, n_cidades)
    
    for g in range(n_geracoes):
        # Selecionar pais
        pai1 = memetico_V3.selecionar_pai(populacao, distancias_ag, metodo=metodo_selecao_pais)
        pai2 = memetico_V3.selecionar_pai(populacao, distancias_ag, metodo=metodo_selecao_pais)
        
        # Crossover
        filhos = memetico_V3.crossover_ox(pai1, pai2)
        
        filhos_processados = []
        for filho in filhos:
            # Mutação
            if random.random() < taxa_mutacao:
                filho = memetico_V3.mutacao_swap(filho)
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

def rodar_forca_bruta(localizacao_cidades):
    distancia_cidades = {}
    
    # Calcular distâncias entre cidades para a força bruta
    for c1, c2 in itertools.combinations(localizacao_cidades.keys(), 2):
        pos1 = localizacao_cidades[c1]
        pos2 = localizacao_cidades[c2]
        dist = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        distancia_cidades[(c1, c2)] = dist
        distancia_cidades[(c2, c1)] = dist
        
    lista_cidades = list(localizacao_cidades.keys())
    cidade_origem = 'R'
    lista_cidades = [c for c in lista_cidades if c != 'R']
    
    menor_distancia = None
    melhor_rota = None
    
    def calculo_tamanho_rota(rota, distancia, limite_atual):
        total = 0
        for c in range(len(rota) - 1):
            total += distancia[(rota[c], rota[c+1])]
            if limite_atual is not None and total >= limite_atual:
                return None
        total += distancia[(rota[-1], rota[0])]
        return total
        
    for permuta in itertools.permutations(lista_cidades, len(lista_cidades)):
        rota = [cidade_origem] + list(permuta)
        tamanho_rota = calculo_tamanho_rota(rota, distancia_cidades, menor_distancia)
        
        if tamanho_rota is None:
            continue
        elif menor_distancia is None or tamanho_rota < menor_distancia:
            menor_distancia = tamanho_rota
            melhor_rota = rota
            
    return menor_distancia, melhor_rota

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
        
    caminho_arquivo = sys.argv[1]
    
    print(f"Lendo matriz de: {caminho_arquivo}")
    localizacao_cidades = carregar_matriz_flyfood(caminho_arquivo)
    
    # R + cidades
    cidades_entrega = [c for c in localizacao_cidades.keys() if c != 'R']
    print(f"Total de pontos de entrega: {len(cidades_entrega)} ({', '.join(sorted(cidades_entrega))})")
    
    # 1. Converter para formato AG
    distancias_ag, mapeamento_index, mapeamento_cidade = converter_para_distancias_ag(localizacao_cidades)
    
    # Salvar em arquivo no mesmo formato do brazil58 para demonstrar a conversão
    caminho_saida_tsp = caminho_arquivo.replace(".txt", "_edges.tsp")
    salvar_edges_tsp(distancias_ag, len(localizacao_cidades), caminho_saida_tsp)
    print(f"Matriz de distâncias salva no formato brazil58 em: {caminho_saida_tsp}")
    
    print("\n" + "="*60)
    print(f"{' COMPARANDO ALGORITMO GENÉTICO VS FORÇA BRUTA ':^60}")
    print("="*60)
    
    # 2. Executar Força Bruta
    print("\nExecutando Força Bruta com poda...")
    inicio_fb = time.perf_counter()
    custo_fb, rota_fb = rodar_forca_bruta(localizacao_cidades)
    fim_fb = time.perf_counter()
    tempo_fb = fim_fb - inicio_fb
    
    rota_fb_formatada = " ".join([c for c in rota_fb if c != 'R'])
    print(f"Força Bruta finalizada em {tempo_fb:.4f} segundos.")
    print(f"  Melhor Rota (FB): {rota_fb_formatada}")
    print(f"  Custo (FB):       {custo_fb}")
    
    # 3. Executar Algoritmo Genético (V3)
    # Vamos rodar com torneio e roleta
    for metodo in ["torneio", "roleta"]:
        print(f"\nExecutando Algoritmo Genético (V3) - Seleção de Pais: {metodo.upper()}...")
        inicio_ag = time.perf_counter()
        custo_ag, rota_ag = rodar_ag(distancias_ag, len(localizacao_cidades), metodo_selecao_pais=metodo)
        fim_ag = time.perf_counter()
        tempo_ag = fim_ag - inicio_ag
        
        rota_ag_formatada = formatar_rota(rota_ag, mapeamento_index)
        print(f"Algoritmo Genético finalizado em {tempo_ag:.4f} segundos.")
        print(f"  Melhor Rota (AG): {rota_ag_formatada}")
        print(f"  Custo (AG):       {custo_ag}")
        diferenca_percentual = ((custo_ag - custo_fb) / custo_fb) * 100
        print(f"  Diferença de Custo vs FB: {diferenca_percentual:.2f}%")
