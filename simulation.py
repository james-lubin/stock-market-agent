import agent
import market
import sys

def main():
    filename = sys.argv[1]
    days = int(sys.argv[2])
    trials = int(sys.argv[3])

    txtFile = open(filename, "r")
    lines = txtFile.readlines()
    data = lines


    for t in range(trials):
        localMarket = market.Market(data)
        localAgent = agent.Agent(localMarket)

        totalReward = 0
        marketReward = 0

        startAverages = localAgent.getAverages()
        for i in range(days):
            tReward, mReward = localAgent.update(True)
            totalReward += tReward
            marketReward += mReward
        endAverages = localAgent.getAverages()

        learningTotal, learningMarketReward = totalReward, marketReward
        print("\n\n-------------------Results-------------------")
        print("Trial ", t + 1)
        print("Total Reward: ", learningTotal)
        print("Market Reward: ", learningMarketReward)

        totalReward = 0
        marketReward = 0

        localAgent.closeFiles()

main()
