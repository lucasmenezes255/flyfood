import random

# ---------------------------------------------------------
# FUNÇÕES DE APOIO E CARREGAMENTO
# ---------------------------------------------------------

def carregar_distancias(caminho_arquivo):
    distancias = {}
    with open(caminho_arquivo, "r") as f:
        for i in range(1, 58):
            linha = f.readline()
            lista = linha.split()
            for j in range(i + 1, 59):
                if lista:
                    peso = int(lista.pop(0))
                    distancias[(i, j)] = peso
                    distancias[(j, i)] = peso
                else:
                    raise ValueError(f"Erro na linha {i}: elementos insuficientes.")
    return distancias

def custo_caminho(permutacao, distancias):
    soma = 0
    n = len(permutacao)
    for i in range(n - 1):
        soma += distancias[(permutacao[i], permutacao[i+1])]
    soma += distancias[(permutacao[-1], permutacao[0])]
    return soma

# ---------------------------------------------------------
# OPERADORES DO ALGORITMO (V2 - FOCO EM VARIEDADE)
# ---------------------------------------------------------

def inicializar_populacao(tamanho, n_cidades):
    populacao = []
    while len(populacao) < tamanho:
        individuo = list(range(1, n_cidades + 1))
        random.shuffle(individuo)
        if individuo not in populacao: # Garante variedade inicial
            populacao.append(individuo)
    return populacao

def selecionar_por_torneio(populacao, distancias, k=3):
    """
    PASSO 3 (V2): Seleção por Torneio
    Escolhe 'k' indivíduos aleatórios e o melhor entre eles vence.
    Isso reduz a 'sede ao pote' da roleta.
    """
    selecionados = random.sample(populacao, k)
    # Ordena pelo custo (menor para maior) e pega o primeiro
    vencedor = min(selecionados, key=lambda ind: custo_caminho(ind, distancias))
    return vencedor

def crossover_ox(pai1, pai2):
    """
    PASSO 4: Cruzamento (OX)
    Gera DOIS filhos invertendo os papéis dos pais.
    """
    def gerar_um_filho(p1_base, p2_fill):
        n = len(p1_base)
        c1, c2 = sorted(random.sample(range(n), 2))
        filho = [None] * n
        filho[c1:c2+1] = p1_base[c1:c2+1]
        
        pos_filho = (c2 + 1) % n
        pos_pai2 = (c2 + 1) % n
        while None in filho:
            cidade = p2_fill[pos_pai2]
            if cidade not in filho:
                filho[pos_filho] = cidade
                pos_filho = (pos_filho + 1) % n
            pos_pai2 = (pos_pai2 + 1) % n
        return filho

    filho1 = gerar_um_filho(pai1, pai2)
    filho2 = gerar_um_filho(pai2, pai1)
    return filho1, filho2

def mutacao_swap(solucao):
    n = len(solucao)
    i, j = random.sample(range(n), 2)
    solucao[i], solucao[j] = solucao[j], solucao[i]
    return solucao

def busca_local_2opt(solucao, distancias):
    """
    PASSO 6: 2-opt (Melhoria Local)
    """
    n = len(solucao)
    melhor_solucao = list(solucao)
    melhor_custo = custo_caminho(melhor_solucao, distancias)
    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(n):
            for j in range(i + 2, n):
                idx_i, idx_i_plus = i, (i + 1) % n
                idx_j, idx_j_plus = j, (j + 1) % n
                if idx_j_plus == idx_i: continue
                a, b = melhor_solucao[idx_i], melhor_solucao[idx_i_plus]
                c, d = melhor_solucao[idx_j], melhor_solucao[idx_j_plus]
                custo_atual = distancias[(a, b)] + distancias[(c, d)]
                novo_custo = distancias[(a, c)] + distancias[(b, d)]
                if novo_custo < custo_atual:
                    melhor_solucao[i+1 : j+1] = melhor_solucao[i+1 : j+1][::-1]
                    melhor_custo -= (custo_atual - novo_custo)
                    melhorou = True
                    break
            if melhorou: break
    return melhor_solucao

def substituir_pior(populacao, novo_filho, distancias):
    # Verifica se o filho já existe na população para manter a variedade
    if novo_filho in populacao:
        return False, 0
    
    custos = [custo_caminho(ind, distancias) for ind in populacao]
    pior_custo = max(custos)
    idx_pior = custos.index(pior_custo)
    custo_filho = custo_caminho(novo_filho, distancias)
    
    if custo_filho < pior_custo:
        populacao[idx_pior] = novo_filho
        return True, pior_custo
    return False, pior_custo

# ---------------------------------------------------------
# EXECUÇÃO PRINCIPAL
# ---------------------------------------------------------

if __name__ == "__main__":
    TAMANHO_POPULACAO = 20 # Aumentado para mais variedade
    N_GERACOES = 1000
    PROB_BUSCA_LOCAL = 0.3 # Variação: Não aplicar 2-opt em todos (reduz a sede ao pote)
    TAXA_MUTACAO = 0.2     # Mutação maior para variedade
    ARQUIVO_DADOS = "edgesbrasil58.tsp"
    
    distancias = carregar_distancias(ARQUIVO_DADOS)
    populacao = inicializar_populacao(TAMANHO_POPULACAO, 58)
    
    melhor_inicial = min([custo_caminho(ind, distancias) for ind in populacao])
    print(f"Melhor inicial: {melhor_inicial}")
    print(f"Iniciando V2 (Torneio + Busca Local Probabilística)...")

    for g in range(N_GERACOES):
        # Seleção por Torneio (2 pais separadamente)
        pai1 = selecionar_por_torneio(populacao, distancias, k=3)
        pai2 = selecionar_por_torneio(populacao, distancias, k=3)
        
        # Crossover (Gera dois filhos)
        filhos = crossover_ox(pai1, pai2)
        
        for filho in filhos:
            # Mutação
            if random.random() < TAXA_MUTACAO:
                filho = mutacao_swap(filho)
            
            # PASSO 6: Melhoria Local (Variação: Somente com probabilidade)
            if random.random() < PROB_BUSCA_LOCAL:
                filho = busca_local_2opt(filho, distancias)
            
            # Substituição
            substituir_pior(populacao, filho, distancias)
        
        if (g + 1) % 100 == 0:
            custos = [custo_caminho(ind, distancias) for ind in populacao]
            print(f"Geração {g+1:4}: Melhor = {min(custos)} | Média = {sum(custos)/len(custos):.1f}")

    custos_finais = [custo_caminho(ind, distancias) for ind in populacao]
    print(f"\nMelhor Inicial: {melhor_inicial}")
    print(f"Melhor Final:   {min(custos_finais)}")
