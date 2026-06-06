import random

# ---------------------------------------------------------
#              FUNÇÕES DE APOIO E CARREGAMENTO
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

# ----------------------------------------------------------
#   OPERADORES DO ALGORITMO (V3 - OPERADORES CUSTOMIZADOS)
# ----------------------------------------------------------

def inicializar_populacao(tamanho, n_cidades):
    populacao = []
    while len(populacao) < tamanho:
        individuo = list(range(1, n_cidades + 1))   # Gera um inivíduo ex: [1,2,3,4,5,...,56,57,58]
        random.shuffle(individuo)                   # Embaralha esse indivíduo
        if individuo not in populacao:              # Garante variedade inicial
            populacao.append(individuo)
    return populacao

def selecionar_por_torneio_binario(populacao, distancias):
    """
        Seleção por torneio binário onde seleciona ALEATORIAMENTE dois 
        indivíduos da população e retorna o menor deles para ser o PAI
    """
    selecionados = random.sample(populacao, 2)
    return min(selecionados, key=lambda individuo: custo_caminho(individuo, distancias))

def selecionar_por_roleta(populacao, distancias):
    """
    e uma possivel alternativa para o passo 3, onde a seleção é feita por roleta (roulette wheel selection) baseada na 
    aptidão inversa (1/custo) para favorecer soluções de menor custo.
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
        Função de gerar filhos, que cruza dois pais usando o Order Crossover - OX,
        onde um segmento do pai1 é copiado para o filho, e o restante é preenchido na 
        ordem em que aparecem no pai2, garantindo que o filho seja uma permutação válida.
    """
    def gerar_filhos(pai1, pai2):
        tamanho_pais = len(pai1)                                        # Guarda o tamanho do indivíduo pai. Como os pais tem o mesmo tamanho, tanto faz usar pai1 ou pai2
        corte1, corte2 = sorted(random.sample(range(tamanho_pais), 2))  # Seleciona 2 índices da lista dos pais para ser o segmento do filhos
        filho1 = [None] * tamanho_pais                                  # Cria o indivíduo filho como os elementos vazios
        filho2 = [None] * tamanho_pais

        filho1[corte1:corte2+1] = pai1[corte1:corte2+1]     # Insere o segmento retirado do pai 1 nas mesmas posições no filho 1
        filho2[corte1:corte2+1] = pai2[corte1:corte2+1]     # Insere o segmento retirado do pai 2 nas mesmas posições no filho 2
        
        pos_filho = (corte2 + 1) % tamanho_pais             # Define o ponto de partida (1 índice depois do segmento) para inserir os elementos do pai 2 no filho 1
        pos_pai_fill = (corte2 + 1) % tamanho_pais
        # Repete enquanto o indivíduo filho estiver com elementos vazios
        while None in filho1:
            cidade = pai2[pos_pai_fill]
            if cidade not in filho1:
                filho1[pos_filho] = cidade                  # Insere o elemento de pai 2 na posição do filho 1
                pos_filho = (pos_filho + 1) % tamanho_pais
            pos_pai_fill = (pos_pai_fill + 1) % tamanho_pais

        while None in filho2:
            cidade = pai1[pos_pai_fill]
            if cidade not in filho2:
                filho2[pos_filho] = cidade                  # Insere o elemento de pai 1 na posição do filho 2
                pos_filho = (pos_filho + 1) % tamanho_pais
            pos_pai_fill = (pos_pai_fill + 1) % tamanho_pais
        return filho1, filho2

    filhos = gerar_filhos(pai1, pai2)
    return filhos

def mutacao_swap(solucao):
    """
        Modificação do indivíduo gerado onde seleciona-se 2 índices e troca os valores deles.
        O elemento da posição X vai para a posição Y e o elemento da posição Y vai para a posição X
    """
    tamanho_filho = len(solucao)
    i, j = random.sample(range(tamanho_filho), 2)
    solucao[i], solucao[j] = solucao[j], solucao[i]
    return solucao

def busca_local_2opt(solucao, distancias):
    """
    Procura pela melhoria local usando o método 2-opt, que tenta melhorar a solução atual invertendo segmentos do caminho 
    e verificando se isso reduz o custo total, continuando a busca até que nenhuma melhoria seja encontrada.
    """
    tamanho_filho = len(solucao)
    melhor_solucao = list(solucao)
    melhor_custo = custo_caminho(melhor_solucao, distancias)            # Guarda o custo atual do filho
    melhorou = True
    while melhorou:
        melhorou = False
        # Percorre toda o filho setando ponteiros para os índices
        for i in range(tamanho_filho):
            for j in range(i + 2, tamanho_filho):
                index_i, index_i_plus = i, (i + 1) % tamanho_filho      # Guarda o índice da cidade i e a próxima cidade ao qual está ligado
                index_j, index_j_plus = j, (j + 1) % tamanho_filho      # Guarda o índice da cidade j e a próxima cidade ao qual está ligado
                if index_j_plus == index_i: continue
                a, b = melhor_solucao[index_i], melhor_solucao[index_i_plus]
                c, d = melhor_solucao[index_j], melhor_solucao[index_j_plus]
                custo_atual = distancias[(a, b)] + distancias[(c, d)]   # Calcula somente a soma dos índices com sua próxima cidade
                novo_custo = distancias[(a, c)] + distancias[(b, d)]    # Calcula a soma dos índices trocados com as próximas cidades
                if novo_custo < custo_atual:
                    melhor_solucao[i+1 : j+1] = melhor_solucao[i+1 : j+1][::-1] # Inverte o trecho encontrado que reduz o custo do filho
                    melhor_custo -= (custo_atual - novo_custo)          # Subtrai a diferença de custo
                    melhorou = True
                    break
            if melhorou: break
    return melhor_solucao

def selecionar_sobreviventes_steady_state(populacao, filhos, distancias, tamanho_populacao):
    """
    Seleção de Sobreviventes (Steady-State com mesclagem Pop + Filhos)
    Mescla a população e os filhos, ordena por custo (minimização),
    e seleciona os melhores indivíduos para formar a nova população,
    garantindo que o melhor indivíduo do conjunto seja sempre preservado.
    Evita indivíduos duplicados na população para manter a diversidade.
    """
    pool_completo = populacao + filhos
    # Ordena pelo custo (menor custo primeiro)
    pool_ordenado = sorted(pool_completo, key=lambda individuo: custo_caminho(individuo, distancias))
    
    nova_populacao = []
    for individuo in pool_ordenado:
        if individuo not in nova_populacao:
            nova_populacao.append(individuo)
        if len(nova_populacao) == tamanho_populacao:
            break
            
    # Caso haja duplicados extremos e não preencha a população
    if len(nova_populacao) < tamanho_populacao:
        for individuo in pool_ordenado:
            if len(nova_populacao) == tamanho_populacao:
                break
            nova_populacao.append(individuo)
            
    return nova_populacao

# --------------------------------------------------------
#                    EXECUÇÃO PRINCIPAL
# ---------------------------------------------------------

if __name__ == "__main__":
    TAMANHO_POPULACAO = 100
    N_GERACOES = 1000
    PROB_BUSCA_LOCAL = 0.3
    TAXA_MUTACAO = 0.2
    ARQUIVO_DADOS = "edgesbrasil58.tsp"
    
    # Configuração do método de seleção de pais: "torneio" ou "roleta"
    METODO_SELECAO_PAIS = "torneio"  # altere para "roleta" se desejar
    
    distancias = carregar_distancias(ARQUIVO_DADOS)
    populacao = inicializar_populacao(TAMANHO_POPULACAO, 58)
    
    melhor_inicial = min([custo_caminho(individuo, distancias) for individuo in populacao]) # Guarda o melhor indivíduo da população inicial
    print(f"Melhor inicial: {melhor_inicial}")
    print(f"Iniciando AG V3 (Seleção de Pais: {METODO_SELECAO_PAIS.upper()} | Sobreviventes: Steady-State com Mesclagem)...")

    for geracao in range(N_GERACOES):
        # Seleção dos pais (usando o método configurado)
        pai1 = selecionar_pai(populacao, distancias, metodo=METODO_SELECAO_PAIS)
        # Garante que não se tenha 2 pais iguais
        while True:
            pai2 = selecionar_pai(populacao, distancias, metodo=METODO_SELECAO_PAIS)
            if pai2 != pai1:
                break
        
        # Cruzamento Crossover (OX) - Gera dois filhos
        filhos = crossover_ox(pai1, pai2)
        
        filhos_processados = []
        for filho in filhos:
            # Mutação dos filhos com 20% de acontecer
            if random.random() < TAXA_MUTACAO:
                filho = mutacao_swap(filho)
            
            # Melhoria local com 2-opt com 30% de acontecer
            if random.random() < PROB_BUSCA_LOCAL:
                filho = busca_local_2opt(filho, distancias)
                
            filhos_processados.append(filho)
            
        # Seleção de sobreviventes (Steady-state: mesclar população + filhos e selecionar os melhores)
        populacao = selecionar_sobreviventes_steady_state(populacao, filhos_processados, distancias, TAMANHO_POPULACAO)
        
        if (geracao + 1) % 100 == 0:
            custos = [custo_caminho(individuo, distancias) for individuo in populacao]
            print(f"Geração {geracao+1:4}: Melhor = {min(custos)} | Média = {sum(custos)/len(custos):.1f}")

    custos_finais = [custo_caminho(individuo, distancias) for individuo in populacao]
    melhor_final = min(custos_finais)
    idx_melhor = custos_finais.index(melhor_final)
    melhor_rota = populacao[idx_melhor]
    
    print(f"\nMelhor Inicial: {melhor_inicial}")
    print(f"Melhor Final:   {melhor_final}")
    print(f"Melhor Rota:    {melhor_rota}")
