import os
from PIL import Image
import configparser

config = None

def getConfig():
    configFile = '4p1w.conf'
    cf = configparser.ConfigParser()
    cf.read(configFile)
    global config
    config = dict(cf.items('cropPics'))

# 获取已保存的大图名称
def getPicsFileNames():
    picsPath = config['source_path']
    picsFiles = None
    for root, dirs, files in os.walk(picsPath):
        picsFiles = files
        break
    return picsFiles

# 裁剪为4张小图
def cropIntoFour(img):
    srcPath = config['source_path']
    dstPath = config['destination_path']
    if not os.path.exists(dstPath):
        os.mkdir(dstPath)
    spl = img.split('.')
    fileName = spl[0]
    fileType = spl[1]
    if not os.path.exists('{0}{1}_1.{2}'.format(dstPath, fileName, fileType)):
        im = Image.open(srcPath + img)
        imWidth = im.size[0] - 1
        imHeight = im.size[1] - 1
        cropSize = 137
        boxes = [(0, 0, cropSize, cropSize), (imWidth - cropSize, 0, imWidth, cropSize), (0, imHeight - cropSize, cropSize, imHeight), (imWidth - cropSize, imHeight - cropSize, imWidth, imHeight)]
        for i in range(len(boxes)):
            croppedPic = im.crop(boxes[i])
            croppedPic.save('{0}{1}_{2}.{3}'.format(dstPath, fileName, i + 1, fileType))
        print('{0} finishes cropping.'.format(img))
    else:
        print('{0} had been cropped.'.format(img))

def cropAllPics():
    allPics = getPicsFileNames()
    for i in allPics:
        try:
            cropIntoFour(i)
        except Exception as e:
            print(e)
            continue

if __name__ == '__main__':
    getConfig()
    cropAllPics()
