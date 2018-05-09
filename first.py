import numpy as np
import math
import matplotlib.pyplot as plt

def randomWithDispersion(dispersion):
    def randomWithExpectedValue(expectedValue):
        def fixedDispersionAndExpected(arg = None):
            return np.random.normal(expectedValue, dispersion)
        return fixedDispersionAndExpected
    return randomWithExpectedValue

def startSimulationGreedy(bandits, iterationsCount, greedyConstant):
    rewardsSumm = [0] * len(bandits)
    selectionsCount = [0] * len(bandits)
    valuations = [0] * len(bandits)
    allValuesSum = 0
    averageReward = []
    
    def returnTrueWithProbability(probability):
        randomNumber = np.random.uniform(0, 1)
        return randomNumber < probability

    def selectBandit(banditIndex):
        banditValue = bandits[banditIndex]()
        rewardsSumm[banditIndex] = rewardsSumm[banditIndex] + banditValue
        selectionsCount[banditIndex] = selectionsCount[banditIndex] + 1
        valuations[banditIndex] = rewardsSumm[banditIndex] / selectionsCount[banditIndex]
        return banditValue
        
    for i in range(0, iterationsCount):
        isGreedy = returnTrueWithProbability(1 - greedyConstant)
        indexOfSelected = 0
        if isGreedy:
            indexOfSelected = valuations.index(max(valuations))
        else:
            indexOfSelected = np.random.randint(0, len(bandits))
        selectedValue = selectBandit(indexOfSelected)
        allValuesSum = allValuesSum + selectedValue
        averageReward.append(allValuesSum / (i + 1))
    return valuations, averageReward

def startSimulationGibbs(bandits, iterationsCount, temperature):
    rewardsSumm = [0] * len(bandits)
    selectionsCount = [0] * len(bandits)
    valuations = [0] * len(bandits)
    allValuesSum = 0
    averageReward = []
    
    def calcPossibilities():
        possibilities = [0] * len(valuations)
        valuationSum = 0
        for valuation in valuations:
            valuationSum = valuationSum + math.exp(valuation / temperature)
        for j in range(0, len(possibilities)):
            possibilities[j] = math.exp(valuations[j] / temperature) / valuationSum
        return possibilities
    def chooseRandomByPossibilities(possibilities):
        randomNumber = np.random.uniform(0, 1)
        possibilitiesSum = 0
        for i in range(0, len(possibilities)):
            possibilitiesSum = possibilitiesSum + possibilities[i]
            if randomNumber < possibilitiesSum:
                return i
        return 0
    
    def selectBandit(banditIndex):
        banditValue = bandits[banditIndex]()
        rewardsSumm[banditIndex] = rewardsSumm[banditIndex] + banditValue
        selectionsCount[banditIndex] = selectionsCount[banditIndex] + 1
        valuations[banditIndex] = rewardsSumm[banditIndex] / selectionsCount[banditIndex]
        return banditValue
    
    for i in range(0, iterationsCount):
        possibilities = calcPossibilities()
        indexOfSelected = chooseRandomByPossibilities(possibilities)
        selectedValue = selectBandit(indexOfSelected)
        allValuesSum = allValuesSum + selectedValue
        averageReward.append(allValuesSum / (i + 1))
    return valuations, averageReward
    
    
def addAverageRewardsToPlot(averageReward, label):
    plt.plot(np.arange(len(averageReward)), averageReward, label = label)

banditsCount = 10
iterationsCount = 1000
tasksCount = 2000

dispersion = 1

generateExpectedValues = np.vectorize(randomWithDispersion(1)(0))
generateBandits = np.vectorize(randomWithDispersion(dispersion))

def startGreedyAlgTest():
    greedyConstants = [0, 0.01, 0.1]
    for greedyConstant in greedyConstants:
        allAverageRewards = np.zeros(iterationsCount)
        for i in range(0, tasksCount):
            expectedValues = generateExpectedValues(np.zeros(banditsCount))
            bandits = generateBandits(expectedValues)
            valuations, averageReward = startSimulationGreedy(bandits, iterationsCount, greedyConstant)
            allAverageRewards = allAverageRewards + averageReward
            if i % 100 == 0:
                print(i)
        allAverageRewards = allAverageRewards / tasksCount
        addAverageRewardsToPlot(allAverageRewards, 'greedy: ' + str(greedyConstant))

def startGibbsAlgTest():
    temperatures = [0.1, 0.5, 1, 10]
    for temperature in temperatures:
        allAverageRewards = np.zeros(iterationsCount)
        for i in range(0, tasksCount):
            expectedValues = generateExpectedValues(np.zeros(banditsCount))
            bandits = generateBandits(expectedValues)
            valuations, averageReward = startSimulationGibbs(bandits, iterationsCount, temperature)
            allAverageRewards = allAverageRewards + averageReward
            if i % 100 == 0:
                print(i)
        allAverageRewards = allAverageRewards / tasksCount
        addAverageRewardsToPlot(allAverageRewards, 'gibbs: ' + str(temperature))

def startDispercionGreedyComparision():
    dispersions = [1, 2, 5]
    expectedValues = generateExpectedValues(np.zeros(banditsCount))
    for disp in dispersions:
        generateCustomBandits = np.vectorize(randomWithDispersion(disp))
        bandits = generateCustomBandits(expectedValues)
        valuations, averageReward = startSimulationGreedy(bandits, iterationsCount, 0.1)
        addAverageRewardsToPlot(averageReward, 'disp: ' + str(disp))

def startDispercionGibbsComparision():
    dispersions = [1, 2, 5]
    expectedValues = generateExpectedValues(np.zeros(banditsCount))
    for disp in dispersions:
        generateCustomBandits = np.vectorize(randomWithDispersion(disp))
        bandits = generateCustomBandits(expectedValues)
        valuations, averageReward = startSimulationGibbs(bandits, iterationsCount, 0.1)
        addAverageRewardsToPlot(averageReward, 'disp: ' + str(disp))

#startGreedyAlgTest()
#startGibbsAlgTest()
#startDispercionGreedyComparision()   
#startDispercionGibbsComparision()
plt.legend()
plt.show()
    
