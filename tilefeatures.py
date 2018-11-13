'''Contains a class for tile-coding continuous state variables, as described in Sutton and Barto.'''

import random

class TileFeatures:
    '''A class for generating tile-coding features.'''
    def __init__(self, ranges, numTiles, numTilings):
        '''Takes three parameters:
           ranges - a list/tuple of lists/tuples representing the range of values in the various dimensions. There should be one list/tuple per dimension with two elements, the minimum and maximum value, respectively
           numTiles - a list of integers indicating how many tiles each dimension should be broken into
           numTilings - many tilings to use (with randomly generated offsets)'''
        self.__ranges = ranges
        self.__numTiles = numTiles

        #Calculate how large tiles will be, based on the ranges and the tiling dimensions
        self.__tileDims = []        
        for i in range(len(self.__ranges)):
            self.__tileDims.append((self.__ranges[i][1]-self.__ranges[i][0])/self.__numTiles[i])

        #Determines the total number of tiles in each tiling
        self.__tilesPerTiling = 1
        for d in range(len(self.__numTiles)):
            self.__tilesPerTiling *= self.__numTiles[d]+1 #+1 because the random offset might push a state into the next tile outside the given range

        #Generate the offsets (a random number between 0 and 1 representing the portion of a tile to offset)
        self.__numTilings = numTilings       
        self.__offsets = []
        for i in range(self.__numTilings):
            self.__offsets.append(random.random())

    def getFeatures(self, state, lowestFeatureIndex=0):
        '''Returns the list of indices of features that are on (one for each tiling).'''
        activeFeatures = []
        for i in range(self.__numTilings):
            tile = 0
            for d in range(len(state)):
                tile *= self.__numTiles[d]+1
                offset = state[d]-self.__ranges[d][0]+self.__offsets[d]*(self.__tileDims[d]/2)
                tile += int(offset/self.__tileDims[d])
            activeFeatures.append(i*self.__tilesPerTiling + tile)
        return activeFeatures

    def getNumFeatures(self):
        '''Returns the total number of features.'''
        return self.__numTilings*self.__tilesPerTiling
