import math

# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console?page=1&tab=votes#tab-top
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


# length of vector
def length(v):
    return math.sqrt(v[0]**2 + v[1]**2)


# angle between two vectors
def getAngle(v1, v2):
    ln = length(v1) * length(v2)
    ct = (v1[0] * v2[0] + v1[1] * v2[1])
    return ct / ln


data = [i for i in open("data.txt", 'r').readlines()]

height = len(data)
width = len(data[height - 1])

asteroidsCoords = []

# get coordinates of asteroids
for y in range(height):
    for x in range(height):
        if data[y][x] == '#':
            asteroidsCoords.append((x, y))

# make vector based on each asteroid (start) and other asteroids (end)
vectors = []
for suspectedStation in asteroidsCoords:

    tempAsteroidCoords = asteroidsCoords[:]
    tempAsteroidCoords.remove(suspectedStation)

    temp = []

    for asteroid in tempAsteroidCoords:
        temp.append((asteroid[0] - suspectedStation[0],
                     asteroid[1] - suspectedStation[1]))

    vectors.append(temp)

countDetections = [0] * (len(vectors[0]) + 1)
i = 0
l = len(vectors)
printProgressBar(0, l, prefix='Calculate detection each asteroid:')

# calculate how many current asteroid detects others asteroid
for asteroidVectors in vectors:
    countDetections[i] = 0
    for vector1 in asteroidVectors:
        isNotCover = True
        
        tempVectors = asteroidVectors[:]
        tempVectors.remove(vector1)

        for vector2 in tempVectors:
            # its in grid so the is some of a deviation (that's why we dont compare angle to 1)
            if getAngle(vector1, vector2) >= 0.999999999999999:
                # when when two asteroid are on the same line
                # shorter vector cover the asteroid behind it
                if length(vector1) > length(vector2):
                    isNotCover = False
                    break

        if isNotCover:
            countDetections[i] += 1

    i += 1
    printProgressBar(i, l, prefix='Calculate detection each asteroid:')

print()
print("Maximum number of detecions: " + max(countDetections))