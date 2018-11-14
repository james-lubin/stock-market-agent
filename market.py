



class Market:

    def __init__(self,data):
        self.numFeatures = 1
        ##positions should be a list of positions
        self.positions = self.createMarket(positionNames)
        self.data = data
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
        self.pTag = file.split(".")[0]

        txtFile = open("/data/Stocks/"+self.fileName,"r")
        txtList = txtFile.readlines()

        self.dayIndex = 0


        line  = txtList[self.dayIndex]
        date = line.split(",")[0]
        while(line!="2015-01-27"):
            self.dayIndex+=1
            line = txtList[self.dayIndex]
            date = line.split(",")[0]
            
        #print(positionData[1])
        self.currentPrice = txtFile[self.dayIndex].split(",")[1]
        '''we will need to add a list of more features'''

    def getCurrentPrice(self):
        print(self.currentPrice)
        return self.currentPrice

    def update(self):
        self.dayIndex+=1
        self.currentPrice = txtFile[self.dayIndex].split(",")[1]




    


