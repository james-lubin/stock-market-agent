import random
from tilefeatures import *
import abc


class Agent:
    def __init__(self,m):
        self.market = m #the market

        self.ownedPosition = None #this will typically be an object of the positon that the agent is currently holding
        self.numHoldings = 0 #how many holdings the agent has of a given position
        
        self.cash = 100  #how much our agent has to spend

        self.decisionMaker = LinearSarsaLearner(1,1,.1,.1,1) ##numFeatures, numActions, alpha, epsilon, gamma

    def update(self):
        '''This will go through the process of a new day in the market'''
        self.market.updateMarket() #first update the market to the new day

        self.makeChoice() #make a choice using sarsa and the binary features that we choose. The choice should be between swapping positions or choosing to not hold any

        #self.updateValues() we cannot choose actions and update values based on rewards we will have to figure out how to do this

        #self.evaluate() evaluate performace of agent, this is issue for much longer down road

    def makeChoice(self):
        "Make a decision using LinearSarsa then buy position"

        #position = self.decisionMaker.learningStep(activeFeatures, action, reward, nextFeatures)
        position = self.market.getPosition(0)
        self.buyPosition(position)

    def buyPosition(self,newPosition):
        "complete transaction of position, for now sell all of old position to buy max of new (assuming partial shares avaiable)"
        if(self.ownedPosition!=None): 
            self.cash = self.ownedPosition[0].getCurrentPrice()*self.ownedPosition[1]
        
        self.numHoldings = self.cash/newPosition.getCurrentPrice()
        self.ownedPosition = newPosition

        





class LinearSarsaLearner:
    '''Represents an agent using SARSA with linear value function approximation, assuming binary features.'''
    def __init__(self, numFeatures, numActions, alpha, epsilon, gamma):
        '''The constructor takes the number of features and actions as well as the step size (alpha), the exploration rate (epsilon), the discount
        factor (gamma).'''
        self.theta = [] #theta represent the weights of the Q function. It is indexed first by action, then by feature index
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
        for feature in activeFeatures:
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
        for i in range (1,self.numActions):
            action = i
            curQ = self.getQValue(activeFeatures, action)
            if curQ > maxQ:
                curQ = maxQ
                greedyActions = [action]
            elif curQ == maxQ:
                #flip a coin on whether we update the max in order to maintain the randomness property
                greedyActions.append(action)

        greedyAction = random.choice(greedyActions)

        return greedyAction


    def learningStep(self, activeFeatures, action, reward, nextFeatures):
        '''Performs a gradient descent SARSA learning step based on the given transition.'''
        nextAction = self.epsilonGreedy(activeFeatures)
        delta = reward + (self.gamma * self.getQValue(nextFeatures, nextAction)) - self.getQValue(activeFeatures, action)
        for feature in activeFeatures:
            self.theta[action][feature] += self.alpha * delta
        return nextAction

    def terminalStep(self, activeFeatures, action, reward):
        '''Performs the last learning step of an episode. Because the episode has terminated, the next Q-value is 0.'''
        nextAction = self.epsilonGreedy(activeFeatures)
        delta = reward - self.getQValue(activeFeatures, action)
        for feature in activeFeatures:
            self.theta[action][feature] += self.alpha * delta
        return nextAction