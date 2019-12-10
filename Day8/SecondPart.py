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


def showImage(image):
    for i in image:
        for j in i:
            print(str(j), end='')
        print()


def getImage(rawImage):
    canvas = []

    # canvas for image
    for i in range(len(rawImage[0])):
        canvas.append(['2'] * len(rawImage[0][0]))

    # on every layer
    for i in rawImage:
        jj = 0
        # on every line of bytes
        for j in i:
            kk = 0
            # on every byte
            for k in j:
                # when byte on canvas is transparent
                # transparent: 2, white: 1, black: 0
                if canvas[jj][kk] == '2':
                    # for better visibility, hide byte 0
                    if k == '0':
                        canvas[jj][kk] = ' '
                    else:
                        canvas[jj][kk] = k

                kk += 1
            jj += 1

    return canvas


data = [i for i in open("data.txt", 'r').read()]

# get image's layers
imageWithLayers = imageLayers(25, 6, data)

# show image without layers
showImage(getImage(imageWithLayers))