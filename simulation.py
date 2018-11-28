import agent
import market
import sys

def main():

    filename = sys.argv[1]
    days = int(sys.argv[2])

    txtFile = open(filename,"r")

    lines = txtFile.readlines()

    #for line in lines: read files if need be,  currently data needs to be in
    #the format of a list of lines where each line is a new day (see example trainingset)

    data = lines
    localMarket = market.Market(data)
    localAgent = agent.Agent(localMarket)

    totalReward = 0
    marketReward = 0
    for i in range(days):
        tReward, mReward = localAgent.update(True)
        totalReward += tReward
        marketReward += mReward

    learningTotal, learningMarketReward = totalReward, marketReward
    print("Learning phase ended!------------------------------------------\n\n\n")

    totalReward = 0
    marketReward = 0
    for i in range(days):
        tReward, mReward = localAgent.update(False)
        totalReward+=tReward
        marketReward += mReward

    print("Learning Phase: ", learningTotal, learningMarketReward)
    print("Learned Phase: ", totalReward, marketReward)
    print(localAgent.getQVal())

def testStuff():
    testSentence = "I hate everything, it all sucks"
    res = localAgent.analyzeHeadline(testSentence)
    print("Sentence: ", testSentence, "\tSentiment: ", res)

    #news testing
    myNews = news.News()
    print(myNews.getHeadlines("Microsoft", 5, "2018-10-14", "2018-10-21"))

main()
