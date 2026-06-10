![Static Badge](https://img.shields.io/badge/Conclu%C3%ADdo-229922?style=for-the-badge)

# 🚚 Flyfood - Otimização de Rotas para Drones Autônomos via Algoritmos Meméticos

O **FlyFood** é um projeto de otimização logística focado em entregas autônomas via drones. Ele resolve o clássico Problema do Caixeiro Viajante (*Traveling Salesman Problem* - TSP) aplicado ao contexto de entregas em matrizes esparsas. Como o TSP é classificado como **NP-difícil**, a busca exaustiva (força bruta) torna-se computacionalmente inviável conforme o número de destinos cresce.

Para superar essa barreira de escalabilidade, o projeto evoluiu de uma solução de busca exaustiva para uma abordagem baseada em **Algoritmos Meméticos** (Algoritmo Genético combinado com a meta-heurística de Busca Local 2-opt). Essa combinação permite obter soluções de altíssima qualidade (geralmente idênticas às ótimas) em frações de segundo, mesmo para grandes volumes de cidades.

---

## 📌 Características Técnicas

- **Métrica de Manhattan:** Utiliza a *Distância de Manhattan* para medir o custo de deslocamento entre os pontos de entrega na matriz, respeitando as limitações físicas de voo dos drones em eixos ortogonais:

$$d(P_1, P_2) = | x_1 - x_2 | + | y_1 - y_2 |$$

- **Algoritmo Genético (AG):** Explora o espaço de busca globalmente simulando a seleção natural. Ele mantém uma população de rotas representadas como permutações de cidades que passam por processos de seleção de pais, cruzamento (*crossover*) e mutação ao longo de várias gerações.
- **Busca Local (2-opt) - O Toque Memético:** Refina as rotas individuais encontradas pelo AG. O operador 2-opt remove auto-interseções e caminhos ineficientes invertendo segmentos da rota de forma iterativa, garantindo a "lapidação" da melhor solução local.
- **Estrutura de Rota:** O ponto de partida e de retorno é sempre a base de recarga e carregamento designada por **R**. A saída do algoritmo exibe a sequência de entrega omitindo o ponto **R** nos resultados intermediários para legibilidade.

---

## 📈 Evolução do Algoritmo (V1 ➔ V2 ➔ V3)

O algoritmo evoluiu através de três versões principais na pasta [genetic_alg](./genetic_alg) para combater a convergência prematura e maximizar a diversidade populacional:

| Funcionalidade / Parâmetro | [Memético V1](./genetic_alg/memetico_V1.py) (Básico) | [Memético V2](./genetic_alg/memetico_V2.py) (Diversidade) | [Memético V3](./genetic_alg/memetico_V3.py) (Otimizado) |
| :--- | :--- | :--- | :--- |
| **Tamanho da População** | 10 indivíduos | 20 indivíduos | 200 indivíduos |
| **Gerações** | 500 | 1000 | 2500 |
| **Inicialização** | Permutações aleatórias comuns | Apenas indivíduos únicos (sem duplicatas) | Apenas indivíduos únicos (sem duplicatas) |
| **Seleção de Pais** | Roleta baseada na aptidão inversa ($1/\text{custo}$) | Torneio ($k=3$) para atenuar pressão seletiva | Escolha entre Torneio Binário ($k=2$) ou Roleta |
| **Crossover** | Order Crossover (OX) - Gera 1 filho | Order Crossover (OX) - Gera 2 filhos (inverte papéis) | Order Crossover (OX) - Gera 2 filhos |
| **Mutação** | Swap (10% de chance) | Swap (20% de chance) | Swap ou Inversão de Segmento (35% de chance) |
| **Busca Local (2-opt)** | Aplicado a 100% dos indivíduos | Aplicado probabilisticamente (30% de chance) | Aplicado probabilisticamente (15% de chance) |
| **Sobrevivência** | Substitui pior se o filho for estritamente melhor | Substitui pior, bloqueando entrada de duplicatas | *Steady-State* com mesclagem global e eliminação de duplicados |

---

## 🖥️ Estrutura do Repositório

```text
flyfood
┣ 📂 forca_bruta                  # Versão legada por força bruta
┃ ┣ 📄 forca_bruta.py             # Algoritmo exaustivo com poda (O(n!))
┃ ┗ 📄 matriz5.txt a matriz14.txt # Casos de teste originais
┣ 📂 genetic_alg                  # Nova versão com Algoritmo Genético/Memético
┃ ┣ 📄 memetico_V1.py             # Versão conceitual básica
┃ ┣ 📄 memetico_V2.py             # Versão com melhor controle de diversidade
┃ ┣ 📄 memetico_V3.py             # Versão otimizada de alta performance
┃ ┣ 📄 comparar_algoritmos.py     # Script que compara AG V3 contra a Força Bruta
┃ ┣ 📄 lerBrasil58.py             # Utilitário de carregamento do dataset Brazil58
┃ ┣ 📄 brazil58.tsp               # Arquivo TSPLIB com distâncias explícitas de 58 cidades brasileiras
┃ ┣ 📄 edgesbrasil58.tsp          # Matriz de adjacência formatada para o Brazil58
┃ ┗ 📄 matriz5_distances.txt a matriz14_distances.txt # Tabelas de distâncias convertidas das matrizes
┗ 📄 README.md                    # Documentação principal (você está lendo agora)
```

---

## ⚡ Resultados: Força Bruta vs. Algoritmo Genético (V3)

A tabela abaixo exibe a comparação prática entre a busca exaustiva (Força Bruta) e o Algoritmo Memético V3 rodando nas matrizes de teste originais:

| Entrada | Qtd. Cidades | Tempo Força Bruta | Custo FB | Tempo AG (V3) | Custo AG | Diferença vs. FB |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `matriz5.txt` | 5 | 0.0003s | 18 | ~1.2s | 18 | **0.00%** (Ótimo) |
| `matriz8.txt` | 8 | 0.0449s | 24 | ~1.2s | 24 | **0.00%** (Ótimo) |
| `matriz10.txt` | 10 | 3.7273s | 30 | ~1.3s | 30 | **0.00%** (Ótimo) |
| `matriz11.txt` | 11 | 32.7921s | 30 | ~1.3s | 30 | **0.00%** (Ótimo) |
| `matriz12.txt` | 12 | 7.38 min (442.89s) | 34 | ~1.4s | 34 | **0.00%** (Ótimo) |
| `matriz13.txt` | 13 | 2.11 horas (7618.07s) | 34 | ~1.5s | 34 | **0.00%** (Ótimo) |
| `matriz14.txt` | 14 | 25.12 horas (90456.31s)| 50 | **~1.6s** | 50 | **0.00%** (Ótimo) |

> [!TIP]
> **Ganho de Escala:** Para a `matriz14.txt`, o Algoritmo Genético V3 reduziu o tempo de execução de **mais de 25 horas para apenas 1.6 segundos**, mantendo a precisão absoluta de 100% (erro de 0.00% em relação à rota ótima global).

---

## 🚀 Como Executar o Código

### Pré-requisitos
Certifique-se de ter o Python 3 instalado no sistema. Não são necessárias bibliotecas externas adicionais (usa apenas módulos padrão como `random`, `time`, `sys` e `os`).

### 1. Clonar o repositório
```bash
git clone https://github.com/lucasmenezes255/flyfood.git
cd flyfood
```

### 2. Executar e Comparar Algoritmos (Matrizes de 5 a 14 cidades)
Para rodar a ferramenta de comparação que executa o AG V3 (com Seleções por Torneio e Roleta) contra os tempos registrados da força bruta, navegue até a pasta `genetic_alg` e forneça o nome do arquivo da matriz como argumento:
```bash
cd genetic_alg
python comparar_algoritmos.py matriz14.txt
```

### 3. Executar o AG V3 na base de dados nacional (Brazil58 - 58 Cidades)
Para testar a capacidade do Algoritmo Memético V3 em larga escala com um problema de 58 cidades (onde o espaço de busca excede $10^{70}$ rotas possíveis), execute:
```bash
python memetico_V3.py
```
O algoritmo imprimirá o melhor custo encontrado a cada 100 gerações, finalizando com a exibição do caminho indexado de 58 cidades e custo mínimo aproximado (geralmente convergindo para ~25.395).

---

## 👥 Créditos

Este projeto foi desenvolvido e mantido por:
- **Bruno Fellype de Santana Vieira** - [GitHub](https://github.com/BrunoFellype)
- **Isaque Lucas Pedrosa Velozo** - [GitHub](https://github.com/BlairFruit)
- **Lucas Menezes dos Santos** - [GitHub](https://github.com/lucasmenezes255)
- **Renato Henrique Barros** - [GitHub](https://github.com/renatobbarros)
