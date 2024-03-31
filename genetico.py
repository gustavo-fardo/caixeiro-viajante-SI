import numpy as np
import random
import math

class Genetico:
    def __init__(
            self,
            n_populacao = 12,
            max_geracoes = 1000,
            k_roleta = 6,
            p_cross = 0.8,
            p_mut = 0.05
            ):
        n_cidades = 10
        print("Matrix de Cidades:")
        cidades = self.cria_cidades(n_cidades)

        populacao = []
        custo_i = []

        print("Cromossomos:")
        for i in range (n_populacao):
            individuo = self.gera_solucao(n_cidades)

            populacao.append(individuo)
            custo_i.append(self.calcula_custo(cidades, individuo))
            print(individuo)
        
        geracao = 0

        print("Custos:")
        print(custo_i)

        self.populacao = populacao
        self.custo_i = custo_i

        individuo =self.roleta(self)
        # print(f"Solucao inicial: {si}")

        
        # sib = self.binariza_solucao(si)
        # print(f"Solucao inicial binarizada: {sib}")

        # self.binariza_solucao([5,15])

    def cria_cidades(self, num_cidades):
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

    def gera_solucao(self, n_cidades):
        sol = np.random.permutation(n_cidades)
        return np.append(sol, sol[0])

    def calcula_custo(self, cidades, solucao):
        custo = 0
        for i in range(1, len(solucao)):
            custo+=cidades[solucao[i]][solucao[i-1]]
        return custo

    def roleta(self):
        custos = self.custo_i

        c_total = 0

        for custo in custos:
            c_total += custo        

    def binariza_solucao(self, solucao):
        
        solucao_binarizada = []

        for i in range(len(solucao)):
            binarizado = []            
            atual = solucao[i]

            while atual != 0:
                binarizado.insert(0, atual%2)
                atual = atual // 2

            while len(binarizado) < 4:
                binarizado.insert(0, 0)

            solucao_binarizada.append(binarizado)

        return solucao_binarizada


genetico = Genetico()