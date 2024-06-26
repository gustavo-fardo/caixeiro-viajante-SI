import numpy as np
import random
import math

def cria_cidades(num_cidades):

    cidades = []
    for i in range(num_cidades):
        adj_cidade = []
        for i in range(num_cidades):
            adj_cidade.append(0)
        cidades.append(adj_cidade)

    for i in range(num_cidades):
        j = 0
        while j < i:
            rand_dist = random.randint(1, 10)
            cidades[i][j] = rand_dist
            cidades[j][i] = rand_dist
            j+=1

    for i in range(num_cidades):
        print(cidades[i])

    return cidades

def gera_solucao(n_cidades):
    sol = np.random.permutation(n_cidades)
    return np.append(sol, sol[0])

def calcula_custo(cidades, solucao):
    custo = 0
    for i in range(1, len(solucao)):
        custo+=cidades[solucao[i]][solucao[i-1]]
    return custo

def retornaTemp(t, max_iter):
    return 100*((max_iter-t)/max_iter)**2

def temperaSimulada(cidades, sol_inicial, max_iter):
    solucoesnotempo = []
    solucao_atual = sol_inicial
    custo_atual = calcula_custo(cidades, solucao_atual)
    for t in range(max_iter):
        solucoesnotempo.append(solucao_atual)
        T = retornaTemp(t, max_iter)
        if T == 0:
            return solucao_atual
        prox_solucao = gera_solucao(np.shape(cidades)[0])
        # print(f"solucao atual:{solucao_atual}")
        # print(f"custo atual:{custo_atual}")
        # print(f"solucao vizinha:{prox_solucao}")
        prox_custo = calcula_custo(cidades, prox_solucao)
        # print(f"custo vizinho:{prox_custo}")
        delta_custos = custo_atual - prox_custo
        # print(f"delta:{delta_custos}")
        if delta_custos > 0:
            # print("MELHOR")
            solucao_atual = prox_solucao
            custo_atual = prox_custo
        else:
            rand = random.random() 
            prob = math.e**(delta_custos/T)
            if rand < prob:
                # print(f"PIOR COM PROB {rand} contra {prob}")
                solucao_atual = prox_solucao
                custo_atual = prox_custo
    return solucoesnotempo