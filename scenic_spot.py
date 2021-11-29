class ScenicSpot:
    id = ''
    name = ''
    url = ''
    level = ''
    mainImage = ''
    mainImageAlt = ''
    shortDesc = ''
    address = {}

    def __init__(self, id, name, url, level, mainImage, mainImageAlt, shortDesc):
        self.id = id
        self.name = name
        self.url = url
        self.level = level
        self.mainImage = mainImage
        self.mainImageAlt = mainImageAlt
        self.shortDesc = shortDesc


class Address:
    address = ''
    country = ''
    province = ''
    cityCode = ''
    city = ''
    district = ''
    adcode = ''
    location = ''

    def __init__(self, address, country, province, cityCode, city, district, adcode, location):
        self.address = address
        self.country = country
        self.province = province
        self.cityCode = cityCode
        self.city = city
        self.district = district
        self.adcode = adcode
        self.location = location


class OneCityTop10ScenicSpot:
    id = ''
    cityName = ''
    keywords = ''
    scenicSpots = []

    def __init__(self, id, cityName, keywords, scenicSpots):
        self.id = id
        self.cityName = cityName
        self.keywords = keywords
        self.scenicSpots = scenicSpots


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
