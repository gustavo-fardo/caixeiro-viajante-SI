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

def calcula_custo(cidades, n_cidades, solucao):
    custo = 0
    for i in range(1, n_cidades):
        custo+=cidades[solucao[i]][solucao[i-1]]
    return custo

def retornaTemp(t, max_iter):
    return 100*((max_iter-t)/max_iter)**2

def temperaSimulada(cidades, n_cidades, sol_inicial, max_iter):
    solucao_atual = sol_inicial
    custo_atual = calcula_custo(cidades, n_cidades, solucao_atual)
    for t in range(max_iter):
        T = retornaTemp(t, max_iter)
        if T == 0:
            return solucao_atual
        prox_solucao = gera_solucao(n_cidades)
        # print(f"solucao atual:{solucao_atual}")
        print(f"custo atual:{custo_atual}")
        # print(f"solucao vizinha:{prox_solucao}")
        prox_custo = calcula_custo(cidades, n_cidades, prox_solucao)
        print(f"custo vizinho:{prox_custo}")
        delta_custos = custo_atual - prox_custo
        print(f"delta:{delta_custos}")
        if delta_custos > 0:
            print("MELHOR")
            solucao_atual = prox_solucao
            custo_atual = prox_custo
        else:
            rand = random.random() 
            prob = math.e**(delta_custos/T)
            if rand < prob:
                print(f"PIOR COM PROB {rand} contra {prob}")
                solucao_atual = prox_solucao
                custo_atual = prox_custo
    return solucao_atual

n_cidades = 20

cidades = cria_cidades(n_cidades)

s = gera_solucao(n_cidades)
print(s)
custo = calcula_custo(cidades, n_cidades, s)
print(custo)

sf = temperaSimulada(cidades, n_cidades, s, max_iter=100)
print(sf)
print(calcula_custo(cidades, n_cidades, sf))