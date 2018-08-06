from urllib import request
import os
import re

def downloadlist():
    with request.urlopen('http://jx3gc.autoupdate.kingsoft.com/jx3hd/zhcn_hd/serverlist/serverlist.ini') as f:
        data = f.read()
    with open("severlist.ini", "wb") as code:
        code.write(data);

def checkFile(fileName):
    return os.path.exists(fileName)

def parse():
    serverlist = dict()
    fileName = "severlist.ini"
    if(not checkFile(fileName)):
        downloadlist()
    with open(fileName, "r", encoding='gbk') as f:
        for line in f:
            str = re.split(r'\s+',line)
            fu = dict()
            fu["name"] = str[1]
            fu["ip"] = str[3]
            fu["port"] = str[4]
            serverlist.setdefault(str[0], []).append(fu)
    return serverlist

