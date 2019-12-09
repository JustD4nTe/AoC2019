# create layers of image
def imageLayers(width, height, data):
    image = []
    layer = []
    row = []
    offset = 0

    # calculate number of all layers
    numberOfLayers = int(len(data) / (width * height))

    for k in range(numberOfLayers):
        layer = []

        for i in range(height):
            row = []

            for j in range(width):
                row.append(data[j + i + offset])

            offset += width - 1
            layer.append(row)

        offset += height

        image.append(layer)

    return image


# display all layers in console
def showImageLayers(image):
    numberOfLayer = 1

    for i in image:
        print("Layer " + str(numberOfLayer) + ": ")
        for j in i:
            print("\t\t" + str(j))

        print()
        numberOfLayer += 1


def findLayerWithFewestAmountOfZero(image):
    numberOfLayer = 1

    minNumberOfZeros = 25 * 6
    numberOfLayerWithMinZeros = 1

    for i in image:
        numberOfZeros = 0

        for j in i:
            for k in j:
                if int(k) == 0:
                    numberOfZeros += 1

        if minNumberOfZeros > numberOfZeros:
            minNumberOfZeros = numberOfZeros
            numberOfLayerWithMinZeros = numberOfLayer

        numberOfLayer += 1

    return numberOfLayerWithMinZeros


# count how many times 1 and 2 digits are apper in layer
def CountOneAndTwo(image, layer):
    numberOfLayer = 1
    one = 0
    two = 0

    for i in image:
        if numberOfLayer == layer:
            for j in i:
                for k in j:
                    if int(k) == 1:
                        one += 1
                    if int(k) == 2:
                        two += 1

        numberOfLayer += 1

    return one, two


data = [i for i in open("data.txt", 'r').read()]

image = (imageLayers(25, 6, data))

# showImageLayers(image)

zero = findLayerWithFewestAmountOfZero(image)

a, b = CountOneAndTwo(image, zero)
print(str(a * b))