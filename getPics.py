import os
import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import configparser

config = None

def getConfig():
    configFile = '4p1w.conf'
    cf = configparser.ConfigParser()
    cf.read(configFile)
    global config
    config = dict(cf.items('getPics'))

# 在分类中获取单页中所有题目Url
def getQuizFromSinglePage(letterCount, pageNum):
    quizUrls = []
    pageUrl = 'http://4pics1word-answers.com/{0}-letters{1}/'.format(letterCount, '' if pageNum == 1 else '-' + str(pageNum))
    page = requests.get(pageUrl).text
    soup = bs(page, config['beautiful_soup_engine'])
    divs = soup.find_all('div', class_ = 'all')
    for div in divs:
        quizUrls.append(div.a['href'])
    return quizUrls

# 从单个Url中获取答案和图片
def getAnswerAndPics(quizUrl):
    returnDict = {}
    page = requests.get(quizUrl).text
    soup = bs(page, config['beautiful_soup_engine'])
    answer = soup.find('div', class_ = 'answer').string.replace('Answer: ', '').lower()
    picsTable = soup.find('table')
    pics = picsTable.tr.td.img['src']
    returnDict['answer'] = answer.strip()
    returnDict['pics'] = pics
    return returnDict

# 保存图片
def saveAnswerAndPics(apDict):
    filePath = config['pics_save_path']
    if not os.path.exists(filePath):
        os.mkdir(filePath)
    fileType = config['pics_save_type']
    if not os.path.exists('{0}{1}.{2}'.format(filePath, apDict['answer'], filePath)):
        urllib.request.urlretrieve(apDict['pics'], '{0}{1}.{2}'.format(filePath, apDict['answer'], fileType))

def getAllQuiz():
    for letterCount in range(3, 9):
        currPage = 1
        timeoutSecond = int(config['timeout_seconds']) # 超时限制秒数
        restartTimes = int(config['restart_times']) # 重试限制次数
        tryingTimes = 0 # 已重试次数
        while True:
            # 获取url和获取文件的几步可能会产生堵塞。若产生堵塞，在超时后抛出异常，捕获到异常时重新执行该轮获取。若多次重试失败，直接跳过该轮
            import socket
            socket.setdefaulttimeout(timeoutSecond)
            if tryingTimes == restartTimes:
                tryingTimes = 0
                currPage += 1
                continue
            try:
                quizes = getQuizFromSinglePage(letterCount, currPage)
                if len(quizes) == 0:
                    break
                for quiz in quizes:
                    ap = getAnswerAndPics(quiz)
                    saveAnswerAndPics(ap)
                print('page {0} of {1} letters - completed.'.format(currPage, letterCount))
                tryingTimes = 0
            except:
                print('page {0} of {1} letters - restarts.'.format(currPage, letterCount))
                tryingTimes += 1
                continue
            currPage += 1

if __name__ == '__main__':
    getConfig()
    getAllQuiz()
