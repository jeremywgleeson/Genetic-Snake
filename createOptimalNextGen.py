import sys
NUMBER_OF_SNAKES = 40
if len(sys.argv) > 2:
    inputFile = open(sys.argv[1], "r")
    #assumes last line is blank and there are no blank lines
    lines = [line[:-1] for line in inputFile]
    inputFile.close()
    bestSnakes = []
    bestScore = 0
    for snake in lines:
        if int(snake.split(":")[0]) > bestScore:
            bestScore = int(snake.split(":")[0])
    for score in range(bestScore, 0, -1):
        for snake in lines:
            if int(snake.split(":")[0]) == score and len(bestSnakes) < NUMBER_OF_SNAKES:
                currentWeights = snake.split(":")[1][1:-1].split(", ")
                newWeights = []
                for i in range(0, len(currentWeights)):
                    if i <= 14:
                        newWeights.append(float(currentWeights[i]))
                    else:
                        newWeights.append(int(currentWeights[i]))
                bestSnakes.append(newWeights)
    #print("Len: " + str(len(bestSnakes)) + "\n" +  "Len weights: " + str(len(bestSnakes[0]))+ "\n" + str(bestSnakes))
    outputFile = open(sys.argv[2], "a")
    outputFile.write(str(bestSnakes) + "\n")
    outputFile.close()
else:
    print("Need input and output file")
