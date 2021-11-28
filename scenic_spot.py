class ScenicSpot:
    id = ''
    name = ''
    url = ''
    level = ''
    mainImage = ''
    mainImageAlt = ''
    shortDesc = ''

    def __init__(self, id, name, url, level, mainImage, mainImageAlt, shortDesc):
        self.id = id
        self.name = name
        self.url = url
        self.level = level
        self.mainImage = mainImage
        self.mainImageAlt = mainImageAlt
        self.shortDesc = shortDesc


class OneCityTop10ScenicSpot:
    id = ''
    scenicSpotID = ''
    cityName = ''
    keywords = ''
    scenicSpots = []

    def __init__(self, id, cityName, keywords, scenicSpots, scenicSpotID):
        self.id = id
        self.cityName = cityName
        self.keywords = keywords
        self.scenicSpots = scenicSpots
        self.scenicSpotID = scenicSpotID


class Image:
    url = ''
    alt = ''

    def __init__(self, url, alt):
        self.url = url
        self.alt = alt


class OneScenicSpotContent:
    id = ''
    keywords = ''
    description = ''
    images = []
    contentText = ''
    scenicSpotID = ''
    oneCityTop10ScenicSpotID = ''

    def __init__(self, id, images, keywords, description, contentText, scenicSpotID, oneCityTop10ScenicSpotID):
        self.id = id
        self.keywords = keywords
        self.description = description
        self.images = images
        self.contentText = contentText
        self.scenicSpotID = scenicSpotID
        self.oneCityTop10ScenicSpotID = oneCityTop10ScenicSpotID


class Top10ScenicSpotLink:
    index = 0
    title = ''
    url = ''
    location = ''
    nav = ''

    def __init__(self, data):
        self.__dict__ = data

    def __init__(self, index, title, url, location, nav):
        self.index = index
        self.title = title
        self.url = url
        self.location = location
        self.nav = nav
