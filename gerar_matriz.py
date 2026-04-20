import random
import sys

def gerar(n, m, num_cidades):
    matriz = [['0' for _ in range(m)] for _ in range(n)]
    
    letras = [chr(i) for i in range(ord('A'), ord('Z')+1)]
    letras.remove('R') 
    random.shuffle(letras)
    
    # ESTA ERA A LINHA QUE TINHA SUMIDO!
    cidades_selecionadas = letras[:num_cidades]
    
    r_i, r_j = random.randint(0, n-1), random.randint(0, m-1)
    matriz[r_i][r_j] = 'R'
    
    posicoes_ocupadas = {(r_i, r_j)}
    for cidade in cidades_selecionadas:
        while True:
            i, j = random.randint(0, n-1), random.randint(0, m-1)
            if (i, j) not in posicoes_ocupadas:
                matriz[i][j] = cidade
                posicoes_ocupadas.add((i, j))
                break

    print(f"{n} {m}")
    for linha in matriz:
        print(" ".join(linha))

if __name__ == "__main__":
    num_cidades = 6
    if len(sys.argv) > 1:
        num_cidades = int(sys.argv[1])
    
    tamanho_matriz = max(5, (num_cidades // 2) + 2)
    
    gerar(n=tamanho_matriz, m=tamanho_matriz, num_cidades=num_cidades)