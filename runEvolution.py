from snake import Snake, sigmoid
import random, pygame, time, numpy, math

# Size of each axis of the board
BOARD_SIZE = 20
WINDOW_SIZE = (1001, 1001 + 20)
STARTING_LENGTH = 3
# Moves each snake can make before removed from gene pool
MAX_MOVES_UNTIL_DEATH = 200
SQUARE_SIZE = (WINDOW_SIZE[0] - BOARD_SIZE - 1) / BOARD_SIZE
# Direction tuples for moving
UP, DOWN, LEFT, RIGHT = [0,1], [0,-1], [-1,0], [1,0]

"""
weightsList = [f1, f2, f3,f4, fb, l1, l2, l3,l4, lb, r1, r2, r3,r4, rb, c1, c2, c3]
"""
output = open("output.txt", "a")
generation = 0
snakeList = []
for i in range(0,40):
    weights = []
    for i in range(0,18):
        if i <= 14:
            weights.append(numpy.random.randn())
        else:
            weights.append(random.randint(0,255))
    snakeList.append(Snake(STARTING_LENGTH, weights))




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
highScore = 0

while not done:

    moved = False
    genDead = True
    for snake in snakeList:
        if not snake.dead:
            genDead = False
    if genDead:
        generation += 1
        bestFitness = [0, 0]
        for i in range(0,len(snakeList)):
            if snakeList[i].fitness() > bestFitness[0]:
                bestFitness = [snakeList[i].fitness(), i]
            if snakeList[i].length - STARTING_LENGTH > highScore:
                output.write("Score: " + str(snakeList[i].length - STARTING_LENGTH) + "\n" + str(snakeList[i].weightsList) + "\n")
                print("New high score: " + str(snakeList[i].length - STARTING_LENGTH))
                highScore = snakeList[i].length - STARTING_LENGTH
        newSnakeList = [Snake(STARTING_LENGTH, snakeList[bestFitness[1]].weightsList)]
        for i in range(0,len(snakeList)):
            if i != bestFitness[1]:
                newSnakeList.append(Snake(STARTING_LENGTH, snakeList[bestFitness[1]].breed(snakeList[i])))
        snakeList = newSnakeList


    #TODO fix events being queued instead of executing last movement to frame
    for event in pygame.event.get():    # whenever pygame recognizes an event (IE: mouse movement, clicking on the window x
        if event.type == pygame.QUIT:   # if user clicked the red box to close the window
            done = True
            output.close()

    """
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
    """

    screen.fill(WHITE)
    for snake in snakeList:
        snake.play()
    #textSurface = myfont.render("Score: " + str(s.length - STARTING_LENGTH), False, BLACK)
    #screen.blit(textSurface,(5,0))
    for row in range(0, BOARD_SIZE):
        for col in range(0, BOARD_SIZE):
            pygame.draw.rect(screen, BLACK, [(1 + SQUARE_SIZE) * col + 1, 20 + (1 + SQUARE_SIZE) * row + 1, SQUARE_SIZE, SQUARE_SIZE])

            #if [col,row] in s.spacesTaken:
                #pygame.draw.rect(screen, GREEN, [(1 + SQUARE_SIZE) * col + 1, 20 + (1 + SQUARE_SIZE) * row + 1, SQUARE_SIZE, SQUARE_SIZE])
            #else:
                #pygame.draw.rect(screen, BLACK, [(1 + SQUARE_SIZE) * col + 1, 20 + (1 + SQUARE_SIZE) * row + 1, SQUARE_SIZE, SQUARE_SIZE])
            #if [col, row] == s.foodPos:
                #pygame.draw.circle(screen, RED, [int((1 + SQUARE_SIZE) * col + 1 + SQUARE_SIZE/2), int(20 + (1 + SQUARE_SIZE) * row + 1 + SQUARE_SIZE/2)], int(SQUARE_SIZE // 2))
    for snake in snakeList:
        if not snake.dead:
            for position in snake.spacesTaken:
                pygame.draw.rect(screen, (snake.weightsList[15], snake.weightsList[16], snake.weightsList[17]), [(1 + SQUARE_SIZE) * position[0] + 1, 20 + (1 + SQUARE_SIZE) * position[1] + 1, SQUARE_SIZE, SQUARE_SIZE])
            pygame.draw.circle(screen, (snake.weightsList[15], snake.weightsList[16], snake.weightsList[17]), [int((1 + SQUARE_SIZE) * snake.foodPos[0] + 1 + SQUARE_SIZE/2), int(20 + (1 + SQUARE_SIZE) * snake.foodPos[1] + 1 + SQUARE_SIZE/2)], int(SQUARE_SIZE // 2))
    pygame.display.flip()
