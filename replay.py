from snake import Snake, sigmoid
import random, pygame, time, numpy, math, sys
# Size of each axis of the board
BOARD_SIZE = 20
WINDOW_SIZE = (1001, 1001 + 20)
STARTING_LENGTH = 3
# Moves each snake can make before removed from gene pool
MAX_MOVES_UNTIL_DEATH = 200
SQUARE_SIZE = (WINDOW_SIZE[0] - BOARD_SIZE - 1) / BOARD_SIZE
# Direction tuples for moving
UP, DOWN, LEFT, RIGHT = [0,1], [0,-1], [-1,0], [1,0]

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)



#try:
if len(sys.argv) > 1:
    weights = [float(x) for x in "".join(sys.argv[1:]).split(",")]
    for i in range(15,18):
        weights[i] = int(weights[i])
    s = Snake(STARTING_LENGTH, weights)
    done = False
    while not done:

        for event in pygame.event.get():    # whenever pygame recognizes an event (IE: mouse movement, clicking on the window x
            if event.type == pygame.QUIT:   # if user clicked the red box to close the window
                done = True

        screen.fill(WHITE)
        s.play()
        textSurface = myfont.render("Score: " + str(s.length - STARTING_LENGTH), False, BLACK)
        screen.blit(textSurface,(5,0))
        for row in range(0, BOARD_SIZE):
            for col in range(0, BOARD_SIZE):
                pygame.draw.rect(screen, BLACK, [(1 + SQUARE_SIZE) * col + 1, 20 + (1 + SQUARE_SIZE) * row + 1, SQUARE_SIZE, SQUARE_SIZE])

                if [col,row] in s.spacesTaken:
                    pygame.draw.rect(screen, (s.weightsList[15], s.weightsList[16], s.weightsList[17]), [(1 + SQUARE_SIZE) * col + 1, 20 + (1 + SQUARE_SIZE) * row + 1, SQUARE_SIZE, SQUARE_SIZE])
                else:
                    pygame.draw.rect(screen, BLACK, [(1 + SQUARE_SIZE) * col + 1, 20 + (1 + SQUARE_SIZE) * row + 1, SQUARE_SIZE, SQUARE_SIZE])
                if [col, row] == s.foodPos:
                    pygame.draw.circle(screen, RED, [int((1 + SQUARE_SIZE) * col + 1 + SQUARE_SIZE/2), int(20 + (1 + SQUARE_SIZE) * row + 1 + SQUARE_SIZE/2)], int(SQUARE_SIZE // 2))
        if s.dead:
            if s.length - STARTING_LENGTH > 0:
                print("Got score of " + str(s.length - STARTING_LENGTH))
            s = Snake(STARTING_LENGTH, weights)
        time.sleep(0.05)
        pygame.display.flip()
else:
    print("Need gene array (no brackets)")
