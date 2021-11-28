import urllib.request
import re
import os
from bs4 import BeautifulSoup
from scenic_spot import Top10ScenicSpotLink
from utils import existingContentByReqURLforTop10, writeFile, readFile, getAcronym, readDirectory
import json


index = 0
top10ScenicSpotLinks = []


def grabContentFunT(url, html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.head.title.string
    location = ''
    try:
        location = soup.select(
            'head meta[name="location"]')[0]['content']
    except Exception:
        pass
    nav = ''
    try:
        navDesc = soup.select(
            'body div#page_left > div')[0].stripped_strings
        for desc in navDesc:
            nav += repr(desc).replace("'", "")
        nav = nav.replace("您现在的位置：首页>", "")
    except Exception:
        pass

    global index
    index += 1
    top10ScenicSpotLink = Top10ScenicSpotLink(index, title, url, location, nav)
    top10ScenicSpotLinks.append(top10ScenicSpotLink)
    print(index, title, url, location, nav)


def doubleCheckReallyNeedRegenerate(eIntrests):
    for eIntrest in eIntrests:
        id = getAcronym(eIntrest)
        if os.path.exists("F:/GitWorkspace/spider/data/scenic_spots/"+id+".json") == False:
            return True
    return False


def top10ListForCheckModle(f, t):
    top10ScenicSpotLinks = []
    fileNames = readDirectory('F:/GitWorkspace/spider/data')
    jsonText = readFile('F:/GitWorkspace/spider/data', '1_TOP_10_LIST.json')
    for link in jsonText:
        index = int(link['index'])
        if index < f or index > t:
            continue
        title = link['title']
        fileName = getAcronym(title)
        existingFiles = list(filter(lambda fn: fn.replace(".json", '') ==
                                    fileName, fileNames))
        reGenerate = False
        eIntrests = []
        try:
            existingIntrests = readFile(
                "F:/GitWorkspace/spider/data", fileName+".json")
            for existingIntrest in existingIntrests['scenicSpots']:
                name = existingIntrest['name']
                eIntrests.append(name)
        except Exception as ex:
            pass
        reGenerate = len(eIntrests) != 10
        readyForReGenerate = len(existingFiles) == 0 or reGenerate
        if readyForReGenerate and doubleCheckReallyNeedRegenerate(eIntrests) == False:
            readyForReGenerate = False
        if readyForReGenerate:
            top10ScenicSpotLinks.append(link)
            print(link['index'], getAcronym(link['title']),
                  link['title'], link['url'], ' is NOT done.')
        else:
            # print(link['index'], getAcronym(link['title']),
            #       link['title'], link['url'], ' is done.')
            pass
    return top10ScenicSpotLinks


isTesting = False
isCheckModle = True


def top10List(f, t):
    if isCheckModle:
        return top10ListForCheckModle(f, t)
    i = f
    max = 4500
    if isTesting:
        i = 134
        max = 135
    while i < t:
        i += 1
        try:
            existingContentByReqURLforTop10(
                'http://www.bytravel.cn/view/top10/index' + str(i)+'.html', grabContentFunT)
        except Exception as err:
            # print(err)
            pass

    jsonStr = json.dumps(
        top10ScenicSpotLinks, ensure_ascii=False, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    writeFile('F:/GitWorkspace/spider/data',
              '1_TOP_10_LIST.json', jsonStr)
    return top10ScenicSpotLinks


# top10List()
