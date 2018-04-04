""""
Programmer: Briton A. Powe          Program Homework Assignment #3
Date: 4/4/18                       Class: Introduction to A.I.
Version: 1.3.1
File: PoweGeneticAlgorithm
------------------------------------------------------------------------
Program Description:
Uses a simple genetic algorithm that uniform crossover and mutation 
to solve the onemax problem with a user defined string length. 
***This program uses Python 3.6.4***
"""

import random
import math
import os
import copy

#list to designate the population
population = []

#Global list to keep track of the best population
bestPopulation = []
generationTracker = 1

#Function to generate starting population
def generatePopulation(length, size):
    group = []

    for _ in range(size):
        string = ""
        for _ in range(length):
            string += str(random.randint(0,1))
        
        group.append(string)
    # returns list of generated strings
    return group

#Function to calculate fitness of a given string
def fitness(string):
    count = 0
    for char in string:
        if char == "1":
            count += 1
    return count

#Function to calculate the average fitness of a population
def fitnessAverage(population):
    size = len(population)
    total = 0

    for individual in population:
        total += fitness(individual)
    
    return (total/size)

#Function to perform selection of parents
def selection(population):
    pair = []

    #Loop to choose parents based on fitness
    for _ in range(2):
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        
        if fitness(parent1) > fitness(parent2):
            pair.append(parent1)
        else:
            pair.append(parent2)
    
    #Return the parent pair
    return pair

#Function to create pairs for reproduction
def createPairs(population):
    pairs = []

    #Calculating number of pairs needed
    pairCount = math.ceil((len(population)-2)/2)

    for _ in range(pairCount):
        pairs.append(selection(population))
    
    return pairs

#Function to mutate string    
def mutation(child):
    mutationChance = 0
    childArr = list(child)

    #Looping over all characters for mutation chance
    for x in range(len(childArr)):
        mutationChance = random.randint(1, len(childArr))
        
        if mutationChance == 1:
            if childArr[x] == "1":
                childArr[x] = "0"
            else:
                childArr[x] = "1"

    #Fusing all characters into string    
    child = ''.join(childArr)
   
    return child

#Function to create the children of next generation        
def generateChildren(population):
    pairs = createPairs(population)
    children = []

    for pair in pairs:
        child = ""
        secondChild = ""

        copyChance = random.randint(1, 10)

        #40% chance of copying parents
        if copyChance >= 1 and copyChance <= 4:
            child = pair[0]
            secondChild = pair[1]

            #Mutating children
            child = mutation(child)
            secondChild = mutation(secondChild)

            #Adding children to new generation
            children.append(child)
            children.append(secondChild)
        
        #60% chance of uniform crossover 
        else:
            
            #Loop for uniform crossover
            for x in range(len(pair[0])):
                gene = random.randint(0,1)
                child += pair[gene][x]

                #Building children
                if gene == 1:
                    secondChild += pair[0][x]
                else:
                    secondChild += pair[1][x]

            #Mutating children
            child = mutation(child)
            secondChild = mutation(secondChild)

            #Adding children to new generation
            children.append(child)
            children.append(secondChild)
    
    return children

#Function to calculate the most fit parent(s) in current generation
def getMostFit(population):
    fitnessOrder = []
    
    for individual in population:
        fitnessOrder.append((individual, fitness(individual)))

    #Ordering list by greatest fitness to poorest fitness
    fitnessOrder = sorted(fitnessOrder, key = lambda fitness: fitness[1], reverse = True)

    #If the population is even it returns 2 parents
    if (len(population)%2) == 0:
        return [fitnessOrder[0][0], fitnessOrder[1][0]]
    
    #If the population is odd it returns 1 parent
    else:
        return [fitnessOrder[0][0]]

#Function to perform replacement for next generation
def replacement(population):
    children = generateChildren(population)
    newPopulation = getMostFit(population) + children
    return newPopulation

#Function to display a populations most fit string(s)
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

#Function to display a populations least fit string(s)
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

#Function to determine if a population has the optimum
def hasOptimum(population):
    optimum = len(population[0])
    hasOpt = False
    for each in population:
        if fitness(each) == optimum:
            hasOpt = True
    
    return hasOpt

#Main function for genetic algorithm
def geneticAlgorithm(stringLength, population):

    previousAvg = fitnessAverage(population)
    flagCounter = 0
    count = 1
    optimumCounter = 0
    global generationTracker

    #Loop for generation and replacement
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

    #Set generation tracker to latest most successful
    if hasOptimum(population):
        generationTracker = count

    #Return the last population and whether optimum was found
    return hasOptimum(population), population

#Function to determine intial upper and lower bounds for bisection
def calculateBounds(population, populationSize, stringLength):
    timesFound = 0
    lowerBound = 10
    upperBound = 0

    #Keeps track of successful generation
    global bestPopulation

    #Main loop to execute. Doubling after failing
    while populationSize <= 81920:
        for _ in range(5):
            population = generatePopulation(stringLength, populationSize)
            foundOpt, lastPopulation = geneticAlgorithm(stringLength, population)
            
            #Set lower bound when it fails
            if foundOpt == False:
                lowerBound = populationSize
                break
            
            #Increment counter for successful generations
            else:
                timesFound += 1

        #Set upper bound when it succeeds 5/5 times
        if timesFound == 5:
            upperBound = populationSize
            bestPopulation = copy.copy(lastPopulation)
            break
        
        #Output failure and double population
        else:
            print("Failed to Find Optimum with population size", populationSize)
            print("-----------------------------------------------------------")
            timesFound = 0
            populationSize *= 2
    
    return upperBound, lowerBound

#Function to calculate whether bisection successfully generates optimum
def calculateBisection(population, size, length):

    timesFound = 0
    hasOpt = False
    global bestPopulation

    #Loop to determine successful optimum generation
    for _ in range(5):
        population = generatePopulation(length, size)
        foundOpt, lastPopulation = geneticAlgorithm(length, population)
        if foundOpt == False:
            hasOpt = False
            break
        else:
            timesFound += 1
    
    #If successful, record the population
    if timesFound == 5:
        hasOpt = True
        bestPopulation = copy.copy(lastPopulation)
    
    return hasOpt


#Main program loop
stringLength = None
while stringLength is None:
        input_value = input("Please enter the length of string: \n\n")
        try:
            #Convert user input into integer and check if valid
            stringLength = int(input_value)
            
            #Error checking for string length
            if stringLength < 1:
                print("\nError! String length must be greater than 0.")
                stringLength = None
            else:
                print("\n-----------------------------------------------------------")

                #Finding upper and lower bounds
                upperBound, lowerBound = calculateBounds(population, 10, stringLength)
                
                print("Success with population size", upperBound)
                print("-----------------------------------------------------------")
                #Find smallest successful population with bisection
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
                    print("-----------------------------------------------------------")
                
                #Output results of smallest successful population
                print("\n\nCalculated Minimum Population:", upperBound, "\n\n")
                print("Generation Count:", generationTracker)
                print("\nFitness Average:", fitnessAverage(bestPopulation), "\n")
                displayMostFit(bestPopulation)
                displayLeastFit(bestPopulation)
         
        except ValueError:
            #Error message for non-integer input
            print("\nError! Please enter an integer greater than 0.")
