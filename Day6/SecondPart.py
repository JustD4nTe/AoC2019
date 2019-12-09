# save planet' relations in dictionary
def getPlanetRelation(data, planet):
    res = {}

    for bar in data:
        if bar[0] == planet:
            res.update({bar[1]: getPlanetRelation(data, bar[1])})

    return res


# https://stackoverflow.com/a/14962509
# trying to find a planet
def findPlanet(mapOfRelations, planetName):
    if planetName in mapOfRelations:
        return mapOfRelations[planetName]

    for k, v in mapOfRelations.items():
        item = findPlanet(v, planetName)
        if item is not None:
            return item

def numberOfOrbitsOfOnePlanet(planets, key):
    if key in planets:
        return 0

    for k, v in planets.items():
        numberOfOrbits = numberOfOrbitsOfOnePlanet(v, key)
        if numberOfOrbits is not None:
            return numberOfOrbits + 1

# trying to find the planet,
# which is shared with Santa
# and it's the farthest from COM than others
def getSharedPlanetWithSanta(data):
    key = None
    value = None
    
    # looking for every "subplanet" (planet which have smaller mass)
    for k, v in data.items():
        if findPlanet(v, "SAN") is not None and findPlanet(v, "YOU") is not None:
            value = v
            key = k
            break

    # currently being checked planet is correct
    if value is not None:
        # but what if next planets are correct to?
        result = getSharedPlanetWithSanta(value)

        # when there not, current one is the final one
        if result == -1:
            return key

        # when there yes, just return them
        return result

    # return "error code"
    # because there is not a planet which "contains" ours and Santa's planet
    else:
        return -1

# get all data
data = [i.split(')') for i in open("Day6/data.txt", 'r').read().splitlines()]

# set map of relations
relations = {"COM": getPlanetRelation(data, "COM")}

#  get nearest shared planet
sharedPlanet = getSharedPlanetWithSanta(relations)

# set map of relations, where COM is nearest sherd planet
newRelations = {sharedPlanet: getPlanetRelation(data, sharedPlanet)}

# prints distance between ours and Santa's planet
# then substract 2, because we don't need a direct orbit (only indirect needed)
print(abs(numberOfOrbitsOfOnePlanet(newRelations, "SAN")
            + numberOfOrbitsOfOnePlanet(newRelations, "YOU")) - 2)
