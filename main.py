import random
import copy

stringSize = 0
populationSize = 0
population = []

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
    print("Hi!")

population = generatePopulation(4,4)
print(population)
print("Population Fitness Average: ", fitnessAverage(population))