import requests
import os
from utils import readDirectory, writeFile
from scenic_spot import OneCityTop10ScenicSpot, ScenicSpot, Address

import json


def geocode(address):
    parameters = {'address': address,
                  's': 'rsv3',
                  'city': '35',
                  'key': 'e23c1cac6c6f5bbb73d063d7115c36d9'}
    base = 'https://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    if answer['count'] == '0':
        return "error", "", "", ""
    address = answer['geocodes'][0]['formatted_address']
    country = answer['geocodes'][0]['country']
    province = answer['geocodes'][0]['province']
    cityCode = answer['geocodes'][0]['citycode']
    city = answer['geocodes'][0]['city']
    district = answer['geocodes'][0]['district']
    adcode = answer['geocodes'][0]['adcode']
    location = answer['geocodes'][0]['location']
    if location != '':
        return Address(address, country, province, cityCode, city, district, adcode, location)
    else:
        return {}


def resolveJson(path):
    file = open(path, "rb")
    fileJson = json.load(file)
    cityName = fileJson["cityName"]
    id = fileJson["id"]
    keywords = fileJson["keywords"]
    scenicSpotID = fileJson["scenicSpotID"]
    scenicSpotsJson = fileJson["scenicSpots"]
    scenicSpots = []
    for ss in scenicSpotsJson:
        scenicSpot = ScenicSpot(ss["id"], ss["name"], ss["url"], ss["level"], ss["mainImage"],
                                ss["mainImageAlt"], ss["shortDesc"])
        try:
            address = geocode(cityName.replace(
                "十大旅游景点", "").replace("前十旅游景点", "")+" "+ss["name"])
            if address.location != '':
                scenicSpot.address = address
            else:
                scenicSpot.address = Address("", "", "", "", "", "", "", "")
        except Exception as ex:
            scenicSpot.address = Address("", "", "", "", "", "", "", "")
            pass
        scenicSpots.append(scenicSpot)

    oneCityTop10ScenicSpot = OneCityTop10ScenicSpot(
        id, cityName, keywords, scenicSpots)
    return oneCityTop10ScenicSpot


def output(path):
    oneCityTop10ScenicSpot = resolveJson(path)
    jsonStr = json.dumps(
        oneCityTop10ScenicSpot, ensure_ascii=False, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    writeFile('F:/GitWorkspace/spider/data/withaddress',
              oneCityTop10ScenicSpot.id+'.json', jsonStr)


# output('F:/GitWorkspace/spider/data/ABTSADMDSDLYJD.json')
# output('F:/GitWorkspace/spider/data/ZJKSSYSDLYJD.json')


# print(geocode('天安门')) #('北京市东城区天安门', '北京市东城区', '110101', '116.397499,39.908722')
# print(geocode('大雁塔')) #('陕西省西安市雁塔区大雁塔', '西安市雁塔区', '610113', '108.964162,34.218285')
# print(geocode('西安城墙·碑林历史文化景区')) #('陕西省西安市碑林区西安城墙', '西安市碑林区', '610103', '108.948302,34.251854')
# print(geocode('小雁塔(荐福寺)')) #('陕西省西安市碑林区小雁塔', '西安市碑林区', '610103', '108.941610,34.239055')
# print(geocode('齐齐哈尔市昂昂溪 昂昂溪遗址')) #('黑龙江省齐齐哈尔市昂昂溪区昂昂溪遗址', '齐齐哈尔市昂昂溪区', '230205', '123.838949,47.145884')
# ('陕西省西安市碑林区钟楼', '西安市碑林区', '610103', '108.948063,34.259067')
# print(geocode('陕西西安 雅逸新城'))
# print(geocode('艾伯塔省埃德蒙顿 旧斯达孔拿历史区'))
# print(geocode('天安门'))
# print(geocode('天安门'))


def main():
    dir = 'F:/GitWorkspace/spider/data'
    files = readDirectory(dir)
    index = 0
    for file in files:
        if file == 'scenic_spots' or file == '1_TOP_10_LIST.json' or file == 'withaddress':
            # print(file)
            continue
        if os.path.exists(dir+"/withaddress/"+file):
            continue
        # if index > 0:
        #     break
        index += 1
        output(dir+"/"+file)
        print(dir+"/"+file, ' is done.')


main()
