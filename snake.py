import random, pygame, time
# Size of each axis of the board
BOARD_SIZE = 20
WINDOW_SIZE = (501, 501 + 20)
STARTING_LENGTH = 3
# Moves each snake can make before removed from gene pool
MAX_MOVES_UNTIL_DEATH = 200
SQUARE_SIZE = (WINDOW_SIZE[0] - BOARD_SIZE - 1) / BOARD_SIZE
# Direction tuples for moving
UP, DOWN, LEFT, RIGHT = (0,1), (0,-1), (-1,0), (1,0)

class Snake:
    # instantiator
    def __init__(self, l):
        self.length = l
        #initialX, initialY = random.randint(0,20), random.randint(0,20)
        self.spacesTaken = []
        for i in range(0, l):
            self.spacesTaken.append([BOARD_SIZE/2,(BOARD_SIZE/2) - i])

        self.movesSinceLastFood = 0
        self.lastDirection = [UP[0], UP[1]]
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
            nextMove = [self.spacesTaken[0][0] + self.lastDirection[0], self.spacesTaken[0][1] + self.lastDirection[1]]
            if nextMove[0] >= BOARD_SIZE or nextMove[1] > BOARD_SIZE - 1 or nextMove[0] < 0 or nextMove[1] < 0 or nextMove in self.spacesTaken[:len(self.spacesTaken) - 1]:
                self.die()
                return 1
            self.spacesTaken.insert(0, nextMove)
            if self.spacesTaken[0] != self.foodPos:
                self.spacesTaken.pop()
                return 0
            else:
                self.length += 1
                self.addFood()
                return 0
        else:
            nextMove = [self.spacesTaken[0][0] + direction[0], self.spacesTaken[0][1] + direction[1]]
            if nextMove[0] >= BOARD_SIZE or nextMove[1] > BOARD_SIZE - 1 or nextMove[0] < 0 or nextMove[1] < 0 or nextMove in self.spacesTaken[:len(self.spacesTaken) - 1]:
                self.die()
                return 1
            self.spacesTaken.insert(0, nextMove)
            self.lastDirection = [direction[0], direction[1]]
            if self.spacesTaken[0] != self.foodPos:
                self.spacesTaken.pop()
                return 0
            else:
                self.length += 1
                self.addFood()
                return 0
    def die(self):
        print("You lose")


    def fitness(self):
        return self.length * 20

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
s = Snake(STARTING_LENGTH)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
done = False
pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)
start = False

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
