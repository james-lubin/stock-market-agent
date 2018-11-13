import agent
import market
import sys

def main():
    filename = sys.argv[1]
    txtFile = open(filename,"r")
    lines = txtFile.readlines()

    '''for line in lines: read files if need be,  currently data needs to be in
    the format of a list of lines where each line is
    a new day (see example trainingset)'''

    data = lines
    m = market.Market(data)
    ag = agent.Agent(m)

    ag.update()

main()
