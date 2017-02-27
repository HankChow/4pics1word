# 4pics1word
---
### 背景
这个项目是我在玩《4 pics 1 word》游戏的时候，在金币不足的情况下，为了强行过关而写的。

### 运行这个项目需要
* 网络
* Python3.x
    * requests 库
    * BeautifilSoup4 库
    * PIL 库

### 如何运行这个项目
1. git clone 这个项目；
2. 设置好配置文件 `4p1w.conf` 中的参数；
3. 运行 `getPics.py`，从网络上下载所有大图（耗时视网速而定）；
4. 上一步完成后，运行 `cropPics.py`，自动把所有大图切分成小图；
5. 上一步完成后，带参数运行 `identify.py`，参数格式为 `python identify.py {该题单词长度} {图片1} [{图片2}[ {图片3}[ 图片4]]]`
