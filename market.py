import os
import simpleSentimentAnalyzer
class Market:

    def __init__(self, p):
        positionNames =p
        print("\\n")
        self.positions = self.createMarket(p)
        self.numFeatures = 1
        ##positions should be a list of positions
        
        self.day = 0
        

    def createMarket(self,data):
        p = []
        #line = data[0]
        #line = line[0:-1].split("\t")
        '''
        print(line)
        for i in range(0,len(line),2):
            name = line[i]
            currentPrice = line[i+1]

            p.append(Position([name,currentPrice]))
        '''
        for line in data:
            #positionName = line[0]
            file = line.replace("\n","")
            p.append(Position(file))
            '''
            for i in range(1,numFeatures+1):
                feature = line[i]
                p[positionName].append(feature)
            '''
            
        
        return p

    def getPositions(self):
        return self.positions

    def getPosition(self,index):
        return self.positions[index]

    def updateMarket(self):
        '''Increment the day and now use the data from the newest day'''
        for i in range(len(self.positions)):
            self.positions[i].update() #update position's features

        return 0


class Position:
    def __init__(self,file):
        self.fileName = file
        #print(os.path.join(os.path.abspath(__file__), "\\Data\\Stocks\\"+self.fileName))
        self.pTag = file.split(".")[0]
        print(os.path.abspath(__file__)+"\\Data\\Stocks\\"+self.fileName)
        txtFile = open("Data\\Stocks\\"+self.fileName+".txt","r")
        txtList = txtFile.readlines()

        self.dayIndex = 0
        self.currentSentiment = 0


        line  = txtList[self.dayIndex]
        date = line.split(",")[0]
        while(line!="2015-01-27"):
            self.dayIndex+=1
            line = txtList[self.dayIndex]
            #print(line)
            line = line.split(",")[0]
            
        #print(positionData[1])
        self.currentPrice = txtList[self.dayIndex].split(",")[1]
        '''we will need to add a list of more features'''

    def getCurrentPrice(self):
        print(self.currentPrice)
        return self.currentPrice

    def updateSentiment(self):
        news = self.getNews() #returns a list of string of current relevent news articles
        totalSentiment = 0
        for article in news:
            sentiment = simpleSentimentAnalyzer(headline)

            if(sentiment=="positive"):
                totalSentiment+=1
            elif(sentiment=="negative"):
                totalSentiment+=-1

        self.currentSentiment = totalSentiment/len(news)

    def getSentiment(self):
        return self.currentSentiment

    def update(self):
        self.dayIndex+=1
        self.updateSentiment()
        self.currentPrice = txtFile[self.dayIndex].split(",")[1]

    def getNews(self):
        return ["Help"]




    


