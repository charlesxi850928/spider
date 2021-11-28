import requests


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
    dz = answer['geocodes'][0]['formatted_address']
    qu = answer['geocodes'][0]['city'] + answer['geocodes'][0]['district']
    adcode = answer['geocodes'][0]['adcode']
    location = answer['geocodes'][0]['location']
    return dz, qu, adcode, location


# print(geocode('天安门')) #('北京市东城区天安门', '北京市东城区', '110101', '116.397499,39.908722')
# print(geocode('大雁塔')) #('陕西省西安市雁塔区大雁塔', '西安市雁塔区', '610113', '108.964162,34.218285')
# print(geocode('西安城墙·碑林历史文化景区')) #('陕西省西安市碑林区西安城墙', '西安市碑林区', '610103', '108.948302,34.251854')
# print(geocode('小雁塔(荐福寺)')) #('陕西省西安市碑林区小雁塔', '西安市碑林区', '610103', '108.941610,34.239055')
print(geocode('齐齐哈尔市昂昂溪 昂昂溪遗址'))
# print(geocode('天安门'))
# print(geocode('天安门'))
# print(geocode('天安门'))
