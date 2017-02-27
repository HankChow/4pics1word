import os
import sys
from PIL import Image
import configparser

config = None

def getConfig():
    configFile = '4p1w.conf'
    cf = configparser.ConfigParser()
    cf.read(configFile)
    global config
    config = dict(cf.items('identify'))

# 图片hash
def dHash(img):
    resizeWidth = int(config['resize_width'])
    resizeHeight = int(config['resize_height'])
    originImage = Image.open(img) # 原图像
    smallerImage = originImage.resize((resizeWidth, resizeHeight)) # 缩小图像，图像越小速度越快，图像越大准确率越高
    grayscaleImage = smallerImage.convert('L') # 灰度化
    # 比较相邻像素
    pixels = list(grayscaleImage.getdata())
    difference = []
    for row in range(resizeHeight):
        rowStartIndex = row * resizeWidth
        for col in range(resizeWidth - 1):
            leftPixelIndex = rowStartIndex + col
            difference.append(pixels[leftPixelIndex] > pixels[leftPixelIndex + 1])
    # 转换为hash值
    decimalValue = 0
    hashString = ''
    for index, value in enumerate(difference):
        if value:
            decimalValue += value * (2 ** (index % 8))
        if index % 8 == 7:
            hashString += str(hex(decimalValue)[2:].rjust(2, '0'))
            decimalValue = 0
    return hashString

# 计算两个hash之间的Hamming距离
def calcHammingDistance(hash1, hash2):
    diff = (int(hash1, 16)) ^ (int(hash2, 16))
    return bin(diff).count('1')

def checkAllHash(targetHash):
    srcPath = config['subpics_path']
    picsFiles = None
    for root, dirs, files in os.walk(srcPath):
        picsFiles = files
        break
    for i in range(len(picsFiles)):
        picsFiles[i] = srcPath + picsFiles[i]
    picHashs = []
    for i in picsFiles:
        picHashs.append([str(calcHammingDistance(targetHash, dHash(i))).zfill(3), i])
    picHashs.sort()
    return picHashs

def getWordFromPic(img):
    spl_slash = img.split('/')
    spl_dot = spl_slash[-1].split('.')
    spl_ul = spl_dot[0].split('_')
    return spl_ul[0]

def getWordLengthFromPic(img):
    spl_slash = img.split('/')
    spl_dot = spl_slash[-1].split('.')
    spl_ul = spl_dot[0].split('_')
    return len(spl_ul[0])

if __name__ == '__main__':
    getConfig()
    picPath = []
    if len(sys.argv) >= 3:
        wordLength = sys.argv[1]
        for i in range(2, len(sys.argv)):
            picPath.append(sys.argv[i])
    else:
        print('Arguments not enough.')
        exit()
    for i in picPath:
        hashVal = dHash(i)
        result = checkAllHash(hashVal)
        printed = 0
        cursor = 0
        outputStr = '与 {0} 最相似的图片对应的 {1} 字单词为：'.format(i.split('/')[-1], wordLength)
        while True:
            if printed == 5:
                break
            if getWordLengthFromPic(result[cursor][1]) == int(wordLength):
                outputStr += getWordFromPic(result[cursor][1]) + ' '
                printed += 1
            cursor += 1
        print(outputStr)
