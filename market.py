



class Market:

    def __init__(self,data):
        self.numFeatures = 1
        ##positions should be a list of positions
        self.positions = self.createMarket(data)
        self.data = data
        self.day = 0
        

    def createMarket(self,data):
        p = []
        line = data[0]
        line = line[0:-1].split("\t")
        
        print(line)
        for i in range(0,len(line),2):
            name = line[i]
            currentPrice = line[i+1]

            p.append(Position([name,currentPrice]))
        '''
        for line in data:
            #positionName = line[0]
            p.append(Position(line))
             
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
        self.day+=1
        line  = self.data[self.day][0:-1].split("\t")

        for i in range(0,len(line),2):
            name = line[i]
            currentPrice = line[i+1]

            self.positions[i/2].update([name,currentPrice]) #update position's features
        return 0


class Position:
    def __init__(self,positionData):
        self.pName = positionData[0]
        print(positionData[1])
        self.currentPrice = positionData[1]
        '''we will need to add a list of more features'''

    def getCurrentPrice(self):
        print(self.currentPrice)
        return self.currentPrice

    def update(self,newDay):
        self.currentPrice = int(newDay[1])




    


