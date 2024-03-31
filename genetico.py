import numpy as np
import random
import math

tipos_mutacoes = ["posicao", "ordem", "embaralhamento"]

# FAVOR AJUSTAR PARAMETROS NA LINHA 261 E NAO OS DEFAULT

class Genetico:
    def __init__(
            self,
            n_populacao = 6,
            r_descendentes = 6,
            max_geracoes = 1000,
            p_cross = 0.8,
            p_mut = 0.05,
            i_mut = 2 # default mutacao por posicao
            ):

        n_cidades = 10
        print("Matrix de Cidades:")
        cidades = self.cria_cidades(n_cidades)

        populacao = []        
        for i in range (n_populacao):
            individuo = self.gera_solucao(n_cidades)
            populacao.append(individuo)

        geracao = 0

        while (geracao < max_geracoes):

            print("Pais:")
            pais = populacao.copy()
            for pai in pais:
                print(pai)
            
            print("Custos:")
            custos = []
            for pai in pais:
                custos.append(self.calcula_custo(cidades, pai))
            print(custos)

            print("Fitness:")
            fitness = self.fitness(custos)
            print(fitness)

            print("Selecionados:")
            selecionados = self.roleta(r_descendentes, fitness, n_populacao, pais)

            print("Cruzados:")
            cruzados = self.cruzamento(selecionados, p_cross)

            print("Mutados:")
            mutados = self.mutacao(cruzados, p_mut, i_mut)

            print("Melhores:")
            populacao = self.seleciona_melhores(cidades, pais, mutados, n_populacao)
        
            geracao += 1
        

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

    def fitness(self, custos):
        fitness = []
        c_total = 0

        for custo in custos:
            c_total += custo

        # a função fit usada 
        for custo in custos:
            f = 1 - (custo/c_total)
            fitness.append(f)

        return fitness

    def calcula_custo(self, cidades, solucao):
        custo = 0
        for i in range(1, len(solucao)):
            custo+=cidades[solucao[i]][solucao[i-1]]
        return custo

    def roleta(self, r_descendentes, fitness, n_populacao, populacao):
        f_total = n_populacao - 1
        p_sol = []

        for f in fitness:
            p_sol.append(f/f_total)

        selecionados = []

        for i in range (r_descendentes):
            selecionado = self.seleciona_roleta(p_sol, populacao)
            selecionados.append(selecionado)
            print(selecionado)

        return selecionados

    def seleciona_roleta(self, p_sol, populacao):
        i = 0
        soma = p_sol[i] 

        r = random.random()

        while soma < r:
            i += 1
            soma += p_sol[i] 
        
        return populacao[i]
    
    def cruzamento(self, selecionados, p_cross):
        n_populacao = len(selecionados)

        i = 0

        cruzados = []

        while(i < n_populacao):
            r = random.random()
            d1 = selecionados[i]
            d2 = selecionados[i+1]

            if (r < p_cross):
                self.cruzar(d1, d2)

            cruzados.append(d1)
            cruzados.append(d2)
            i += 2

            print(d1)
            print(d2)
        
        return cruzados
        

    def cruzar(self, d1, d2):
        tam = len(d1)

        p_i = random.randint(0,tam-3)
        p_j = random.randint(p_i,tam-2)

        M_12 = {}
        M_21 = {}

        for i in range (p_i, p_j+1):
            M_12[d1[i]] = d2[i]
            M_21[d2[i]] = d1[i]

            d1[i] = M_12[d1[i]]
            d2[i] = M_21[d2[i]]

        self.remove_duplicatas(d1, M_21, p_i, p_j, tam)
        self.remove_duplicatas(d2, M_12, p_i, p_j, tam)
            
    def remove_duplicatas(self, d, M, p_i, p_j, tam):
        while len(d[0:-1]) != len(set(d[0:-1])):
            for i in range (0,p_i):
                if d[i] in M:
                    d[i] = M[d[i]]
            for i in range (p_j+1,tam-1):
                if d[i] in M:
                    d[i] = M[d[i]]

        d[tam-1] = d[0]

    def mutacao(self, cromossomos, p_mut, i_mut):
        for i in range(len(cromossomos)):
            cromossomos[i] = self.mutar(list(cromossomos[i]), p_mut, i_mut)
            print(cromossomos[i])

        return cromossomos

    def mutar(self, cromossomo, p_mut, i_mut):
        tam = len(cromossomo)
        mutacao = tipos_mutacoes[i_mut]

        if mutacao == "posicao":
            cromossomo = self.muta_posicao(cromossomo, p_mut, tam)
            cromossomo[tam-1] = cromossomo[0]
        elif mutacao == "ordem":
            cromossomo = self.muta_ordem(cromossomo, p_mut, tam)
            cromossomo[tam-1] = cromossomo[0]
        else:
            cromossomo = self.muta_embaralhamento(cromossomo, p_mut, tam)
            cromossomo[tam-1] = cromossomo[0]
        
        return cromossomo
        
    def muta_posicao(self, cromossomo, p_mut, tam):
        for i in range(tam - 2):
            r = random.random()
            if r < p_mut:
                j = random.randint(i+1, tam - 2)
                cromossomo.insert(j, cromossomo[i])
                cromossomo.remove(cromossomo[i])
        return cromossomo
    
    def muta_ordem(self,cromossomo,  p_mut, tam):
        for i in range(tam - 2):
            r = random.random()
            if r < p_mut:
                j = random.randint(i+1, tam - 2)
                aux = cromossomo[i]
                cromossomo[i] = cromossomo[j]
                cromossomo[j] = aux
        return cromossomo
    
    def muta_embaralhamento(self, cromossomo, p_mut, tam):
        for i in range(tam - 2):
            r = random.random()
            if r < p_mut:
                j = random.randint(i+1, tam - 2)
                sublist = cromossomo[i:j+1]
                random.shuffle(sublist)
                cromossomo[i:j+1] = sublist
        return cromossomo

    def seleciona_melhores(self, cidades, pais, filhos, n_populacao):
        custos = []
        uniao = pais + filhos
        melhores = []

        for cromossomo in uniao:
            custo = self.calcula_custo(cidades, cromossomo)
            custos.append(custo)

        c_ordenados = custos.copy()
        c_ordenados.sort()
        for i in range (0, n_populacao):
           index = custos.index(c_ordenados[i])
           melhores.append(uniao[index])
           print(str(c_ordenados[i]) + ": "+ str(uniao[index]))

        return melhores

genetico = Genetico(
    n_populacao=16,
    r_descendentes=16,
    max_geracoes=1000,
    p_cross= 0.8,
    p_mut=0.05,
    i_mut=2
)