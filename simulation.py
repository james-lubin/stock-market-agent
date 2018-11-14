import agent
import market
import sys
import news

def main():
    filename = sys.argv[1]
    txtFile = open(filename,"r")
    lines = txtFile.readlines()

    '''for line in lines: read files if need be,  currently data needs to be in
    the format of a list of lines where each line is
    a new day (see example trainingset)'''

    data = lines
    localMarket = market.Market(data)
    localAgent = agent.Agent(localMarket)

    #agent.update()
    testSentence = "I hate everything, it all sucks"
    res = localAgent.analyzeHeadline(testSentence)
    print("Sentence: ", testSentence, "\tSentiment: ", res)

    #news testing
    myNews = news.News()
    print(myNews.getHeadlines("Microsoft", 5, "2018-10-14", "2018-10-21"))


main()
