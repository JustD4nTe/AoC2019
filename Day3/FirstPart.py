from shapely.geometry import LineString
import matplotlib.pyplot as plt

# parse wire's moves
def getPath(moves):
    # set start position
    path = [(0,0)]

    #           X  Y
    position = [0, 0]

    for move in moves:
        direction = move[0]
        stepCount = int(move[1:])

        if direction == "U":
            position[1] += stepCount
        elif direction == "R":
            position[0] += stepCount
        elif direction == "D":
            position[1] -= stepCount
        elif direction == "L":
            position[0] -= stepCount

        path.append(tuple(position[:]))

    return path

# get pairs of points for line segments
def getLineSegments(points):
    coords = getPath(points)
    return list(zip(coords, coords[1:]))

def intersection(ab, cd):
    line1 = LineString(ab)
    line2 = LineString(cd)
    x = line1.intersection(line2)

    if x.is_empty:
        return (0, 0)

    # because there're line segments not lines
    # we must check if point is on segments
    if (min(ab[0][0],ab[1][0],cd[0][0],cd[1][0]) <= x.x <= max(ab[0][0],ab[1][0],cd[0][0],cd[1][0]) 
        and min(ab[0][1],ab[1][1],cd[0][1],cd[1][1]) <= x.y <= max(ab[0][1],ab[1][1],cd[0][1],cd[1][1])):
        return (x.x, x.y)
    
    return (0, 0)

def drawWires(first, second):
    for i in first:
        plt.plot((i[0][0],i[1][0]), (i[0][1],i[1][1]), 'ro--')

    for i in second:
        plt.plot((i[0][0],i[1][0]), (i[0][1],i[1][1]), 'co:')
    
    plt.show()


with open("data.txt", 'r') as data:
    firstPath = getLineSegments(data.readline().split(","))
    secondPath = getLineSegments(data.readline().split(","))

distanceOfIntersection = []

for f in firstPath:
    for s in secondPath:
        tempPoint = intersection(f, s)
        if tempPoint != (0, 0):
            # distplay coords of intersection point
            print(str(tempPoint), end=' ')
            
            # we are looking for the shortest taxicab distance => so it can't be negative
            distanceOfIntersection.append((abs(tempPoint[0]) + abs(tempPoint[1])))

print()


print(min(distanceOfIntersection))

# comment if u dont want see a plot
drawWires(firstPath, secondPath)