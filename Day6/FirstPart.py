# save planet' relations in dictionary
def getPlanetRelation(data, planet):
    res = {}

    for bar in data:
        if bar[0] == planet:
            res.update({bar[1]: getPlanetRelation(data, bar[1])})

    return res


# next two func are based on:
# https://stackoverflow.com/a/14962509

# get total number of direct and indirect orbits
def totalNumberOfOrbits(planets):
    totalNumber = 0

    for k, v in planets.items():
        # every planet has a dictionary with smaller planets
        # but when it doesn't, dict is empty
        # so we can calculate all relations for this planet
        if v != {}:
            totalNumber += totalNumberOfOrbits(v)

        totalNumber += numberOfOrbitsOfOnePlanet(relations, k)

    return totalNumber


def numberOfOrbitsOfOnePlanet(foo, key):
    if key in foo:
        return 0

    for k, v in foo.items():
        numberOfOrbits = numberOfOrbitsOfOnePlanet(v, key)
        if numberOfOrbits is not None:
            return numberOfOrbits + 1


data = [i.split(')') for i in open("data.txt", 'r').read().splitlines()]

relations = {"COM": getPlanetRelation(data, "COM")}

print(totalNumberOfOrbits(relations))