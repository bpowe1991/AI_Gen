import random
import math
import os

stringSize = 0
population = []

def generatePopulation(length, size):
    group = []

    for _ in range(size):
        string = ""
        for _ in range(length):
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

    for _ in range(2):
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

    for _ in range(pairCount):
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

        copyChance = random.randint(1, 10)

        if copyChance >= 1 and copyChance <= 4:
            child = pair[0]
            secondChild = pair[1]

            child = mutation(child)
            secondChild = mutation(secondChild)

            children.append(child)
            children.append(secondChild)
        
        else:
            for x in range(len(pair[0])):
                gene = random.randint(0,1)
                child += pair[gene][x]

                if gene == 1:
                    secondChild += pair[0][x]
                else:
                    secondChild += pair[1][x]

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

def geneticAlgorithm(stringLength, population):

    previousAvg = fitnessAverage(population)
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

    print("\nPopulation Size:", len(population))
    print("Generation Count: ", count)
    print("\nFitness Average:", currentAvg, "\n")
    displayMostFit(population)
    displayLeastFit(population)
    print("Optimum Found:", hasOptimum(population))
    print("\n-----------------------------------------------------------")
    return hasOptimum(population)

def calculatePopulationRange(population, populationSize, stringLength):
    #os.system('cls' if os.name == 'nt' else 'clear')
    timesFound = 0
    lowerBound = 10
    upperBound = 0

    while populationSize <= 19200:
        for _ in range(5):
            population = generatePopulation(stringLength, populationSize)
            foundOpt = geneticAlgorithm(stringLength, population)
            if foundOpt == False:
                lowerBound = populationSize
                break
            else:
                timesFound += 1
        if timesFound == 5:
            upperBound = populationSize
            break
        else:
            print("Failed to Find Optimum with population size", populationSize)
            print("-----------------------------------------------------------")
            timesFound = 0
            populationSize *= 2
    
    return upperBound, lowerBound

def calculateBisection(population, size, length):
    #os.system('cls' if os.name == 'nt' else 'clear')
    timesFound = 0
    hasOpt = False

    for _ in range(5):
        population = generatePopulation(length, size)
        foundOpt = geneticAlgorithm(length, population)
        if foundOpt == False:
            hasOpt = False
            break
        else:
            timesFound += 1
    
    if timesFound == 5:
        hasOpt = True
    
    return hasOpt


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
                print("\n-----------------------------------------------------------")
                upperBound, lowerBound = calculatePopulationRange(population, 10, stringLength)
                while ((upperBound-lowerBound)/upperBound) >= 0.1:
                    bisection = math.ceil((upperBound+lowerBound)/2)
                    print("Current Upper Bound:", upperBound, 
                          "\nCurrent Lower Bound:", lowerBound, 
                          "\nCurrent Bisection:", bisection)
                    print("-----------------------------------------------------------")
                    success = calculateBisection(population, bisection, stringLength)
                    if success == True:
                        print("Success at population size", bisection)
                        upperBound = bisection
                    else:
                        print("Failure at population size", bisection)
                        lowerBound = bisection
                    print("-----------------------------------------------------------\n\n")
                print("Calculated Minimum Population: ", upperBound, "\n\n")
                
                
        except ValueError:
            #Error message for non-integer input
            print("\nError! Please enter an integer greater than 0.")
