import random, pygame, time, numpy, math

# Size of each axis of the board
BOARD_SIZE = 20
WINDOW_SIZE = (1001, 1001 + 20)
STARTING_LENGTH = 3
# Moves each snake can make before removed from gene pool
MAX_MOVES_UNTIL_DEATH = 400
SQUARE_SIZE = (WINDOW_SIZE[0] - BOARD_SIZE - 1) / BOARD_SIZE
# Direction tuples for moving
UP, DOWN, LEFT, RIGHT = [0,1], [0,-1], [-1,0], [1,0]

def sigmoid(x):
    return 1/(1 + numpy.exp(-x))

class Snake:
    # instantiator
    def __init__(self, l, weightsList):
        self.length = l
        self.dead = False
        #initialX, initialY = random.randint(0,20), random.randint(0,20)
        self.spacesTaken = []
        for i in range(0, l):
            self.spacesTaken.append([int(BOARD_SIZE/2),int((BOARD_SIZE/2) - i)])
        """
        weightsList = [f1, f2, f3,f4, fb, l1, l2, l3,l4, lb, r1, r2, r3,r4, rb, c1, c2, c3]
        """
        self.weightsList = weightsList

        self.movesSinceLastFood = 0
        self.lastDirection = UP
        #self.generateBoard()
        self.foodPos = []
        self.addFood()

    def addFood(self):
        if len(self.spacesTaken) == BOARD_SIZE**2:
            print("You win!")
        self.foodPos = [random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)]
        while self.foodPos in self.spacesTaken:
            self.foodPos = [random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)]
        # Might want to add it to board or just not care about that oh well
    """
    def generateBoard(self):
        #board = []
        tempArray = [0 for i in range(BOARD_SIZE)]
        self.board = [tempArray for i in range(BOARD_SIZE)]
    """
    def goInDirection(self, direction):
        if -direction[0] == self.lastDirection[0] or direction[0] == self.lastDirection[0]:
            nextMove = [int(self.spacesTaken[0][0] + self.lastDirection[0]), int(self.spacesTaken[0][1] + self.lastDirection[1])]
            if nextMove[0] >= BOARD_SIZE or nextMove[1] > BOARD_SIZE - 1 or nextMove[0] < 0 or nextMove[1] < 0 or nextMove in self.spacesTaken[:len(self.spacesTaken) - 1]:
                self.die()
                return 1
            self.spacesTaken.insert(0, nextMove)
            if self.spacesTaken[0] != self.foodPos:
                self.spacesTaken.pop()
                self.movesSinceLastFood+=1
                return 0
            else:
                self.length += 1
                self.movesSinceLastFood = 0
                self.addFood()
                return 0
        else:
            nextMove = [int(self.spacesTaken[0][0] + direction[0]), int(self.spacesTaken[0][1] + direction[1])]
            if nextMove[0] >= BOARD_SIZE or nextMove[1] > BOARD_SIZE - 1 or nextMove[0] < 0 or nextMove[1] < 0 or nextMove in self.spacesTaken[:len(self.spacesTaken) - 1]:
                self.die()
                return 1
            self.spacesTaken.insert(0, nextMove)
            self.lastDirection = [direction[0], direction[1]]
            if self.spacesTaken[0] != self.foodPos:
                self.movesSinceLastFood+=1
                self.spacesTaken.pop()
                return 0
            else:
                self.length += 1
                self.movesSinceLastFood = 0
                self.addFood()
                return 0
    def die(self):
        self.dead = True

    def neuralNet(self, fWallDist, fSelfDist, rWallDist, rSelfDist, lWallDist, lSelfDist, foodDist, foodAngle):    # returns array of outputs
        f = self.weightsList[0] * foodAngle + self.weightsList[1] * fWallDist + self.weightsList[2] * fSelfDist + foodDist * self.weightsList[3] + self.weightsList[4]
        r = self.weightsList[5] * foodAngle + self.weightsList[6] * rWallDist + self.weightsList[7] * rSelfDist + foodDist * self.weightsList[8] + self.weightsList[9]
        l = self.weightsList[8] * foodAngle + self.weightsList[10] * lWallDist + self.weightsList[11] * lSelfDist + foodDist * self.weightsList[12] + self.weightsList[13]
        return [sigmoid(f), sigmoid(r), sigmoid(l)]

    def fitness(self):
        return (self.length - STARTING_LENGTH) * 20 + self.movesSinceLastFood/20
    def breed(self, snake):
        cutLoc = [random.randint(1,len(self.weightsList) - 2)]
        #get cut locations
        for cutnum in range(0, random.randint(6, len(self.weightsList) - 3)):
            newCutLoc = random.randint(1,len(self.weightsList) - 2)
            while newCutLoc in cutLoc:
                newCutLoc = random.randint(1,len(self.weightsList) - 2)
            cutLoc.append(newCutLoc)
        cutLoc.append(len(self.weightsList))
        cutLoc.sort()
        lastLoc = 0
        newWeights = []
        #splice
        for i in range(0,len(cutLoc)):
            if (i%2 == 0):
                newWeights += self.weightsList[lastLoc:cutLoc[i]]
            else:
                newWeights += snake.weightsList[lastLoc:cutLoc[i]]
            lastLoc = cutLoc[i]
        #mutate
        for i in range(0, random.randint(0, int(round(3 * sigmoid(-self.fitness()/40))))):
            newPlace = random.randint(0, len(newWeights) - 1)
            if newPlace > len(self.weightsList) - 4:
                newWeights[newPlace] = random.randint(0,255)
            else:
                newWeights[newPlace] = numpy.random.randn()

        if len(newWeights) != len(self.weightsList):
            print("BREEDING ALGORITHM BROKEN")
        return newWeights

    def play(self):
        foodDist = math.sqrt((self.foodPos[0] - self.spacesTaken[0][0])**2 + (self.foodPos[1] - self.spacesTaken[0][1])**2)
        if (self.lastDirection == UP):
            # up is forward
            # right is right
            # left is left
            foodAngle = math.atan2((self.foodPos[0] - self.spacesTaken[0][0]), (self.spacesTaken[0][1] - self.foodPos[1]))
            fWallDist = self.spacesTaken[0][1]
            fSelfDist = -200
            for i in range(self.spacesTaken[0][1] - 1, -1, -1):
                if [self.spacesTaken[0][0], i] in self.spacesTaken:
                    fSelfDist = self.spacesTaken[0][1] - i - 1
            rWallDist = BOARD_SIZE - self.spacesTaken[0][0]
            rSelfDist = -200
            for i in range(self.spacesTaken[0][0] + 1, 20):
                if [i, self.spacesTaken[0][1]] in self.spacesTaken:
                    rSelfDist = i - self.spacesTaken[0][0] - 1
            lWallDist = self.spacesTaken[0][0]
            lSelfDist = -200
            for i in range(self.spacesTaken[0][0] - 1, -1, -1):
                if [i, self.spacesTaken[0][1]] in self.spacesTaken:
                    lSelfDist = self.spacesTaken[0][0] - i - 1


        elif (self.lastDirection == DOWN):
            # down is forward
            # left is right
            # right is left
            foodAngle = math.atan2(self.spacesTaken[0][0] - self.foodPos[0], self.foodPos[1] - self.spacesTaken[0][1])
            fWallDist = BOARD_SIZE -1 - self.spacesTaken[0][1]
            fSelfDist = -200
            for i in range(self.spacesTaken[0][1] - 1, BOARD_SIZE):
                if [self.spacesTaken[0][0], i] in self.spacesTaken:
                    fSelfDist = i - self.spacesTaken[0][1] - 1
            rWallDist = self.spacesTaken[0][0]
            rSelfDist = -200
            for i in range(self.spacesTaken[0][0] - 1, -1, -1):
                if [i, self.spacesTaken[0][1]] in self.spacesTaken:
                    rSelfDist = self.spacesTaken[0][0] - i - 1
            lWallDist = BOARD_SIZE - self.spacesTaken[0][0]
            lSelfDist = -200
            for i in range(self.spacesTaken[0][0] + 1, 20):
                if [i, self.spacesTaken[0][1]] in self.spacesTaken:
                    lSelfDist = i - self.spacesTaken[0][0] - 1


        elif (self.lastDirection == LEFT):
            # left is forward
            # up is right
            # down is left
            foodAngle = math.atan2(self.spacesTaken[0][1] - self.foodPos[1], self.spacesTaken[0][0] - self.foodPos[0])
            fWallDist = self.spacesTaken[0][0]
            fSelfDist = -200
            for i in range(self.spacesTaken[0][0] - 1, -1, -1):
                if [i, self.spacesTaken[0][1]] in self.spacesTaken:
                    fSelfDist = self.spacesTaken[0][0] - i - 1
            rWallDist = self.spacesTaken[0][1]
            rSelfDist = -200
            for i in range(self.spacesTaken[0][1] - 1, -1, -1):
                if [self.spacesTaken[0][0], i] in self.spacesTaken:
                    rSelfDist = self.spacesTaken[0][1] - i - 1
            lWallDist = BOARD_SIZE - self.spacesTaken[0][0]
            lSelfDist = -200
            for i in range(self.spacesTaken[0][1] - 1, BOARD_SIZE):
                if [self.spacesTaken[0][0], i] in self.spacesTaken:
                    lSelfDist = i - self.spacesTaken[0][1] - 1

        elif (self.lastDirection == RIGHT):
            # right is forward
            # down is right
            # up is left
            foodAngle = math.atan2(self.foodPos[1] - self.spacesTaken[0][1], self.foodPos[0] - self.spacesTaken[0][0])
            fWallDist = BOARD_SIZE - self.spacesTaken[0][0]
            fSelfDist = -200
            for i in range(self.spacesTaken[0][0] + 1, 20):
                if [i, self.spacesTaken[0][1]] in self.spacesTaken:
                    fSelfDist = i - self.spacesTaken[0][0] - 1
            rWallDist = BOARD_SIZE -1 - self.spacesTaken[0][1]
            rSelfDist = -200
            for i in range(self.spacesTaken[0][1] - 1, BOARD_SIZE):
                if [self.spacesTaken[0][0], i] in self.spacesTaken:
                    rSelfDist = i - self.spacesTaken[0][1] - 1
            lWallDist = self.spacesTaken[0][1]
            lSelfDist = -200
            for i in range(self.spacesTaken[0][1] - 1, -1, -1):
                if [self.spacesTaken[0][0], i] in self.spacesTaken:
                    lSelfDist = self.spacesTaken[0][1] - i - 1
        #movement = self.neuralNet(sigmoid(fWallDist), sigmoid(fSelfDist), sigmoid(rWallDist), sigmoid(rSelfDist), sigmoid(lWallDist), sigmoid(lSelfDist), sigmoid(foodDist), sigmoid(foodAngle))
        movement = self.neuralNet(fWallDist, fSelfDist, rWallDist, rSelfDist, lWallDist, lSelfDist, foodDist, foodAngle)
        # sigmoid(f), sigmoid(r), sigmoid(l)
        if (movement[0] >= movement[1] and movement[0] >= movement[2]):
            self.goInDirection(self.lastDirection)
        elif (movement[1] >= movement[0] and movement[1] >= movement[2]):
            if self.lastDirection == UP:
                self.goInDirection(RIGHT)
            elif self.lastDirection == RIGHT:
                self.goInDirection(DOWN)
            elif self.lastDirection == LEFT:
                self.goInDirection(UP)
            elif self.lastDirection == DOWN:
                self.goInDirection(LEFT)
        elif (movement[2] >= movement[0] and movement[2] >= movement[1]):
            if self.lastDirection == UP:
                self.goInDirection(LEFT)
            elif self.lastDirection == RIGHT:
                self.goInDirection(UP)
            elif self.lastDirection == LEFT:
                self.goInDirection(DOWN)
            elif self.lastDirection == DOWN:
                self.goInDirection(RIGHT)
        #if not self.dead:
            #self.play()
        #else:
        if self.movesSinceLastFood == MAX_MOVES_UNTIL_DEATH:
            self.die()
        return self.fitness()
