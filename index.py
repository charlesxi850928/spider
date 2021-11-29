#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib.request
import re
import os
from bs4 import BeautifulSoup
from scenic_spot import ScenicSpot, OneCityTop10ScenicSpot, Image, OneScenicSpotContent, Top10ScenicSpotLink
from utils import readFile, short_uuid, downImg, findLast, getAcronym, writeFile, isPhoneOrTelephoneNumber, isWebUrl, isActiveReqURL
from grab_top_10_list import top10List
import json


def strippedShotDesc(intrest):
    ret = ''
    descs = intrest.select('div#tctitletop102 div[style="margin:0 0 10px 0"]')[
        0].stripped_strings
    for desc in descs:
        d = repr(desc)
        if d == "'[详细]'":
            continue
        else:
            ret = d
    return ret.replace("'", "")


# os.mkdir("d://message")
os.chdir("d://message")

imgMap = []


def fetchImage(mainImage, extTargeUrl):
    targetUrl = ''
    targetImgName = ''
    existingImgs = list(filter(lambda img: img['oriUrl'] ==
                               mainImage, imgMap))
    if len(existingImgs) > 0:
        targetImg = existingImgs[0]
        targetUrl = targetImg['targetUrl']
        targetImgName = targetImg['targetImgName']
    else:
        targetUrl = 'F:/GitWorkspace/spider/assets/images/scenic-spot/'+extTargeUrl
        targetImgName = short_uuid()+mainImage[findLast(mainImage, '.'):]
        downImg(mainImage,
                targetUrl, targetImgName)
        targetUrl = targetUrl.replace(
            'F:/GitWorkspace/spider/assets/', 'assets/')
        imgMap.append(
            {'oriUrl': mainImage, 'targetUrl': targetUrl, 'targetImgName': targetImgName})
    return {'targetUrl': targetUrl, 'targetImgName': targetImgName}


scenicSpotsMap = []


def strippedOneScenicSpotContent(url, mainId, id):
    existingScenicSpots = list(filter(lambda ss: ss['url'] ==
                               url, scenicSpotsMap))
    if len(existingScenicSpots) > 0:
        print(mainId, id, ' is done.')
        return
    scenicSpotsMap.append({'url': url})
    response = urllib.request.urlopen(url)
    html = ''
    try:
        html = response.read().decode("GBK")
    except Exception as ex:
        html = response.read().decode("UTF-8")

    soup = BeautifulSoup(html, 'html.parser')
    imgs = soup.find_all(
        "img", style='border:1px #cccccc solid;')
    images = []
    for img in imgs:
        mainImage = img['src']
        targetUrl = ''
        targetImgName = ''
        try:
            imgInfo = fetchImage(mainImage, id)
            targetUrl = imgInfo['targetUrl']
            targetImgName = imgInfo['targetImgName']
        except Exception:
            pass
        image = Image(targetUrl+"/"+targetImgName, img['alt'])
        images.append(image)

    divs = soup.find_all(
        "div", style='margin:0 10px 0 10px;clear:both')[0]
    contentText = ''
    for divOrP in divs.contents:
        if divOrP.name == 'div':
            ass = divOrP.select('a')
            l = len(ass)
            if l > 0:
                span = '<div class="imgWrapper" ><span>'
                for a in ass:
                    imgAlt = ''
                    imgSrc = ''
                    try:
                        imgAlt = a.select('img')[0]['alt']
                    except Exception as ex:
                        # print(ex)
                        pass
                    try:
                        imgSrc = a.select('img')[0]['src']
                        if imgSrc.startswith("http") == False:
                            imgSrc = "http://www.bytravel.cn" + imgSrc
                            imgInfo = fetchImage(imgSrc, id)
                            targetUrl = imgInfo['targetUrl']
                            targetImgName = imgInfo['targetImgName']
                            imgSrc = targetUrl+"/"+targetImgName
                    except Exception as ex:
                        # print(ex)
                        pass
                    if imgAlt != '' or imgSrc != '':
                        divImg = '<img '
                        if imgAlt != '':
                            divImg += 'alt="'+imgAlt+'" '
                        if imgSrc != '':
                            divImg += 'src="'+imgSrc+'" '
                        span += divImg+" />"
                span += "</span></div>"
                contentText += span
                continue
            else:
                contentText += str(divOrP)
                continue
        try:
            tagP = str(divOrP)
            if '延伸阅读' in tagP or '<a ' in tagP:
                continue
            tagC = tagP.replace('<p>', "").replace('</p>', '')
            if isPhoneOrTelephoneNumber(tagC):
                tagP = '<p class="phoneNumber">' + \
                    tagC+'</p>'
            # if isWebUrl(tagC) and isActiveReqURL(tagC):
            if isWebUrl(tagC):
                tagP = '<p class="weburl"><a target="_blank" href="'+tagC+'">' + \
                    tagC+'</a></p>'
            pdivOrP = tagP
        except Exception as ex:
            # print(ex)
            pass
        contentText += pdivOrP.replace("\n", "")
    title = soup.head.title.string
    keywords = soup.select(
        'head meta[name="keywords"]')[0]['content']
    description = soup.select(
        'head meta[name="description"]')[0]['content']
    oneScenicSpotContent = OneScenicSpotContent(
        id, images, keywords, description,  contentText, mainId, id)
    jsonStr = json.dumps(
        oneScenicSpotContent, ensure_ascii=False, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    writeFile('F:/GitWorkspace/spider/data/scenic_spots',
              oneScenicSpotContent.id+'.json', jsonStr)
    print(mainId, id, ' is done.')

# strippedOneScenicSpotContext()


def strippedOneCityTop10ScenicSopts(url):
    scenicSpots = []
    response = urllib.request.urlopen(url)
    html = response.read().decode("GBK")
    soup = BeautifulSoup(html, 'html.parser')
    intrests = soup.find_all(
        "div", style='margin:2px 10px 0 7px;padding:3px 0 0 0')
    title = soup.head.title.string
    mainId = getAcronym(title)

    reGenerate = False
    eIntrests = []
    try:
        existingIntrests = readFile(
            "F:/GitWorkspace/spider/data", mainId+".json")
        for existingIntrest in existingIntrests['scenicSpots']:
            name = existingIntrest['name']
            eIntrests.append(name)
    except Exception as ex:
        # print(ex)
        pass
    reGenerate = len(eIntrests) != 10
    for intrest in intrests:
        name = intrest.select('div#tctitletop10 .blue14b')[0].string
        id = getAcronym(name)
        if os.path.exists("F:/GitWorkspace/spider/data/scenic_spots/"+id+".json") and reGenerate == False:
            continue
        reGenerate = True
        url = ''
        try:
            url = "http://www.bytravel.cn" + \
                intrest.select('div#tctitletop10 .blue14b')[0]['href']
        except Exception:
            pass
        level = ''
        try:
            level = intrest.select(
                'div#tctitletop10 span font.f14[color="red"]')[0].string
        except Exception:
            pass
        mainImage = ''
        try:
            mainImage = intrest.select('div#tctitletop102 img.hpic')[0]['src']
        except Exception:
            pass
        targetUrl = ''
        targetImgName = ''
        try:
            imgInfo = fetchImage(mainImage, id)

            targetUrl = imgInfo['targetUrl']
            targetImgName = imgInfo['targetImgName']
        except Exception:
            pass
        mainImageAlt = ''
        try:
            mainImageAlt = intrest.select(
                'div#tctitletop102 img.hpic')[0]['alt']
        except Exception:
            pass
        shortDesc = strippedShotDesc(intrest)
        scenicSpot = ScenicSpot(id, name, url, level, targetUrl+"/"+targetImgName,
                                mainImageAlt, shortDesc)
        try:
            strippedOneScenicSpotContent(url, mainId, id)
        except Exception as ex:
            # print(ex)
            pass
        scenicSpots.append(scenicSpot)
    keywords = ''
    try:
        keywords = soup.select(
            'head meta[name="keywords"]')[0]['content']
    except Exception as ex:
        # print(ex)
        pass
    if reGenerate:
        oneCityTop10ScenicSpot = OneCityTop10ScenicSpot(
            mainId, title, keywords, scenicSpots)
        jsonStr = json.dumps(
            oneCityTop10ScenicSpot, ensure_ascii=False, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        writeFile('F:/GitWorkspace/spider/data',
                  oneCityTop10ScenicSpot.id+'.json', jsonStr)
    return oneCityTop10ScenicSpot


# url = "http://www.bytravel.cn/view/top10/index527.html"  # 安康市十大旅游景点
# url = "http://www.bytravel.cn/view/top10/index109.html"  # 北京市十大旅游景点
# url = "http://www.bytravel.cn/view/top10/index113.html"  # 内蒙古自治区十大旅游景点
# url = "http://www.bytravel.cn/view/top10/index116.html"  # 黑龙江省十大旅游景点
# url = "http://www.bytravel.cn/view/top10/index4322.html" #英格兰威尔特郡十大旅游景点


def main(f, t):
    top10ScenicSpotLinks = top10List(f, t)
    # global url
    # top10ScenicSpotLinks = [url]
    for link in top10ScenicSpotLinks:
        url = link['url']
        try:
            strippedOneCityTop10ScenicSopts(url)
            try:
                print(link['index'], getAcronym(link['title']),
                      link['title'], link['url'], ' is done.')
            except Exception as ex:
                print(url, ' is done.')
                pass
        except Exception as ex:
            # print(ex)
            pass


# main()
