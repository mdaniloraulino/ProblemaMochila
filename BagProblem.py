import pandas as pd
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
from matplotlib import style
from operator import attrgetter
style.use('fivethirtyeight')

dt = pd.read_excel('Tabela_Artigos.xls')

class Item:
    def __init__(self, artigo, volume, peso, valor):
        self.artigo = artigo
        self.volume = volume
        self.peso = peso
        self.valor = valor
        
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
                vlT = vlT + dt.iloc[i].values[3]
                p = p + dt.iloc[i].values[2]
                v = v + dt.iloc[i].values[1]
        if not elitista:
            if (p) == 0 :
                self.fitness = 0 
            elif p + v == 250:
                self.fitness = vlT
            else:
                self.fitness = vlT / (p + v) + abs(125 - p) + abs(125 - v)
        else:
            if p > 125 or v > 125:
                self.fitness = 0
            else:
                self.fitness = vlT
        self.peso = p
        self.vlTotal = vlT
        self.volume = v
        return self.fitness
        
    def doMutation(self):
        for i in range(3):
            randIndex = np.random.randint(0,25)
            if self.itens[randIndex] == 0:
                self.itens[randIndex] = 1
            else:
                self.itens[randIndex] = 0

def initPopulation(size):
    pop = []
    for i in range(size):
        a = np.random.randint(low=0,high=2,size=25)
        pop.append(Bag(a.tolist()))
    return np.array(pop)

def calculatePopFitness(pop):
    global theBest, theBestFromGen
    for bag in pop:
        fit = bag.calculateFitness(True)
        if fit > theBestFromGen.fitness:
            theBestFromGen = copy.copy(bag)
    return pop
        
def naturalSelection(pop,numToSelection):
    max = sum([bag.fitness for bag in pop])
    selection_probs = [bag.fitness/max for bag in pop]
    felizardos = (pop[np.random.choice(len(pop),size=numToSelection,replace = False, p=selection_probs)])
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
    else:  # Swap the two cx points
        corte1, corte2 = corte2, corte1
    son1 = bag1.itens[:corte1] + bag2.itens[corte1:corte2] + bag1.itens[corte2:]
    son2 = bag2.itens[:corte1] + bag1.itens[corte1:corte2] + bag2.itens[corte2:]
    return [Bag(son1), Bag(son2)]

def mutatePop(pop):
    toMutate = round(len(pop)* 0.03)
    for i in range(toMutate):
        pop[np.random.randint(0,len(pop))].doMutation()
    return pop

def saveGraph(epoca):
        global ax1
        global meanFit
        epochList = np.arange(epoca)
        ax1.clear()
        ax1.plot(epochList,meanFit)
        plt.savefig('c:\\Users\\Danilo\\desktop\\epocas\\epoca.png')

population = initPopulation(1000)
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
theBest = Bag([])
theBestFromGen = Bag([])
meanFit = []
for i in range(250):
    theBestFromGen = Bag([])
    population = calculatePopFitness(population)
    population = naturalSelection(population,800)
    population = iniciaCrossover(population)
    population = mutatePop(population)
    if theBestFromGen.fitness > theBest.fitness:
        theBest = copy.copy(theBestFromGen)
    maximo = sum([bag.fitness for bag in population])
    meanFit.append(maximo/len(population))
    print(f'-------------------\nGEN {i+1}\nTB: {theBest}\nTBG: {theBestFromGen}\n-------------------')
    saveGraph(i+1)
print("FIM")