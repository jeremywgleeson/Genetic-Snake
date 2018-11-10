import random, pygame, time, numpy, math
# Size of each axis of the board
BOARD_SIZE = 20
WINDOW_SIZE = (501, 501 + 20)
STARTING_LENGTH = 3
# Moves each snake can make before removed from gene pool
MAX_MOVES_UNTIL_DEATH = 200
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
        if self.movesSinceLastFood > 0:
            return (self.length - STARTING_LENGTH) * 20 + 5/self.movesSinceLastFood
        else:
            return (self.length - STARTING_LENGTH) * 20 + 5
    def breed(self, snake):
        cutLoc = [random.randint(1,len(self.weightsList) - 2)]
        #get cut locations
        for cutnum in range(0, random.randint(3, len(self.weightsList) - 3)):
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
        for i in range(0, random.randint(0, int(round(10 * sigmoid(-self.fitness()/20))))):
            newPlace = random.randint(0, len(newWeights) - 1)
            if newPlace > len(self.weightsList) - 3:
                newWeights[newPlace] = random.randint(0,255)
            else:
                newWeights[newPlace] = numpy.random.randn()

        if len(newWeights) != len(self.weightsList):
            print("BREEDING ALGORITHM BROKEN")
        return newWeights

    def play(self):
        done = False
        foodDist = math.sqrt((self.foodPos[0] - self.spacesTaken[0][0])**2 + (self.foodPos[1] - self.spacesTaken[0][1])**2)
        foodAngle = math.degrees(math.atan2((self.foodPos[0] - self.spacesTaken[0][0]), (self.foodPos[1] - self.spacesTaken[0][1])))
        if (self.lastDirection == UP):
            # up is forward
            # right is right
            # left is left
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
        movement = self.neuralNet(sigmoid(fWallDist), sigmoid(fSelfDist), sigmoid(rWallDist), sigmoid(rSelfDist), sigmoid(lWallDist), sigmoid(lSelfDist), sigmoid(foodDist), sigmoid(foodAngle))
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
        for event in pygame.event.get():    # whenever pygame recognizes an event (IE: mouse movement, clicking on the window x
            if event.type == pygame.QUIT:   # if user clicked the red box to close the window
                done = True
        screen.fill(WHITE)
        textSurface = myfont.render("Score: " + str(s.length - STARTING_LENGTH), False, BLACK)
        screen.blit(textSurface,(5,0))
        for row in range(0, BOARD_SIZE):
            for col in range(0, BOARD_SIZE):
                if [col,row] in self.spacesTaken:
                    pygame.draw.rect(screen, (self.weightsList[15], self.weightsList[16], self.weightsList[17]), [(1 + SQUARE_SIZE) * col + 1, 20 + (1 + SQUARE_SIZE) * row + 1, SQUARE_SIZE, SQUARE_SIZE])
                else:
                    pygame.draw.rect(screen, BLACK, [(1 + SQUARE_SIZE) * col + 1, 20 + (1 + SQUARE_SIZE) * row + 1, SQUARE_SIZE, SQUARE_SIZE])
                if [col, row] == self.foodPos:
                    #TODO fix drawing this on the wrong area
                    pygame.draw.circle(screen, RED, [int((1 + SQUARE_SIZE) * col + 1 + SQUARE_SIZE/2), int(20 + (1 + SQUARE_SIZE) * row + 1 + SQUARE_SIZE/2)], int(SQUARE_SIZE // 2))
        pygame.display.flip()
        time.sleep(0.5)
        if not self.dead and not done:
            self.play()
        else:
            print(self.fitness())




"""
weightsList = [f1, f2, f3,f4, fb, l1, l2, l3,l4, lb, r1, r2, r3,r4, rb, c1, c2, c3]
"""
weights = []
for i in range(0,18):
    if i <= 14:
        weights.append(numpy.random.randn())
    else:
        weights.append(random.randint(0,255))
print("Original Snake: " + str(weights))
s = Snake(STARTING_LENGTH, weights)




pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
done = False
pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)
start = False
s.play()
"""
while not done:
    time.sleep(0.1)
    moved = False
    #TODO fix events being queued instead of executing last movement to frame
    for event in pygame.event.get():    # whenever pygame recognizes an event (IE: mouse movement, clicking on the window x
        if event.type == pygame.QUIT:   # if user clicked the red box to close the window
            done = True

        elif event.type == pygame.KEYDOWN and not moved:
            start = True
            if event.key == pygame.K_LEFT:
                if s.goInDirection(LEFT) == 1:
                    done = True
                moved = True
                pygame.event.clear()
            elif event.key == pygame.K_UP:
                if s.goInDirection(DOWN) == 1:
                    done = True
                pygame.event.clear()
                moved = True
            elif event.key == pygame.K_DOWN:
                if s.goInDirection(UP) == 1:
                    done = True
                pygame.event.clear()
                moved = True
            elif event.key == pygame.K_RIGHT:
                if s.goInDirection(RIGHT) == 1:
                    done = True
                pygame.event.clear()
                moved = True

    if not moved and start:
        if s.goInDirection(s.lastDirection) == 1:
            done = True


    screen.fill(WHITE)
    textSurface = myfont.render("Score: " + str(s.length - STARTING_LENGTH), False, BLACK)
    screen.blit(textSurface,(5,0))
    for row in range(0, BOARD_SIZE):
        for col in range(0, BOARD_SIZE):
            if [col,row] in s.spacesTaken:
                pygame.draw.rect(screen, GREEN, [(1 + SQUARE_SIZE) * col + 1, 20 + (1 + SQUARE_SIZE) * row + 1, SQUARE_SIZE, SQUARE_SIZE])
            else:
                pygame.draw.rect(screen, BLACK, [(1 + SQUARE_SIZE) * col + 1, 20 + (1 + SQUARE_SIZE) * row + 1, SQUARE_SIZE, SQUARE_SIZE])
            if [col, row] == s.foodPos:
                #TODO fix drawing this on the wrong area
                pygame.draw.circle(screen, RED, [int((1 + SQUARE_SIZE) * col + 1 + SQUARE_SIZE/2), int(20 + (1 + SQUARE_SIZE) * row + 1 + SQUARE_SIZE/2)], int(SQUARE_SIZE // 2))
    pygame.display.flip()
    """
