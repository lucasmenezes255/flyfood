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
    """
    PASSO 2: Avaliar cada rota (Calcula a distância total)
    """
    soma = 0
    n = len(permutacao)
    for i in range(n - 1):
        soma += distancias[(permutacao[i], permutacao[i+1])]
    # Fecha o ciclo voltando para a primeira cidade
    soma += distancias[(permutacao[-1], permutacao[0])]
    return soma

# ---------------------------------------------------------
# LÓGICA DO ALGORITMO MEMÉTICO
# ---------------------------------------------------------

def inicializar_populacao(tamanho, n_cidades):
    """
    PASSO 1: Criar várias rotas iniciais (Normalmente aleatórias)
    """
    populacao = []
    for _ in range(tamanho):
        individuo = list(range(1, n_cidades + 1))
        random.shuffle(individuo)
        populacao.append(individuo)
    return populacao

def busca_local_2opt(solucao, distancias):
    """
    PASSO 6: Melhorar localmente cada filho (Busca Local / Lapidação)
    """
    n = len(solucao)
    melhor_solucao = list(solucao)
    melhor_custo = custo_caminho(melhor_solucao, distancias)
    
    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(n):
            for j in range(i + 2, n):
                idx_i = i
                idx_i_plus = (i + 1) % n
                idx_j = j
                idx_j_plus = (j + 1) % n
                
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
    """
    PASSO 7: Formar nova geração
    Substitui o pior indivíduo da população pelo novo filho,
    se o filho for melhor.
    """
    # 1. Encontrar o índice do pior (maior custo)
    custos = [custo_caminho(ind, distancias) for ind in populacao]
    pior_custo = max(custos)
    idx_pior = custos.index(pior_custo)
    
    custo_filho = custo_caminho(novo_filho, distancias)
    
    # 2. Substituir se o filho for melhor
    if custo_filho < pior_custo:
        populacao[idx_pior] = novo_filho
        return True, pior_custo
    return False, pior_custo

def selecionar_por_roleta(populacao, distancias, n_pais=2):
    """
    PASSO 3: Selecionar as melhores rotas (Roleta)
    Como é um problema de minimização, usamos 1/custo para dar
    mais chance aos caminhos mais curtos.
    """
    # 1. Calcular a aptidão (fitness) de cada um: f = 1 / custo
    custos = [custo_caminho(ind, distancias) for ind in populacao]
    aptidoes = [1.0 / c for c in custos]
    soma_aptidoes = sum(aptidoes)
    
    pais_selecionados = []
    
    for _ in range(n_pais):
        r = random.uniform(0, soma_aptidoes)
        acumulado = 0
        for i, apt in enumerate(aptidoes):
            acumulado += apt
            if acumulado >= r:
                pais_selecionados.append(populacao[i])
                break
                
    return pais_selecionados

def crossover_ox(pai1, pai2):
    """
    PASSO 4: Cruzar soluções (Order Crossover - OX)
    Garante que o filho seja uma permutação válida sem repetições.
    """
    n = len(pai1)
    # 1. Escolher dois pontos de corte aleatórios
    p1, p2 = sorted(random.sample(range(n), 2))
    
    # 2. Criar o filho com o segmento do pai1
    filho = [None] * n
    filho[p1:p2+1] = pai1[p1:p2+1]
    
    # 3. Preencher o restante com o pai2 na ordem em que aparecem
    # Começamos a preencher após o ponto de corte p2
    pos_filho = (p2 + 1) % n
    pos_pai2 = (p2 + 1) % n
    
    while None in filho:
        cidade_pai2 = pai2[pos_pai2]
        if cidade_pai2 not in filho:
            filho[pos_filho] = cidade_pai2
            pos_filho = (pos_filho + 1) % n
        pos_pai2 = (pos_pai2 + 1) % n
        
    return filho

def mutacao_swap(solucao):
    """
    PASSO 5: Aplicar mutação (Swap)
    Troca a posição de duas cidades aleatórias.
    """
    n = len(solucao)
    i, j = random.sample(range(n), 2)
    solucao[i], solucao[j] = solucao[j], solucao[i]
    return solucao

# ---------------------------------------------------------
# EXECUÇÃO PRINCIPAL
# ---------------------------------------------------------

if __name__ == "__main__":
    # Configurações iniciais
    TAMANHO_POPULACAO = 10
    N_GERACOES = 500
    N_CIDADES = 58
    ARQUIVO_DADOS = "edgesbrasil58.tsp"
    
    # 1. Carregar Dados
    distancias = carregar_distancias(ARQUIVO_DADOS)
    
    # PASSO 1: Criar várias rotas iniciais
    print(f"Gerando população inicial de {TAMANHO_POPULACAO} indivíduos...")
    populacao = inicializar_populacao(TAMANHO_POPULACAO, N_CIDADES)
    
    # PASSO 2: Avaliar cada rota inicial
    custos_iniciais = [custo_caminho(ind, distancias) for ind in populacao]
    melhor_inicial = min(custos_iniciais)
    print(f"Melhor custo inicial: {melhor_inicial}")
    
    print(f"\nIniciando Evolução por {N_GERACOES} gerações...")
    
    # PASSO 8: Repetir o processo
    for g in range(N_GERACOES):
        # PASSO 3: Selecionar os melhores
        pais = selecionar_por_roleta(populacao, distancias, n_pais=2)
        
        # PASSO 4: Cruzar soluções
        filho = crossover_ox(pais[0], pais[1])
        
        # PASSO 5: Aplicar mutação (com 10% de chance para exemplo)
        if random.random() < 0.1:
            filho = mutacao_swap(filho)
        
        # PASSO 6: Melhorar localmente cada filho (O passo memético)
        filho = busca_local_2opt(filho, distancias)
        
        # PASSO 7: Formar nova geração (Substituição do pior)
        substituir_pior(populacao, filho, distancias)
        
        # Log de progresso
        if (g + 1) % 50 == 0:
            custos_atuais = [custo_caminho(ind, distancias) for ind in populacao]
            print(f"Geração {g+1:4}: Melhor Custo = {min(custos_atuais)}")

    # RESULTADOS FINAIS
    custos_finais = [custo_caminho(ind, distancias) for ind in populacao]
    melhor_final = min(custos_finais)
    idx_melhor = custos_finais.index(melhor_final)
    melhor_rota = populacao[idx_melhor]
    
    print("\n--- RESULTADOS FINAIS ---")
    print(f"Melhor custo Inicial: {melhor_inicial}")
    print(f"Melhor custo Final:   {melhor_final}")
    print(f"Melhoria total:       {melhor_inicial - melhor_final} unidades de distância")
    print("\nMelhor Rota encontrada:")
    print(melhor_rota)
