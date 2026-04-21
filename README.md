![Static Badge](https://img.shields.io/badge/Conclu%C3%ADdo-229922?style=for-the-badge)

# 🚚 Flyfood - Otimização de rotas para drones autônomos 
O FlyFood é um projeto de otimização logística focado em entregas autônomas via drones. Sendo concretizado a partir de um algoritmo em Python criado para solucionar o problema do Caxeiro Viajante - *Traveling Salesman Problem*, um problema clássico de Grafos, ao qual o FlyFood é uma derivação direta, classificado como um problema NP-difícil, pois a solução exata do problema é computacionalmente inviável conforme o número de cidades cresce.

⚠️ *Nota: Este algoritmo utiliza busca exaustiva com complexidade **O(n!)**, garantindo a solução ótima absoluta.*

A ideia principal é usar esse código para fazer com que um drone de *delivery* calcule a rota mais eficiente, de menor custo dentro das cidades onde precisa fazer entrega através do método conhecido como **força bruta** ou **busca exaustiva**.


## 📌 Características Técnicas
Para abstração do problema, as cidades estão dispostas em uma matriz esparsa, onde o ponto *$R$* sempre será o ponto de partida e retorno da rota do drone. O objetivo é calcular a menor rota percorrendo todas as cidades da matriz e retornando ao ponto *$R$*.

- **Métrica de Manhattan:** Utiliza a *Distância de Manhattan* para calcular a distância entre as cidades, respeitando as limitações físicas de voo do drone nos eixos ortogonais.

$$d(P_1, P_2) = | x_1 - x_2 | + | y_1 - y_2 |$$

- **Força bruta:** O Programa deve encontrar todas as rotas possíveis na matriz: $n!$ e compara uma a uma o tamanho das rotas entre si em busca da rota de menor tamanho. Quando encontra a menor rota, deve retornar a sequência de cidades que o drone deverá seguir para ser mais eficiente.

- **PODA (AKA Pruning):** O algoritmo possui um sistema inteligente de poda que interrompe o cálculo de uma rota no meio do caminho caso sua distância acumulada já seja maior que a menor rota já analisada, poupando operações computacionais.

- **Teste automatizado:** Inclui uma maneira automatica de testar as matrizes, indo de uma maneira crescente com a opção de cancelar a operação do codigo.


### 🚩 Problema da força bruta
Esse algoritmo chega no limite de processamento da máquina de forma muito rápida, pois precisa de todas as $n!$ permutações de cidade para encontrar a menor. Amostra de crescimento do problema:

- Com 5 cidades: $5! = 120$ possíveis rotas
- Com 8 cidades: $8! = 40.320$ possíveis rotas
- Com 10 cidades: $10! = 3.628.800$ possíveis rotas
- Com 11 cidades: $11! = 39.916.800$ possíveis rotas
- Com 12 cidades: $12! = 479.001.600$ possíveis rotas
- Com 13 cidades: $13! = 6.2287.020.800$ possíveis rotas
- Com 14 cidades: $14! = 87.178.291.200$ possíveis rotas

### Artigo - Otimização de rotas para drones: Abordagem via força bruta para o problema do FlyFood

Para informações mais detalhadas e profundas acerca da construção do algoritmo, motivações do projeto, metodologia adotada e análise de resultados, você pode ler o artigo criado pelos desenvolvedores através [deste link](https://drive.google.com/file/d/10tGLSzvwy_PMY2b05rffMeQMUTbtC5Ss/view?usp=drive_link) ou acessando o arquivo *FlyFood.pdf* no repositório

---
### 🖥️ Interface do algoritmo
```text
input

    6 6
    R 0 0 A 0 B
    0 0 0 0 0 0
    0 C 0 0 D 0
    0 0 0 0 0 0
    E 0 0 F 0 G
    0 0 0 0 0 H
```
A partir disso, o programa deve calcular a menor rota partindo de *$R$* e retornar essa rota onde o ponto *$R$* pode ser omitido, além de retornar o tamanho da rota e o custo que ela teve:

```text
output

    Menor rota: A B D G H F E C

    Tamanho da rota: 24

    Demorou: 0.03 segundos
```

### 🔹 Estrutura do Repositório
```text
flyfood
┣ forca_bruta.py           # Arquivo principal com o algoritmo de roteamento
┣ matriz5.txt a matriz14.txt # Conjunto de dados de teste (5 a 14 cidades)
┣ README.md # Você esta lendo ele agora.
```

### 🔹 Clonar o repositório e executar o código
1. Clone o repositório

```
git clone https://github.com/lucasmenezes255/flyfood.git
```

2. Entre na pasta do projeto

```
cd flyfood
```

3. Execute o código python

```
python forca_bruta.py
```

# Créditos
- **Bruno Fellype de Santana Vieira** - [GitHub](https://github.com/BrunoFellype)
- **Isaque Lucas Pedrosa Velozo** - [GitHub](https://github.com/BlairFruit)
- **Lucas Menezes dos Santos** - [GitHub](https://github.com/lucasmenezes255)
- **Renato Henrique Barros** - [GitHub](https://github.com/renatobbarros)