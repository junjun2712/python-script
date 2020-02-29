#!/usr/bin/env python
# -*-coding:utf-8 -*-

import sys
import os


name=sys.argv[1]
namelist=name.split(" ")
print (namelist)
cmdcd="cd /d D:\jenkins\workspace\ci-test-cocos-client-new\H5Framework_cc\\assets\games"

for i in range(len(namelist)):

    #print namelist[i]
    namelistone=namelist[i]
    #print (namelistone)
    cmddel=("rd /s/q %s" % namelistone)
    cmdgit=("git clone -b common http://gitlab.sihai.com/cocos-game/%s.git" % namelistone)
    #print (cmdthree)
    cmd=  cmdcd  + " && " + cmddel + " && " + cmdgit
    #print (cmd)
    
    #os.system(cmd)
    ret = os.system(cmd)
    #print (ret)
    if ret == 0 :
       print ("代码下载完成")
    else:
       cmd1=  cmdcd  + " && " + cmdgit
       os.system(cmd1)
       print ("代码下载完成")
