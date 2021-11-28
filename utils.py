#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import urllib.request
from uuid import uuid4
import re
import os
from pypinyin import pinyin, lazy_pinyin
import json
import hashlib

uuidChars = ("a", "b", "c", "d", "e", "f",
             "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
             "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
             "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
             "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
             "W", "X", "Y", "Z")


def short_uuid():
    uuid = str(uuid4()).replace('-', '')
    result = ''
    for i in range(0, 8):
        sub = uuid[i * 4: i * 4 + 4]
        x = int(sub, 16)
        result += uuidChars[x % 0x3E]
    return result


def downImg(img, folderPath, fileName):
    # print(img, folderPath, fileName)
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
    res = requests.get(img, headers={'User-Agent': ua})
    with requests.get(img, headers={'User-Agent': ua}) as resp:
        # print(resp.status_code)
        resp.raise_for_status()
        resp.encoding = res.apparent_encoding
        # 将图片内容写入
        with open(folderPath+"/"+fileName, 'wb') as f:
            f.write(resp.content)
            f.close()


def replaceSpecialChar(str):
    return str.replace("\t", "").replace("》", "").replace("【", "").replace("】", "").replace("，", "").replace("－", '').replace("、", '').replace("—", '').replace("•", "").replace("“", "").replace("”", "").replace("（", '').replace('）', '').replace("(", '').replace(")", '').replace('Ā', 'A').replace('Á', 'A').replace('Ǎ', 'A').replace("À", "A").replace('Ě', 'E').replace('È', 'E').replace('Ē', 'E').replace("É", 'E').replace("Ō", 'O').replace('·', '').replace("《", "").replace("-", "")


def getAcronym(strData):
    return replaceSpecialChar("".join([i[0][0] for i in pinyin(strData)]).upper())


def readDirectory(dirName):
    fileNames = []
    for fileName in os.listdir(dirName):
        fileNames.append(fileName)
    return fileNames


def writeFile(folderPath, fileName, contentText):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    fo = open(folderPath + "/"+fileName, 'w', encoding="UTF-8")
    fo.write(contentText)
    fo.close()


def readFile(folderPath, fileName):
    if not os.path.exists(folderPath+"/"+fileName):
        return ''
    else:
        with open(folderPath+"/"+fileName, 'r', encoding="UTF-8") as load_f:
            load_dict = json.load(load_f)
            load_f.close()
            return load_dict
    return ''


def existingContentByReqURL(url, checkFun, grabContentFun):
    response = urllib.request.urlopen(url)
    html = response.read().decode("GBK")
    if checkFun(html):
        return False
    grabContentFun(url, html)
    return True


def isActiveReqURL(url):
    try:
        response = urllib.request.urlopen(url)
        html = response.read()
    except Exception:
        return False
    return True


def existingContentByReqURLforTop10(url, grabContentFun):
    return existingContentByReqURL(url,
                                   lambda html: '对不起，你要查看的页面不存在' in html, grabContentFun)


def isPhoneOrTelephoneNumber(number):
    if re.match(r'^(\(\d{3,4}\)|\d{3,4}-|\s)?\d{7,14}$', number):
        return True
    return False


def isWebUrl(url):
    if re.match(r"^((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?$", url):
        return True
    return False


fileNames = readDirectory('F:/GitWorkspace/spider/data/scenic_spots')
# fileNames = readDirectory('F:/GitWorkspace/spider/assets/images/scenic-spot')


def clearBadFiles(dir):
    fileNames = readDirectory(dir)
    i = 0
    for fileName in fileNames:
        fixedFileName = replaceSpecialChar(fileName)
        if fixedFileName != fileName:
            i = i+1
            # if i > 1:
            #     break
            print(i, fileName)
            os.remove(dir+'/'+fileName)
            # fixedStr = str(readFile('F:/GitWorkspace/spider/data/scenic_spots',
            #                         fileName)).replace(fileName.replace(".json", ""), fixedFileName.replace(".json", ""))
            # print(fixedStr)
            # writeFile('F:/GitWorkspace/spider/data/scenic_spots',
            #           fileName, fixedStr)


# clearBadFiles('F:/GitWorkspace/spider/data/scenic_spots')

def getFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def keepTheLatestOneFile(dirPath):
    md5s = []
    files = []
    dirs = readDirectory(dirPath)
    if len(dirs) <= 1:
        return
    for dir in dirs:
        md5 = getFileMd5(dirPath + "/"+dir)
        create_time = os.path.getctime(dirPath + "/"+dir)
        update_time = os.path.getmtime(dirPath + "/"+dir)
        files.append(
            {"dir": dir, "md5": md5, "ct": create_time, "mt": update_time})
        existingmd5s = list(filter(lambda m: m ==
                                   md5, md5s))
        if len(existingmd5s) <= 0:
            md5s.append(md5)

    for mmdd55 in md5s:
        sameFileswithmd5s = list(filter(lambda f: f["md5"] ==
                                        mmdd55, files))
        sameFileswithmd5sSorted = sorted(
            sameFileswithmd5s, key=lambda ff: ff['ct'], reverse=True)
        index = 0
        for ffile in sameFileswithmd5sSorted:
            if index > 0:
                os.remove(dirPath+'/'+ffile['dir'])
                print(ffile['dir'], ffile['md5'], ffile['ct'],
                      ffile['mt'], ' be removed as duplicated.')
            index += 1


imgDirs = readDirectory('F:/GitWorkspace/spider/images/scenic_spots')
for imgDir in imgDirs:
    keepTheLatestOneFile(
        'F:/GitWorkspace/spider/images/scenic_spots', imgDir)


def renameBadFiles(dir):
    fileNames = readDirectory(dir)
    i = 0
    for fileName in fileNames:
        fixedFileName = replaceSpecialChar(fileName)
        if fixedFileName != fileName:
            i = i+1
            # if i > 1:
            #     break
            print(i, fileName)
            os.renames(dir+'/'+fileName, dir+'/'+fixedFileName)

            # fixedStr = str(readFile('F:/GitWorkspace/spider/data/scenic_spots',
            #                         fileName)).replace(fileName.replace(".json", ""), fixedFileName.replace(".json", ""))
            # print(fixedStr)
            # writeFile('F:/GitWorkspace/spider/data/scenic_spots',
            #           fileName, fixedStr)
# renameBadFiles('F:/GitWorkspace/spider/assets/images/scenic-spot')
# print(readFile('F:/GitWorkspace/spider/data', '1_TOP_10_LIST.json'))
# print(isActiveReqURL('http://www.baidu.com/1'))
# print(isWebUrl('http22://www.baidu.com'))
# print(getAcronym('西安市十大旅游景点').replace('Ā', 'A'))
# writeFile('F:/GitWorkspace/spider/data', 'test.json', '''[
#     {
#         "id": "QSHBMY",
#         "level": "AAAAA",
#         "mainImage": "assets/images/scenic-spot/SXSXASSDLYJD/QSHBMY/z5Y1Ervm.gif",
#         "mainImageAlt": "秦始皇兵马俑",
#         "name": "秦始皇兵马俑",
#         "shortDesc": "世界第八大奇迹。1974年，秦始皇陵兵马俑坑的发现震惊世界。这一建在公元前3世纪的地下雕塑群以恢弘磅礴的气势，威武严整
# 的军阵，形态逼真的陶俑向人们展示出古代东方文化的灿烂辉煌，无论建造年代、建筑规模与艺术效果无不堪与“世界七大奇迹”媲美。于是，“世界第八大
# 奇迹”之誉不胫而走，成为秦始皇陵兵马俑的代名词。秦始皇兵马俑博物馆是我国最大的遗址博物馆，除一号坑、二号坑、三号坑保护陈列大厅外，还有兵
# 马俑坑出土文物陈列室和秦陵铜车马陈列室。20世纪最重要的发现西杨村本是郦山北麓一个默默无闻的普通村庄。１９７４年３月，西杨村的村民在村南
# １６０米的柿树林畔打一口井。这里地处骊山冲积扇前缘，累经山洪泥石流淤积，耕地间夹杂布满鹅卵石的灌木丛和废弃荒地。３月２４日动工，挖到３
# 米多深时，发现下面是红烧土、烧结硬块和炭屑灰烬，大家以为碰上了老砖窑址。继续往下打，在５米多深处的井壁西侧，阴暗的光线下终于露出“瓦王爷
# ”凝静的面容。村民们正诧异间，恰好公社干部房树民来检查打井进度。他下到井底仔细观察，发现出上的砖块与秦始皇陵附近发现的秦砖一模一样，急忙
# 告诉大家暂停打井，接着便匆匆赶往县城报告县文化馆。湮没２２００年的……",
#         "url": "http://www.bytravel.cn/landscape/3/qinshihuangbingma.html"
#     },
#     {
#         "id": "DYTDTFRYJQ",
#         "level": "AAAAA",
#         "mainImage": "assets/images/scenic-spot/SXSXASSDLYJD/DYTDTFRYJQ/NjzzGhlY.gif",
#         "mainImageAlt": "大雁塔·大唐芙蓉园景区",
#         "name": "大雁塔·大唐芙蓉园景区",
#         "shortDesc": "大雁塔文化休闲景区,坐落西安标志性建筑大雁塔的脚下,是国家AAAAA级景区,也是中国首批国家级文化产业示范区——曲江新区的
# 北大门。自2003年12月31日大雁塔北广场盛妆开放以来,景区平均每日接待各地游客数以万计,成为游客的乐土、市民的家园、城市的窗口、文化的盛地,被
# 誉为西安的“城市会客厅”,为西安、陕西的文化建设和旅游业发展带来了极大的品牌效应。大雁塔位于唐长安城晋昌坊（今陕西省西安市南）的大慈恩寺内
# ，又名“慈恩寺塔”。唐永徽三年（652年），玄奘为保存由天竺经丝绸之路带回长安的经卷佛像主持修建了大雁塔，最初五层，后加盖至九层，再后层数和
# 高度又有数次变更，最后固定为所看到的七层塔身，通高64.517米，底层边长25.5米。大雁塔作为现存最早、规模最大的唐代四方楼阁式砖塔，是佛塔这
# 种古印度佛寺的建筑形式随佛教传入中原地区，并融入华夏文化的典型物证，是凝聚了中国古代劳动人民智慧结晶的标志性建筑。1961年3月4日，国务院
# 公布大雁塔为第一批全国重点文物保护单位。2014年6月22日，在卡塔尔多哈召开的联合国教科文组织第38届世界遗产委员会会议上，大雁塔作为中国、哈
# 萨克斯坦和吉尔吉斯斯坦三国……",
#         "url": "http://www.bytravel.cn/landscape/2/jianmenshudao.html"
#     }]''')
# downImg('http://h.bytravel.cn/www/33/head/33335.gif',
#         './assets/images/scenic-spot/aiFvEQjt/69bkpQrJ', 'exRzRIWW.gif')

# downImg('http://h.bytravel.cn/www/33/head/33335.gif',
#         './assets/images/scenic-spot/9rVMxGM8/nq8Nh1MS', 'xBbnhNxf.gif')
# downImg('http://www.bytravel.cn/images/4A.png',
#         './assets/images/scenic-spot/9rVMxGM8/93AQcBzA', 'PzKLlpo9.png')
# downImg('http://h.bytravel.cn/www/61/head/61285.gif',
#         './assets/images/scenic-spot/9rVMxGM8/BqfHQcae', 'FNrm2qPI.gif')
# downImg('http://www.bytravel.cn/images/sl.png',
#         './assets/images/scenic-spot/9rVMxGM8/Z2lgm6fF', 'MOxGleSD.png')
# downImg('http://h.bytravel.cn/www/55/head/55405.gif',
#         './assets/images/scenic-spot/9rVMxGM8/hCA2Nl7m', 'IByVt3wP.gif')
# downImg('http://h.bytravel.cn/www/61/head/61284.gif',
#         './assets/images/scenic-spot/9rVMxGM8/jM5nHe3p', 'QLzS7FyC.gif')
# downImg('http://h.bytravel.cn/www/37/head/36836.gif',
#         './assets/images/scenic-spot/9rVMxGM8/mi57PRiE', 'QVnGEMsL.gif')
# downImg('http://h.bytravel.cn/www/91/head/90817.gif',
#         './assets/images/scenic-spot/9rVMxGM8/NSCK3e1U', 'TuyAvk3v.gif')
# downImg('http://www.bytravel.cn/images/wen.png',
#         './assets/images/scenic-spot/9rVMxGM8/wKXF3GNw', 'fL630YsD.png')
# downImg('http://h.bytravel.cn/www/37/head/36830.gif',
#         './assets/images/scenic-spot/9rVMxGM8/ExB04M5l', '9DQjXtXp.gif')
# downImg('http://h.bytravel.cn/www/37/head/36822.gif',
#         './assets/images/scenic-spot/9rVMxGM8/kSoFM6iZ', 'zrsQHpXU.gif')
# downImg('http://h.bytravel.cn/www/37/head/36764.gif',
#         './assets/images/scenic-spot/9rVMxGM8/IJMUFY7s', 'A56t8yiF.gif')
# downImg('http://h.bytravel.cn/www/31/head/30679.gif',
#         './assets/images/scenic-spot/9rVMxGM8/GWNeakMp', 'SoPQfVeW.gif')
# downImg('http://img.bytravel.cn/827/8278/w460632432.jpg',
#         './assets/images/scenic-spot/2/3', '1.jpg')


def findLast(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position+1)
        if position == -1:
            return last_position
        last_position = position
    return last_position


x = 'http://img.bytravel.cn/827/8278/w460632432.jpg'

# print(x[findLast(x, '.'):])
# mainImage = 'http://img.bytravel.cn/827/8278/w460632432.jpg'
# targetUrl = '/a/b/c'
# targetImgName = '1.jpg'
# x = []
# x.append({'oriUrl': mainImage, 'targetUrl': targetUrl,
#          'targetImgName': targetImgName})
# mainImage = 'http://img.bytravel.cn/827/8278/w460632433.jpg'
# targetUrl = '/a/b/e'
# targetImgName = '2.jpg'
# x.append({'oriUrl': mainImage, 'targetUrl': targetUrl,
#          'targetImgName': targetImgName})


# print(list(filter(lambda img: img['oriUrl'] ==
#       'http://img.bytravel.cn/827/8278/w460632433.jpg', x))[0])

# print(short_uuid())
# print(short_uuid())
# print(short_uuid())
