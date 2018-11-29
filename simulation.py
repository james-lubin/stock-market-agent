import agent
import market
import sys

def main():
    filename = sys.argv[1]
    days = int(sys.argv[2])

    txtFile = open(filename, "r")

    lines = txtFile.readlines()

    data = lines
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
    print("Learning phase ended!------------------------------------------\n\n\n")

    totalReward = 0
    marketReward = 0
    '''secStartAverages = localAgent.getAverages()
    for i in range(days):
        tReward, mReward = localAgent.update(False)
        totalReward += tReward
        marketReward += mReward
    secEndAverages = localAgent.getAverages()'''

    learningAverages = []
    learnedAverages = []
    for i in range(len(startAverages)):
        learningAverages.append((endAverages[i] - startAverages[i]) / startAverages[i])
        #learnedAverages.append((secEndAverages[i] - secStartAverages[i]) / secStartAverages[i])

    marketAverage = sum(learningAverages) / len(learningAverages)
    #secMarketAvg = sum(learnedAverages) / len(learnedAverages)

    print("\n\n\n---Averages---  ", "Agent", "\t\t\t", "Market")
    print("Learning Phase: ", learningTotal, "\t", (marketAverage * 100))
    #print("Learned  Phase: ", totalReward, "\t", (secMarketAvg * 100), "\n")
    localAgent.closeFiles()

def testStuff():
    testSentence = "I hate everything, it all sucks"
    res = localAgent.analyzeHeadline(testSentence)
    print("Sentence: ", testSentence, "\tSentiment: ", res)

    #news testing
    myNews = news.News()
    print(myNews.getHeadlines("Microsoft", 5, "2018-10-14", "2018-10-21"))

main()
