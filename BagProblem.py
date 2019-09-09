import pandas as pd
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import time
from matplotlib import style
style.use('fivethirtyeight')

dt = pd.read_excel('Tabela_Artigos.xls')
itemMatrix = dt.values

class Bag:

    def __init__(self, itens):
        self.itens = itens
        self.fitness = int(0)
        self.vlTotal, self.peso, self.volume = 0, 0, 0
        
    def __repr__(self):
        return f'fitness:{self.fitness}, Itens:{self.itens} Valor/Peso/Volume: {self.vlTotal}/{self.peso}/{self.volume}'
    
    def calculateFitness(self, elitista):
        vlT, p, v = 0, 0, 0
        for i in range(25):
            if self.itens[i] == 1:
                vlT = vlT + itemMatrix[i][3]
                p = p + itemMatrix[i][2]
                v = v + itemMatrix[i][1]
        
        #A cada ponto acima do limite de peso ou volume é descontada como porcentagem do valor do item.
        if v > 125:
            vlT = vlT - (vlT * ((v-125) / 100))
        if p > 125:
            vlT = vlT - (vlT * ((p-125) / 100))
        self.fitness = vlT
        
        #Variaveis informativas
        self.peso = p
        self.vlTotal = vlT
        self.volume = v
        return self.fitness
        
    def doMutation(self):
        i = 5
        while i >= 0:
            randIndex = np.random.randint(0,25)
            if self.itens[randIndex] == 0:
                self.itens[randIndex] = 1
            else:
                self.itens[randIndex] = 0
            i -= 1
            
def initPopulation(size):
    pop = []
    while size >= 0:
        a = np.random.randint(low=0,high=2,size=25)
        pop.append(Bag(a.tolist()))
        size -= 1
    stop = time.perf_counter()
    return np.array(pop)

def calculatePopFitness(pop):
    global theBest, theBestFromGen
    for bag in pop:
        fit = bag.calculateFitness(False)
        if fit > theBestFromGen.fitness:
            theBestFromGen = copy.copy(bag)
    return pop
        
def naturalSelection(pop,numToSelection):
    max = sum([bag.fitness for bag in pop])
    selection_probs = [bag.fitness/max for bag in pop]
    felizardos = pop[np.random.choice(len(pop),size=numToSelection,replace = False, p=selection_probs)]
    return felizardos

def iniciaCrossover(pop):
    toProcriate = pop[np.random.choice(len(pop),size=round(len(pop)* 0.8),replace = False)]
    for i in range(0,len(toProcriate),2):
        bag1, bag2 = toProcriate[i-1], toProcriate[i]
        pop = np.append(pop, crossover(bag1,bag2))
    return pop

def crossover(bag1, bag2):
    corte1 = np.random.randint(0,25)
    corte2 = np.random.randint(0,24)
    if corte2 >= corte1:
        corte2 += 1
    else:
        corte1, corte2 = corte2, corte1
    son1 = bag1.itens[:corte1] + bag2.itens[corte1:corte2] + bag1.itens[corte2:]
    son2 = bag2.itens[:corte1] + bag1.itens[corte1:corte2] + bag2.itens[corte2:]
    return [Bag(son1), Bag(son2)]

def mutatePop(pop):
    toMutate = round(len(pop) * 0.03)
    while toMutate >= 0 :
        pop[np.random.randint(0,len(pop))].doMutation()
        toMutate -= 1
    return pop

def saveGraph(epoca):
        global ax1
        global meanFit
        epochList = np.arange(epoca)
        ax1.clear()
        ax1.plot(epochList,meanFit)
        plt.savefig('epoca.png')

population = initPopulation(1000)
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
theBest = Bag([])
theBestFromGen = Bag([])
meanFit = []
start = time.process_time()
gen = 500
for i in range(gen):
    theBestFromGen = Bag([])
    population = calculatePopFitness(population)
    population = naturalSelection(population,700)
    population = iniciaCrossover(population)
    population = mutatePop(population)
    if theBestFromGen.fitness > theBest.fitness:
        theBest = copy.copy(theBestFromGen)
    maximo = sum([bag.fitness for bag in population])
    meanFit.append(maximo/len(population))
    print(f'-------------------\nGEN {i+1}\nTB: {theBest}\nTBG: {theBestFromGen}\n-------------------')
    saveGraph(i+1)
stop = time.process_time()   
print(f'Finalizado\nExecutada {gen} gerações em {stop - start} segundos\nMelhor Solução: {theBest}')