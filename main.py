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

def fitnessAverage(group):
    size = len(group)
    total = 0

    for individual in group:
        total += fitness(individual)
    
    return (total/size)

def selection(group):
    pair = []
    for x in range(2):
        string1 = random.choice(group)
        string2 = random.choice(group)
        
        print(string1, "\n", string2)

        if fitness(string1) > fitness(string2):
            pair.append(string1)
        else:
            pair.append(string2)
        
        print(pair)
    
    return pair

def createPairs(group):
    pairCount = int(ceil((len(group)-2)/2)))
    


population = generatePopulation(4,4)
print(population)
print("Population Fitness Average: ", fitnessAverage(population))
breedingPairs.append(selection(population))
print(breedingPairs)