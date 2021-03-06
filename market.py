import os

class Market:
    def __init__(self, p):
        positionNames = p
        self.positionTable = {}
        self.positions = self.createMarket(p) #a list of positions
        self.numFeatures = 1
        self.day = 0
        self.activeFeatures = []

    def createMarket(self,data):
        p = []
        for line in data:
            #positionName = line[0]
            file = line.replace("\n", "")
            newPosition = Position(file)
            p.append(newPosition)
            self.positionTable[newPosition.getTicker()] = newPosition

        return p

    def getPositions(self):
        return self.positions

    def getPosition(self, index):
        return self.positions[index]

    def getPositionByTicker(self, ticker):
        return self.positionTable[ticker]

    def updateMarket(self):
        '''Increment the day and now use the data from the newest day'''
        self.activeFeatures = []
        for i in range(len(self.positions)):
            self.positions[i].update() #update position's features
            self.activeFeatures.append(self.positions[i].getPositionActiveFeatures())

    def getActiveFeatures(self):
        return self.activeFeatures

class Position:
    def __init__(self, file):
        self.fileName = file
        self.pTag = file.split(".")[0] #TODO: change more descriptive name
        self.txtFile = open("Data\\Stocks\\" + self.fileName + ".txt", "r")
        self.txtList = self.txtFile.readlines()
        self.ticker = self.fileName.split(".")[0] #split off the .us that follows all the ticker names
        self.startDate = "2012-01-03"

        self.dayIndex = 0
        self.currentSentiment = 0

        line  = self.txtList[self.dayIndex]
        date = line.split(",")[0]
        self.last52 = []

        while(line != self.startDate):
            self.dayIndex += 1
            line = self.txtList[self.dayIndex]
            splitLine = line.split(",")
            self.currentPrice = float(splitLine[1])
            self.last52.append(self.currentPrice)
            if(len(self.last52) >= 53):
                self.last52.pop(0)
            #print(line)
            line = splitLine[0]

        self.lastWeekSum = sum(self.last52[-7:])
        self.lastWeekAvg = self.lastWeekSum / 5
        self.yesterdayValue = self.last52[-2]
        self.last52Sum = sum(self.last52)
        self.last52Avg = self.last52Sum / 260
        self.currentPrice = float(self.txtList[self.dayIndex].split(",")[1])

    def getCurrentPrice(self):
        return self.currentPrice

    def getTicker(self):
        return self.ticker

    def updateSentiment(self):
        news = self.getNews() #returns a list of string of current relevent news articles
        totalSentiment = 0
        for article in news:
            sentiment = "Y" #simpleSentimentAnalyzer(headline)

            if(sentiment == "positive"):
                totalSentiment += 1
            elif(sentiment == "negative"):
                totalSentiment += -1

        self.currentSentiment = totalSentiment/len(news)

    def getSentiment(self):
        return self.currentSentiment

    def getPositionActiveFeatures(self):
        features = []
        if(self.below52Week()):
            features.append(0)
        if(self.belowWeek()):
            features.append(1)
        if(self.belowYesterday()):
            features.append(2)

        return features

    def update(self):
        old52 = self.last52[0]
        weeklyOldestDay = self.last52[0]
        self.last52.pop(0)

        self.dayIndex += 1
        #self.updateSentiment()
        #print(self.ticker)
        #print(self.txtList[-1])
        #print(self.txtList[self.dayIndex-1])
        #print("len :"+str(len(self.txtList)))
        #print(self.dayIndex)
        self.currentPrice = float(self.txtList[self.dayIndex].split(",")[1])
        self.last52.append(float(self.currentPrice))

        self.last52Sum = self.last52Sum - old52 + self.currentPrice
        self.last52Avg = self.last52Sum / 260
        self.lastWeekSum = self.lastWeekSum - weeklyOldestDay + self.getCurrentPrice()
        self.lastWeekAvg = self.lastWeekSum / 5

    def getNews(self):
        #TODO: makre variables more readable
        #self.news.getHeadlines(self.pTag, 3, self.txtList[self.dayIndex - 7].split(",")[0], self.txtList[self.dayIndex].split(",")[0])
        return self.news.getHeadlines(self.pTag, 3, "2018-10-21", "2018-10-28")

    def below52Week(self):
        if(self.last52Avg < self.currentPrice):
            return True
        else:
            return False

    def belowWeek(self):
        if(self.lastWeekAvg < self.currentPrice):
            return True
        else:
            return False

    def belowYesterday(self):
        if(self.yesterdayValue < self.currentPrice):
            return True
        else:
            return False

    def closeFile(self):
        txtFile.close()
