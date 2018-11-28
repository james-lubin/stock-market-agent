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

    for j in range(10):
        localMarket = market.Market(data)
        localAgent = agent.Agent(localMarket)


        totalReward = 0
        marketReward = 0
        startAverages = localAgent.getAverages()
        for i in range(days):
            tReward, mReward = localAgent.update(True)
            totalReward+=tReward
            marketReward += mReward
            #print("Day: ", i)
        endAverages = localAgent.getAverages()
        #print(startAverages)

        #print(endAverages)
        learningTotal, learningMarketReward = totalReward, marketReward
        #print("Learning phase ended!------------------------------------------\n\n\n")

        totalReward = 0
        marketReward = 0
        start1Averages = localAgent.getAverages()
        for i in range(days):
            tReward, mReward = localAgent.update(False)
            totalReward+=tReward
            marketReward += mReward
            #print("Day: ", i)
        end1Averages = localAgent.getAverages()

        learningAverages = []
        learnedAverages = []
        for i in range(len(startAverages)):
            learningAverages.append((endAverages[i]-startAverages[i])/startAverages[i])
            learnedAverages.append((end1Averages[i]-start1Averages[i])/start1Averages[i])

        #print(learningAverages)
        marketAverage = sum(learningAverages)/len(learningAverages)
        marketAverage1=  sum(learnedAverages)/len(learnedAverages)

        print("Learnin Phase: "+ ","+str(learningTotal)+"," +str(marketAverage*100))
        print("Learned Phase: "+","+str(totalReward)+","+ str(marketAverage1*100)+"\n")
        #print(localAgent.getQVal())


main()
