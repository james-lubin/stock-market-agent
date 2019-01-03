import agent
import market
import sys
import math

def main():
    filename = sys.argv[1]
    days = int(sys.argv[2])
    trials = int(sys.argv[3])

    txtFile = open(filename, "r")
    lines = txtFile.readlines()
    data = lines
    rewardLists = []
    totalRewards = []
    rewardIntervalLength = 100

    for t in range(trials):
        localMarket = market.Market(data)
        localAgent = agent.Agent(localMarket, rewardIntervalLength)

        totalReward = 0
        marketReward = 0

        startAverages = localAgent.getAverages()
        for d in range(days):
            tReward, mReward = localAgent.update(True)
            totalReward += tReward
            marketReward += mReward
        endAverages = localAgent.getAverages()
        rewardLists.append(localAgent.getNormalizedRewardList())
        totalRewards.append(totalReward)
        learningTotal, learningMarketReward = totalReward, marketReward

        print("\n\n-------------------Results-------------------")
        print("Trial ", t + 1)
        print("Total Reward: ", learningTotal)
        print("Market Reward: ", learningMarketReward)

        totalReward = 0
        marketReward = 0

        localAgent.closeFiles()

    normRewardsAvgsFile = open("NormalizedRewardAverages.txt", "w")
    numIntervals = len(rewardLists[0]) #all intervals should have the same length reward list
    numLists = trials
    for interval in range(numIntervals):
        dailyRewardSum = 0
        for rewardList in rewardLists:
            dailyRewardSum += rewardList[interval]
        intervalAverage = dailyRewardSum / numLists
        normRewardsAvgsFile.write(str(intervalAverage) + "\n")

    totalRewardAvg = sum(totalRewards)/len(totalRewards)

    print("\n\n-------------------TRIALS COMPLETED-------------------")
    print("Average Profit: ", totalRewardAvg)

    rewardFile = open("TotalRewards.txt", "w")
    for reward in totalRewards:
        rewardFile.write(str(reward) + "\n")
    normRewardsAvgsFile.close()




main()
