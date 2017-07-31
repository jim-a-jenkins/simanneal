import sys
import random
import math
import copy

#myText = open(sys.argv[1])
myText = open("largeState.txt") #HARDCODED sample data file

myLines = myText.read().split('\n')

Matrix = [ [ 0 for i in range(len(myLines)) ] for j in range(len(myLines)) ]

numRabbits = 0
numDragons = 0


for i in range(0,len(myLines)):
    currentLine = myLines[i]
    j = 0
    while j < len(myLines)*2-1:
        if currentLine[j] is ' ':
            j+=1
        else:
            Matrix[i][j/2] = currentLine[j]
            if currentLine[j] is 'D':
                numDragons += 1
            elif currentLine[j] is 'R':
                numRabbits += 1
            j+=1

gridSize = float(len(myLines)*len(myLines))

'''
****** CREATE INITIAL DISTRICT MATRIX ******
'''


initMatrix = [ [ 0 for i in range(len(myLines)) ] for j in range(len(myLines)) ]
for i in range(len(myLines)):
    for j in range(len(myLines)):
        initMatrix[i][j] = i+1



'''
****** DISTRICT MATRIX CHECKER ******
'''

def matrixCheck(theMatrix):
    global checked
    checked = [ [ False for i in range(len(myLines)) ] for j in range(len(myLines)) ]
    districtComplete = [False] * len(myLines)
    for i in range(0, len(myLines)):
        for j in range(0, len(myLines)):
            def markAsChecked(i, j):
                checked[i][j] = True
                if i - 1 >= 0:                                  #check NORTH
                    if theMatrix[i][j] == theMatrix[i-1][j] and checked[(i-1)][j] != True:
                        markAsChecked((i-1),j)
                if j + 1 < len(myLines):                                   #check EAST
                    if theMatrix[i][j] == theMatrix[i][j+1] and checked[i][(j+1)] != True:
                        markAsChecked(i,(j+1))
                if i + 1 < len(myLines):                                   #check SOUTH
                    if theMatrix[i][j] == theMatrix[i+1][j] and checked[(i+1)][j] != True:
                        markAsChecked((i+1),j)
                if j - 1 >= 0:                                   #check SOUTH
                    if theMatrix[i][j] == theMatrix[i][j-1] and checked[i][(j-1)] != True:
                        markAsChecked(i,j-1)
                return
            if checked[i][j] == False and districtComplete[(theMatrix[i][j])-1] == True:
                return False
            elif checked[i][j] == False and districtComplete[(theMatrix[i][j])-1] == False:
                markAsChecked(i,j)
                districtComplete[(theMatrix[i][j]) - 1] = True
    return True


def prettyPrintMatrix(theMatrix):
    for i in range(0,len(myLines)):
        print theMatrix[i]


def districtScore(distMatrix):
    tally = [0] * len(myLines)
    for i in range(0, len(myLines)):
        for j in range(0, len(myLines)):
            if Matrix[i][j] == 'D':
                tally[(distMatrix[i][j])-1] += 1
            if Matrix[i][j] == 'R':
                tally[(distMatrix[i][j])-1] -= 1
    dScore = 0
    rScore = 0
    for i in range(0, len(myLines)):
        if tally[i] > 0:
            dScore += 1
        if tally[i] < 0:
            rScore += 1
    return (dScore/float(len(myLines))),(rScore/float(len(myLines)))

def newSolution(distMatrix):
    newSol = copy.deepcopy(distMatrix)
    validSolution = False
    while validSolution == False:
        randA = random.randint(0,len(myLines)-1)
        randB = random.randint(0,len(myLines)-1)
        randX = random.randint(0,len(myLines)-1)
        randY = random.randint(0,len(myLines)-1)
        if newSol[randA][randB] != newSol[randX][randY]:
            swapVar = newSol[randA][randB]
            newSol[randA][randB] = newSol[randX][randY]
            newSol[randX][randY] = swapVar
            if matrixCheck(newSol) == True:
                validSolution = True
            else:
                unswapVar = newSol[randA][randB]
                newSol[randA][randB] = newSol[randX][randY]
                newSol[randX][randY] = unswapVar
    return newSol

def solutionQuality(solutionMatrix):
    dragonsDiff = abs(districtScore(solutionMatrix)[0]-(numDragons/gridSize))
    rabbitsDiff = abs(districtScore(solutionMatrix)[1]-(numDragons/gridSize))
    return dragonsDiff + rabbitsDiff

def acceptProb(sol1, sol2, T):
    acceptance = math.exp(-(solutionQuality(sol2)-solutionQuality(sol1))/T)
    return acceptance

def simAnneal(initial):
    statesExplored = 0
    oldMatrix = initial
    oldScore = solutionQuality(initial)
    T = 1.0
    Tmin = 0.0005
    alpha = 0.9
    while T > Tmin:
        i = 0
        while i <= 10:
            statesExplored += 1
            newSol = newSolution(oldMatrix)
            accept = acceptProb(oldMatrix, newSol, T)
            if accept > random.random():
                oldMatrix = newSol
                oldScore = solutionQuality(newSol)
            i += 1
        T = T*alpha
    return oldMatrix, statesExplored



'''
****** RESULTS ******
'''
print "Calculating. Please wait..."
print ""

myResult = simAnneal(initMatrix)
myMatrix = myResult[0]
myStates = myResult[1]

districtWinners = [0]*len(myLines)

for i in range(len(myLines)):
    for j in range(len(myLines)):
        if Matrix[i][j] == 'D':
            districtWinners[(myMatrix[i][j])-1] += 1

majorityD = 0
majorityR = 0

for i in range(len(myLines)):
    if districtWinners[i] < (len(myLines))/2:
        majorityR += 1
    if districtWinners[i] > (len(myLines))/2:
        majorityD += 1


print "Party division in popluation:"
print "*************************************"
print 'R:', (numRabbits/gridSize)*100, '%'
print 'D:', (numDragons/gridSize)*100, '%'
print "*************************************"

print ""

print "Number of districts with a majority for each party"
print "*************************************"
print "R:", majorityR
print "D:", majorityD
print "*************************************"

print ""

print "Locations assigned to each district:"
print "*************************************"

districtGuide = {}
for i in range(len(myLines)):
    districtGuide[i] = []

for i in range(len(myLines)):
    for j in range(len(myLines)):
        dist = myMatrix[i][j] - 1
        location = i,j
        districtGuide[dist].append(location)

for i in range(len(myLines)):
    print "District", i+1, ":", districtGuide[i]

print "*************************************"
print ""

print "*************************************"
print "Algorithm applied: SA"
print "*************************************"

print ""
print "*************************************"
print "Number of search states explored:", myStates
print "*************************************"

print ""
print "*************************************"
print "Additional Information: Map of districts"
prettyPrintMatrix(myMatrix)
print "*************************************"
print ""