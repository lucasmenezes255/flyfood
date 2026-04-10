[![Static Badge](https://img.shields.io/badge/Python-0F3978?style=for-the-badge)](https://github.com/lucasmenezes255)

# 🚚 Flyfood - Otimização de Rotas
Algoritmo em Python criado para solucionar o problema do Caxeiro Viajante, um problema clássico de Grafos de complexidade **$`O(n!)`$**, classificado como NP-difícil, pois a solução exata do problema é computacionalmente inviável conforme o número de cidades cresce.

A ideia principal é usar esse código para fazer com que um drone de entrega de comida calcule a rota mais eficiente, de menor custo dentro das cidades onde precisa fazer entrega.

Para abstração do problema, as cidades estão dispostas em uma matriz esparsa, onde o ponto *`R`* sempre será o ponto de partida e retorno da rota do drone. O objetivo é calcular a menor *Distância Manhattan* percorrendo todas as cidades da matriz e retornando ao ponto *`R`* 

## 📌 Fase 1 - Força Bruta
O código do cálculo da menor Distância Manhattan por força bruta é um algoritmo simples em sua essência, porém inviável conforme o número de cidades aumenta.

> O Programa deve encontrar todas as rotas possíveis na matriz: $n!$<br> E compara uma a uma o tamanho das rotas entre si em busca da rota de menor tamanho. Quando encontra a menor rota, deve retornar a sequência de cidades que o drone deverá seguir para ser mais eficiente.

- Exemplo de Entrada do programa:
```text
   4 5
   0 0 0 0 D
   0 A 0 0 0
   0 0 0 0 C
   R 0 B 0 0
```
A partir disso, o programa deve calcular a menor rota partindo de *`R`* e retornar essa rota onde o ponto *`R`* pode ser omitido:

```text
    B C D A
```
### 🚩 Problema da força bruta
Esse algoritmo chega no limite de processamento da máquina de forma muito rápida, pois precisa de todas as $n!$ permutações de cidade para encontrar a menor. Amostra de crescimento do problema:

- Com 6 cidades: $6! = 720$ possíveis rotas
- Com 7 cidades: $7! = 5040$ possíveis rotas
- Com 8 cidades: $8! = $40.320$ possíveis rotas
- Com 9 cidades: $9! = 362.880$ possíveis rotas
- Com 10 cidades: $10! = 3.628.800$ possíveis rotas