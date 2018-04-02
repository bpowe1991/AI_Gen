import random
import math
import os

stringSize = 0
population = []
lowerBound = 0
upperBound = 0

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
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        
        if fitness(parent1) > fitness(parent2):
            pair.append(parent1)
        else:
            pair.append(parent2)
    
    return pair

def createPairs(population):
    pairs = []
    pairCount = math.ceil((len(population)-2)/2)

    for i in range(pairCount):
        pairs.append(selection(population))
    
    return pairs
    
def mutation(child):
    mutationChance = 0
    childArr = list(child)

    for x in range(len(childArr)):
        mutationChance = random.randint(1, len(childArr))
        
        if mutationChance == 1:
            if childArr[x] == "1":
                childArr[x] = "0"
            else:
                childArr[x] = "1"
        
    child = ''.join(childArr)
   
    return child
        
def generateChildren(population):
    pairs = createPairs(population)
    children = []

    for pair in pairs:
        child = ""
        secondChild = ""

        copyChance = random.randint(1, len(pair[0]))

        if copyChance >= 1 and copyChance <= 4:
            child = pair[0]
            secondChild = pair[1]

            child = mutation(child)
            secondChild = mutation(secondChild)

            children.append(child)
            children.append(secondChild)
        
        else:
            for x in range(len(pair[0])):
                child += pair[random.randint(0,1)][x]

                if child [len(child)-1] == "1":
                    secondChild += "0"
                else:
                    secondChild += "1"

            child = mutation(child)
            secondChild = mutation(secondChild)

            children.append(child)
            children.append(secondChild)
    
    return children

def getMostFit(population):
    fitnessOrder = []
    
    for individual in population:
        fitnessOrder.append((individual, fitness(individual)))

    fitnessOrder = sorted(fitnessOrder, key = lambda fitness: fitness[1], reverse = True)

    if (len(population)%2) == 0:
        return [fitnessOrder[0][0], fitnessOrder[1][0]]
    else:
        return [fitnessOrder[0][0]]

def replacement(population):
    children = generateChildren(population)
    newPopulation = getMostFit(population) + children
    return newPopulation

def displayMostFit(population):
    mostFit = []
    highestFitness = 0
    for individual in population:
        if fitness(individual) > highestFitness:
            mostFit.clear()
            mostFit.append(individual)
            highestFitness = fitness(individual)
        elif fitness(individual) == highestFitness:
            mostFit.append(individual)
    
    print("Highest Fitness:", highestFitness, "\n")
    print("Most Fit:")
    for each in mostFit:
        print(each)
    print("")

def displayLeastFit(population):
    leastFit = []
    lowestFitness = len(population[0])
    for individual in population:
        if fitness(individual) < lowestFitness:
            leastFit.clear()
            leastFit.append(individual)
            lowestFitness = fitness(individual)
        elif fitness(individual) == lowestFitness:
            leastFit.append(individual)
    
    print("Lowest Fitness:", lowestFitness, "\n")
    print("Least Fit:")
    for each in leastFit:
        print(each)
    print("")

def hasOptimum(population):
    optimum = len(population[0])
    hasOpt = False
    for each in population:
        if fitness(each) == optimum:
            hasOpt = True
    
    return hasOpt

def geneticAlgorithm(stringLength):
    global population

    previousAvg = fitnessAverage(population)
    print("Starting Population:\n")
    for each in population:
        print(each)
    print("\nFitness Average:", previousAvg, "\n")
    displayMostFit(population)
    displayLeastFit(population)
    print("Optimum Found:", hasOptimum(population))
    print("-----------------------------------------------------------")

    flagCounter = 0
    count = 1
    optimumCounter = 0

    while flagCounter < 3:
        population = replacement(population)
        currentAvg = fitnessAverage(population)

        if currentAvg <= previousAvg:
            flagCounter += 1
        else:
            flagCounter = 0

        if hasOptimum(population):
            optimumCounter += 1
        previousAvg = currentAvg
        count += 1
    
    print("Generation Count: ", count)
    print("Population:\n")
    for each in population:
        print(each)
    print("\nFitness Average:", currentAvg, "\n")
    displayMostFit(population)
    displayLeastFit(population)
    print("Optimum Found:", hasOptimum(population))
    print("-----------------------------------------------------------")
    return hasOptimum(population), count

stringLength = None
while stringLength is None:
        input_value = input("Please enter the length of string: \n\n")
        try:
            #Convert user input into integer and check if in range
            stringLength = int(input_value)
            if stringLength < 1:
                print("\nError! String length must be greater than 0.")
                stringLength = None
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                populationSize = 10
                timesFound = 0
                population = generatePopulation(stringLength, populationSize)
                for x in range(5):
                    foundOpt, bound = geneticAlgorithm(stringLength)
                    if foundOpt == False:
                        lowerBound = bound
                        break
                    else:
                        timesFound += 1
                if timesFound == 5:
                    upperBound == bound
                else:
                    print("Failed to Find Optimum with population size", populationSize)

                print("\n")

        except ValueError:
            #Error message for non-integer input
            print("\nError! Please enter an integer greater than 0.")
