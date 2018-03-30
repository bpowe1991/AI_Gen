import random
import math

stringSize = 0
populationSize = 0
population = []
breedingPairs = []

def generatePopulation(length, size):
    group = []

    for i in range(size):
        string = ""
        for c in range(length):
            string += str(random.randint(0,1))
        
        group.append(string)
    
    return group

def fitness(string):
    count = 0
    for char in string:
        if char == "1":
            count += 1
    return count

def fitnessAverage(population):
    size = len(population)
    total = 0

    for individual in population:
        total += fitness(individual)
    
    return (total/size)

def selection(population):
    pair = []

    for x in range(2):
        string1 = random.choice(population)
        string2 = random.choice(population)
        
        if fitness(string1) > fitness(string2):
            pair.append(string1)
        else:
            pair.append(string2)
    
    return pair

def createPairs(population):
    pairs = []
    pairCount = math.ceil((len(population)-2)/2)
    print("Number of Pairs:", pairCount)

    for i in range(pairCount):
        pairs.append(selection(population))
    
    return pairs
    
def generateChildren(population):
    pairs = createPairs(population)
    print(pairs)
    children = []
    for pair in pairs:
        child = ""
        print(len(pair[0]))
        for x in range(len(pair[0])):
            child += pair[random.randint(0,1)][x]
        children.append(child)
    print(children)

population = generatePopulation(10,10)
print(population)
print("Population Fitness Average: ", fitnessAverage(population))
generateChildren(population)