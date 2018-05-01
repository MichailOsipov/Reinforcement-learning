import numpy as np
import matplotlib.pyplot as plt

minExpected = 1
maxExpected = 100
dispersion = 1
automatsCount = 20
def randomNumberInRange(x):
    return np.random.randint(minExpected, maxExpected)

def randomWithExpectedValue(expectedValue):
    def fixedExpected():
        return np.random.normal(expectedValue, dispersion)
    return fixedExpected

generatedExpectedValues = np.vectorize(randomNumberInRange)
generateBandits = np.vectorize(randomWithExpectedValue)
expectedValuesToBandits = generatedExpectedValues([0] * automatsCount)
print("expected:")
print(expectedValuesToBandits)
bandits = generateBandits(expectedValuesToBandits)
    
def startSimulationGreedy(bandits, iterationsCount, greedyConstant):
    rewardsSumm = [0] * len(bandits)
    selectionsCount = [0] * len(bandits)
    valuation = [0] * len(bandits)
    allValuesSum = 0
    averageReward = []
    
    def returnTrueWithProbability(probability):
        randomNumber = np.random.uniform(0, 1)
        return randomNumber < probability

    def selectBandit(banditIndex):
        banditValue = bandits[banditIndex]()
        rewardsSumm[banditIndex] = rewardsSumm[banditIndex] + banditValue
        selectionsCount[banditIndex] = selectionsCount[banditIndex] + 1
        valuation[banditIndex] = rewardsSumm[banditIndex] / selectionsCount[banditIndex]
        return banditValue
        
    for i in range(0, iterationsCount):
        isGreedy = returnTrueWithProbability(1 - greedyConstant)
        indexOfSelected = 0
        if isGreedy:
            indexOfSelected = valuation.index(max(valuation))
        else:
            indexOfSelected = np.random.randint(0, len(bandits))
        selectedValue = selectBandit(indexOfSelected)
        allValuesSum = allValuesSum + selectedValue
        averageReward.append(allValuesSum / (i + 1))
    return valuation, averageReward
      
greedyConstants = [0, 0.01, 0.1]

iterationsCount = 1000
for greedyConstant in greedyConstants:
    valuation, averageReward = startSimulationGreedy(bandits, iterationsCount, greedyConstant)
    plt.plot(np.arange(len(averageReward)), averageReward, label = greedyConstant)

plt.legend()
plt.show()
