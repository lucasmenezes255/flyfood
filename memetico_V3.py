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
# OPERADORES DO ALGORITMO (V3 - OPERADORES CUSTOMIZADOS)
# ---------------------------------------------------------

def inicializar_populacao(tamanho, n_cidades):
    populacao = []
    while len(populacao) < tamanho:
        individuo = list(range(1, n_cidades + 1))
        random.shuffle(individuo)
        if individuo not in populacao: # Garante variedade inicial
            populacao.append(individuo)
    return populacao

def selecionar_por_torneio_binario(populacao, distancias):
    """
    PASSO 3: Seleção por Torneio Binário (k=2)
    Escolhe 2 indivíduos aleatórios e o de menor custo vence.
    """
    selecionados = random.sample(populacao, 2)
    return min(selecionados, key=lambda ind: custo_caminho(ind, distancias))

def selecionar_por_roleta(populacao, distancias):
    """
    PASSO 3: Seleção por Roleta (Roulette Wheel Selection)
    Como é um problema de minimização, usamos 1/custo para dar
    mais chance aos caminhos mais curtos.
    """
    custos = [custo_caminho(ind, distancias) for ind in populacao]
    aptidoes = [1.0 / c for c in custos]
    soma_aptidoes = sum(aptidoes)
    
    r = random.uniform(0, soma_aptidoes)
    acumulado = 0
    for i, apt in enumerate(aptidoes):
        acumulado += apt
        if acumulado >= r:
            return populacao[i]
    return populacao[-1]

def selecionar_pai(populacao, distancias, metodo="torneio"):
    if metodo == "torneio":
        return selecionar_por_torneio_binario(populacao, distancias)
    elif metodo == "roleta":
        return selecionar_por_roleta(populacao, distancias)
    else:
        raise ValueError(f"Método de seleção desconhecido: {metodo}")

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

def selecionar_sobreviventes_steady_state(populacao, filhos, distancias, tamanho_populacao):
    """
    PASSO 7: Seleção de Sobreviventes (Steady-State com mesclagem Pop + Filhos)
    Mescla a população e os filhos, ordena por custo (minimização),
    e seleciona os melhores indivíduos para formar a nova população,
    garantindo que o melhor indivíduo do conjunto seja sempre preservado.
    Evita indivíduos duplicados na população para manter a diversidade.
    """
    pool_completo = populacao + filhos
    # Ordena pelo custo (menor custo primeiro)
    pool_ordenado = sorted(pool_completo, key=lambda ind: custo_caminho(ind, distancias))
    
    nova_populacao = []
    for ind in pool_ordenado:
        if ind not in nova_populacao:
            nova_populacao.append(ind)
        if len(nova_populacao) == tamanho_populacao:
            break
            
    # Caso haja duplicados extremos e não preencha a população
    if len(nova_populacao) < tamanho_populacao:
        for ind in pool_ordenado:
            if len(nova_populacao) == tamanho_populacao:
                break
            nova_populacao.append(ind)
            
    return nova_populacao

# ---------------------------------------------------------
# EXECUÇÃO PRINCIPAL
# ---------------------------------------------------------

if __name__ == "__main__":
    TAMANHO_POPULACAO = 20
    N_GERACOES = 1000
    PROB_BUSCA_LOCAL = 0.3
    TAXA_MUTACAO = 0.2
    ARQUIVO_DADOS = "edgesbrasil58.tsp"
    
    # Configuração do método de seleção de pais: "torneio" ou "roleta"
    METODO_SELECAO_PAIS = "torneio"  # altere para "roleta" se desejar
    
    distancias = carregar_distancias(ARQUIVO_DADOS)
    populacao = inicializar_populacao(TAMANHO_POPULACAO, 58)
    
    melhor_inicial = min([custo_caminho(ind, distancias) for ind in populacao])
    print(f"Melhor inicial: {melhor_inicial}")
    print(f"Iniciando AG V3 (Seleção de Pais: {METODO_SELECAO_PAIS.upper()} | Sobreviventes: Steady-State com Mesclagem)...")

    for g in range(N_GERACOES):
        # Seleção dos pais (usando o método configurado)
        pai1 = selecionar_pai(populacao, distancias, metodo=METODO_SELECAO_PAIS)
        pai2 = selecionar_pai(populacao, distancias, metodo=METODO_SELECAO_PAIS)
        
        # Crossover (Gera dois filhos)
        filhos = crossover_ox(pai1, pai2)
        
        filhos_processados = []
        for filho in filhos:
            # Mutação
            if random.random() < TAXA_MUTACAO:
                filho = mutacao_swap(filho)
            
            # PASSO 6: Melhoria Local (Somente com probabilidade)
            if random.random() < PROB_BUSCA_LOCAL:
                filho = busca_local_2opt(filho, distancias)
                
            filhos_processados.append(filho)
            
        # Seleção de sobreviventes (Steady-state: mesclar população + filhos e selecionar os melhores)
        populacao = selecionar_sobreviventes_steady_state(populacao, filhos_processados, distancias, TAMANHO_POPULACAO)
        
        if (g + 1) % 100 == 0:
            custos = [custo_caminho(ind, distancias) for ind in populacao]
            print(f"Geração {g+1:4}: Melhor = {min(custos)} | Média = {sum(custos)/len(custos):.1f}")

    custos_finais = [custo_caminho(ind, distancias) for ind in populacao]
    melhor_final = min(custos_finais)
    idx_melhor = custos_finais.index(melhor_final)
    melhor_rota = populacao[idx_melhor]
    
    print(f"\nMelhor Inicial: {melhor_inicial}")
    print(f"Melhor Final:   {melhor_final}")
    print(f"Melhor Rota:    {melhor_rota}")
