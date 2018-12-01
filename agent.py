import random
from tilefeatures import *
import abc

class Agent:
    def __init__(self, m):
        self.market = m #the market

        self.ownedPositions = [] #a list of positons that the agent is currently holding
        self.ownedPositionNums = []
        self.numHoldings = [] #how many holdings the agent has of a given position
        self.latestReward = 0
        self.previousPrices = []
        self.changeInPrices = []

        self.marketPrices = []

        self.cash = 100  #how much our agent has to spend
        self.deltaValue = 0
        self.decisionMaker = LinearSarsaLearner(3, len(self.market.getPositions()), .1, .1, .9) ##numFeatures, numActions, alpha, epsilon, gamma

        self.rewardIntervalSum = 0
        self.rewardIntervalCount = 0
        self.normalizedRewardIntervalLength = 2
        self.skipFirst = True
        self.rewardFile = open("NormalizedRewards.txt", "w")
        self.rewardFileNoLearn = open("NormalizedRewardsNoL.txt", "w")

        self.lastAction = 0
        self.yesterdayValue = 0
        self.market.updateMarket()

        self.initializePositions()

    def initializePositions(self):
        for i in range(4):
            num = random.randrange(len(self.market.getPositions()))
            while(num in self.ownedPositionNums):
                num = random.randrange(len(self.market.getPositions()))
            newPosition = self.market.getPosition(num)

            self.ownedPositions.append(newPosition)
            self.ownedPositionNums.append(num)
            self.numHoldings.append(25 / float(newPosition.getCurrentPrice()))
            self.previousPrices.append(float(newPosition.getCurrentPrice()))
            self.changeInPrices.append(0)

    def update(self, learning):
        '''This will go through the process of a new day in the market'''
        previousWorth = self.calculateHoldingsWorth()
         #first update the market to the new day
        activeFeatures = self.market.getActiveFeatures()
        nextAction = self.makeChoice(activeFeatures,learning)

        oldMarketPrices = self.marketPrices[:]

        self.updatePreviousPrices()
        self.market.updateMarket()
        
        self.marketPrices = self.getPrices()



        nextFeatures = self.market.getActiveFeatures()
        currentWorth = self.calculateHoldingsWorth()
        self.latestReward = currentWorth - previousWorth
        self.latestRewardPercent = self.latestReward/previousWorth

        self.decisionMaker.updateReward(self.latestReward, nextAction, self.lastAction, activeFeatures, nextFeatures)
        self.lastAction = nextAction

        #print("Reward: ", self.latestReward)
        '''make a choice using sarsa and the binary features
                          that we choose. The choice should be between swapping
                          positions or choosing to not hold any'''

        '''self.updateValues() we cannot choose actions and update values based on
        rewards we will have to figure out how to do this'''

        #comment
        marketReward = self.evaluate()
        self.rewardIntervalCount += 1
        if not self.skipFirst:

            avgChange = self.getMarketAverageChange(oldMarketPrices,self.marketPrices)
            normalizedReward = self.latestRewardPercent - avgChange
            self.rewardIntervalSum += normalizedReward
            if self.rewardIntervalCount == self.normalizedRewardIntervalLength:
                averageNormalizedReward = self.rewardIntervalSum / self.normalizedRewardIntervalLength
                self.rewardIntervalCount = 0
                self.rewardIntervalSum = 0
                if learning:
                    self.rewardFile.write(str(averageNormalizedReward) + "\n")
                else:
                    self.rewardFileNoLearn.write(str(averageNormalizedReward) + "\n")
        else:
            self.rewardIntervalSum += 0
        self.skipFirst = False
        return self.latestReward, marketReward / 30

    def getQVal(self):
        return self.decisionMaker.getQVal()

    def getMarketAverageChange(self, oPrices, nPrices):

        totalChange = 0
        for i in range(len(oPrices)):
            totalChange+= (nPrices[i]-oPrices[i])/oPrices[i]

        return totalChange/len(oPrices)

    def makeChoice(self,activeFeatures,learning):
        "Make a decision using LinearSarsa then buy position"
        if(learning):
            position, sell = self.decisionMaker.epsilonGreedy(activeFeatures, self.ownedPositionNums)
        else:
            position, sell = self.decisionMaker.greedy(activeFeatures, self.ownedPositionNums)
        #position = self.market.getPosition(0)

        low = min(self.changeInPrices)
        idx=0
        for i in range(len(self.changeInPrices)):
            if(self.changeInPrices==low):
                idx = i


        self.buyPosition(position, self.ownedPositionNums[idx])
        return position

    def buyPosition(self, newPosition, oldPosition):
        "complete transaction of position, for now sell all of old position to buy max of new (assuming partial shares avaiable)"
        #for pos in self.ownedPositions:
        oldPosIdx = 0
        priorW = self.calculateHoldingsWorth()

        if(newPosition in self.ownedPositionNums):
            print("Erorr already owned", newPosition, self.ownedPositionNums)


        oldPositionH = self.numHoldings[:]
        oldPositions = self.ownedPositionNums[:]
        
        for i in range(len(self.ownedPositionNums)):
            if(self.ownedPositionNums[i]==oldPosition):
                oldPosIdx = i


        #self.cash = self.market.getPositions()[oldPosition].getCurrentPrice()*self.numHoldings
        self.cash = self.ownedPositions[oldPosIdx].getCurrentPrice()*self.numHoldings[oldPosIdx]                             
        self.ownedPositionNums.remove(oldPosition)
        self.ownedPositions.remove(self.market.getPositions()[oldPosition])
        self.numHoldings.pop(oldPosIdx)
        #print("Sold   ", self.numHoldings, "shares of ", self.ownedPositions[0].getTicker(), " at price ", self.ownedPositions[0].getCurrentPrice(), " each")


        
        actualPosition = self.market.getPosition(newPosition)
        self.numHoldings.append((self.cash-.001) / float(actualPosition.getCurrentPrice()))
        self.cash = 0
        self.ownedPositions.append(actualPosition)
        self.ownedPositionNums.append(newPosition)

        if(priorW<self.calculateHoldingsWorth()):
            print("Error!",priorW, self.calculateHoldingsWorth())

            print(oldPosition)
            print(newPosition)
            print(oldPositions)
            print(self.ownedPositionNums)


    def analyzeHeadline(self, headline):
        '''Analyze a string (headline) and return whether it is positive, negative or neutral.'''
        return self.analyzer.runSimpleAnalysis(headline)

    def getReward(self):
        '''Get the reward for the latest day'''
        return self.latestReward

    def updatePreviousPrices(self):

        newPrices = []
        self.changeInPrices = []
        i=0
        for pos in self.ownedPositions:
            newPrices.append(pos.getCurrentPrice())
            self.changeInPrices.append((pos.getCurrentPrice()- self.previousPrices[i])/self.previousPrices[i])
            i+=1
        self.previousPrices = newPrices

    def calculateHoldingsWorth(self):
        '''Calculate the worth of the agent's positions according to the market'''
        worth = 0

        #get the updated position and then add it's price to worth
        for i in range(len(self.ownedPositions)):
            worth += self.market.getPosition(self.ownedPositionNums[i]).getCurrentPrice() * self.numHoldings[i]


        return worth

    def calculateHoldingsWorth2(self,positions,holdings):
        '''Calculate the worth of the agent's positions according to the market'''
        worth = 0

        #get the updated position and then add it's price to worth
        for i in range(len(self.ownedPositions)):
            worth += self.market.getPosition(positions[i]).getCurrentPrice() * holdings[i]


        return worth

    def evaluate(self):
        positions = self.market.getPositions()
        i = 0
        avgValue = 0
        for pos in positions:
            avgValue += pos.getCurrentPrice()
            i += 1
        diff = avgValue - self.yesterdayValue
        self.yesterdayValue = avgValue
        return diff

    def getAverages(self):
        positions = self.market.getPositions()
        i = 0
        avgValue = 0
        for pos in positions:
            avgValue += pos.getCurrentPrice()
            i += 1
        diff = avgValue - self.yesterdayValue
        self.yesterdayValue = avgValue
        return diff

    def getPrices(self):
        positions = self.market.getPositions()
        averages = []
        i = 0
        avgValue = 0
        for pos in positions:
            avgValue = pos.getCurrentPrice()
            averages.append(avgValue)
            i += 1
        return averages

    def closeFiles(self):
        self.rewardFile.close()
        self.rewardFileNoLearn.close()

class LinearSarsaLearner:
    '''Represents an agent using SARSA with linear value function approximation, assuming binary features.'''
    def __init__(self, numFeatures, numActions, alpha, epsilon, gamma):
        '''The constructor takes the number of features and actions as well as
        the step size (alpha), the exploration rate (epsilon), the discount
        factor (gamma).'''
        self.theta = [] #theta represents the weights of the Q function. It is indexed first by action, then by feature index
        for a in range(numActions):
            self.theta.append([0]*numFeatures)

        self.numFeatures = numFeatures
        self.numActions = numActions

        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma

    def getQValue(self, activeFeatures, action):
        '''Calculates the approximate Q-value of a state-action pair. It takes a list of indices of active features (feature value is 1) and the
        action.'''
        q = 0

        for feature in activeFeatures[action]:
            q += self.theta[action][feature]
        return q

    def epsilonGreedy(self, activeFeatures, positions):
        '''With probability epsilon returns a uniform random action. Otherwise it returns a greedy action with respect to the current
         Q function (breaking ties randomly).'''
        chance = random.random()
        if chance > self.epsilon:
            #Do the greedy choice
            return self.greedy(activeFeatures,positions)
        else:
            action = random.randrange(self.numActions)
            while(action in positions):
                #print(positions)
                action = random.randrange(self.numActions)
            return action, positions[random.randrange(len(positions))]

    def greedy(self, activeFeatures, positions):
        '''Returns a greedy action with respect to the current Q function (breaking ties randomly).'''

        action = random.randrange(self.numActions)
        while(action in positions):
            #print(positions)
            action = random.randrange(self.numActions)
        maxQ = self.getQValue(activeFeatures, action)

        minQ = maxQ
        greedyActions = [action]
        sell= 0
        if(len(positions)>0):
            sell = positions[0]
            minQ = self.getQValue(activeFeatures, sell)   
        greedyAction = 0
        for i in range (0, self.numActions):
            action = i
            if(action not in positions):

                curQ = self.getQValue(activeFeatures, action)
                if curQ > maxQ:
                    maxQ = curQ
                    greedyActions = [action]
                elif curQ == maxQ:
                    greedyActions.append(action)
            else:
                curQ = self.getQValue(activeFeatures, action)
                if curQ < minQ:
                    minQ = curQ
                    sell = action

        #randomly pick from greedy actions
        greedyAction = random.choice(greedyActions)

        return greedyAction, sell

    '''
    def learningStep(self, activeFeatures, action, reward, nextFeatures):
        Performs a gradient descent SARSA learning step based on the given transition.
        nextAction = self.epsilonGreedy(activeFeatures)
        return nextAction
    '''

    def updateReward(self, reward, nextAction,action,activeFeatures,nextFeatures):
        delta = reward + (self.gamma * self.getQValue(nextFeatures, nextAction)) - self.getQValue(activeFeatures, action)
        for feature in activeFeatures[action]:
            self.theta[action][feature] += self.alpha * delta


    def terminalStep(self, activeFeatures, action, reward):
        '''Performs the last learning step of an episode. Because the episode has terminated, the next Q-value is 0.'''
        nextAction = self.epsilonGreedy(activeFeatures)
        delta = reward - self.getQValue(activeFeatures, action)
        for feature in activeFeatures:
            self.theta[action][feature] += self.alpha * delta
        return nextAction

    def getQVal(self):
        return self.theta
