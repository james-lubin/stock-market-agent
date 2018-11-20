import random
from tilefeatures import *
import abc
from natural_language_processing import *

class Agent:
    def __init__(self, m):
        self.market = m #the market

        self.ownedPositions = [] #a list of positons that the agent is currently holding
        self.numHoldings = 0 #how many holdings the agent has of a given position
        self.latestReward = 0

        self.cash = 100  #how much our agent has to spend
        self.deltaValue = 0
<<<<<<< HEAD
        self.decisionMaker = LinearSarsaLearner(3, len(self.market.getPositions()), .1, .1, .9) ##numFeatures, numActions, alpha, epsilon, gamma

        self.analyzer = Sentiment()
        self.lastAction = 0
        self.yesterdayValue = 0
        self.market.updateMarket()
=======
        self.decisionMaker = LinearSarsaLearner(1, 1, .1, .1, 1) ##numFeatures, numActions, alpha, epsilon, gamma
        self.analyzer = Sentiment()
>>>>>>> master

    def update(self, learning):
        '''This will go through the process of a new day in the market'''
        previousWorth = self.calculateHoldingsWorth(self.ownedPositions)
<<<<<<< HEAD
         #first update the market to the new day
        activeFeatures = self.market.getActiveFeatures()
        nextAction = self.makeChoice(activeFeatures,learning)
        self.market.updateMarket()


        nextFeatures = self.market.getActiveFeatures()
        currentWorth = self.calculateHoldingsWorth(self.ownedPositions)
        self.latestReward = currentWorth - previousWorth

        self.decisionMaker.updateReward(self.latestReward,nextAction,self.lastAction,activeFeatures,nextFeatures)
        self.lastAction = nextAction
=======
        self.market.updateMarket() #first update the market to the new day
        self.makeChoice()
        currentWorth = self.calculateHoldingsWorth(self.ownedPositions)
        self.latestReward = currentWorth - previousWorth
        print("Reward: ", self.latestReward)
        '''make a choice using sarsa and the binary features
                          that we choose. The choice should be between swapping
                          positions or choosing to not hold any'''

        '''self.updateValues() we cannot choose actions and update values based on
        rewards we will have to figure out how to do this'''
        #self.evaluate() evaluate performace of agent, this is issue for much longer down road
>>>>>>> master

        #print("Reward: ", self.latestReward)
        '''make a choice using sarsa and the binary features
                          that we choose. The choice should be between swapping
                          positions or choosing to not hold any'''

        '''self.updateValues() we cannot choose actions and update values based on
        rewards we will have to figure out how to do this'''
        marketReward = self.evaluate()# evaluate performace of agent, this is issue for much longer down road
        return self.latestReward, marketReward/30

    def getQVal(self):
        return self.decisionMaker.getQVal()

    def makeChoice(self,activeFeatures,learning):
        "Make a decision using LinearSarsa then buy position"
        if(learning):
            position = self.decisionMaker.epsilonGreedy(activeFeatures)
        else:
            position = self.decisionMaker.greedy(activeFeatures)
        #position = self.market.getPosition(0)
        self.buyPosition(position)
        print("Buying position: ", self.market.getPosition(position).getTicker(), " at price: ",  self.market.getPosition(position).getCurrentPrice())
        return position

    def buyPosition(self, newPosition):
        "complete transaction of position, for now sell all of old position to buy max of new (assuming partial shares avaiable)"
<<<<<<< HEAD
        #for pos in self.ownedPositions:
        if(len(self.ownedPositions) >= 1):
            self.cash = self.ownedPositions[0].getCurrentPrice()*self.numHoldings
        #self.ownedPositions = []

        actualPosition = self.market.getPosition(newPosition)
        self.numHoldings = self.cash / float(actualPosition.getCurrentPrice())
        self.cash = 0
        self.ownedPositions = [actualPosition]

    def analyzeHeadline(self, headline):
        '''Analyze a string (headline) and return whether it is positive, negative or neutral.'''
        return self.analyzer.runSimpleAnalysis(headline)

    def getReward(self, previousWorth, currentWorth):
        '''Get the reward for the latest day'''
        return self.latestReward

    def calculateHoldingsWorth(self, positions):
        '''Calculate the worth of the agent's positions according to the market'''
        worth = 0
        #get the updated position and then add it's price to worth
        if(len(positions)==1):
            worth += self.market.getPositionByTicker(positions[0].getTicker()).getCurrentPrice() * self.numHoldings
        else:
            worth+= self.cash

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

=======
        for pos in self.ownedPositions:
            self.cash += pos.getCurrentPrice()
        self.ownedPositions = []

        self.numHoldings = self.cash / float(newPosition.getCurrentPrice())
        self.cash = 0
        self.ownedPositions.append(newPosition)

    def analyzeHeadline(self, headline):
        '''Analyze a string (headline) and return whether it is positive, negative or neutral.'''
        return self.analyzer.runSimpleAnalysis(headline)

    def getReward(self, previousWorth, currentWorth):
        '''Get the reward for the latest day'''
        return self.latestReward

    def calculateHoldingsWorth(self, positions):
        '''Calculate the worth of the agent's positions according to the market'''
        worth = self.cash
        for pos in positions:
            #get the updated position and then add it's price to worth
            worth += self.market.getPositionByTicker(pos.getTicker()).getCurrentPrice() * self.numHoldings

        return worth
>>>>>>> master

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

    def epsilonGreedy(self, activeFeatures):
        '''With probability epsilon returns a uniform random action. Otherwise it returns a greedy action with respect to the current
         Q function (breaking ties randomly).'''
        chance = random.random()
        if chance > self.epsilon:
            #Do the greedy choice
            return self.greedy(activeFeatures)
        else:
            return random.randrange(self.numActions)

    def greedy(self, activeFeatures):
        '''Returns a greedy action with respect to the current Q function (breaking ties randomly).'''
        maxQ = self.getQValue(activeFeatures, 0)
        greedyActions = [0]
        greedyAction = 0
        for i in range (1, self.numActions):
            action = i
            curQ = self.getQValue(activeFeatures, action)
            if curQ > maxQ:
                curQ = maxQ
                greedyActions = [action]
            elif curQ == maxQ:
                greedyActions.append(action)

        #randomly pick from greedy actions
        greedyAction = random.choice(greedyActions)

        return greedyAction

<<<<<<< HEAD
    '''
=======

>>>>>>> master
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
