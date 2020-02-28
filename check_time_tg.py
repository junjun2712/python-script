#!/usr/bin/python
#coding:utf-8

import paramiko
import time
import os
import telegram

bot = telegram.Bot(token="xxxx:xxxxxxxxxxxxx")
chatID = "-xxxxxxxx"

port=22
IPs=["10.3.19.61","10.3.19.62","10.3.19.63"]

usernames="xxxx"
passwords="xxxx"
alarm_cmd="date +%s"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for i in range(len(IPs)):
    ssh.connect(IPs[i],port,usernames, passwords)
    stdin, stdout, stderr = ssh.exec_command(alarm_cmd)
    str=stdout.readlines()
    #print str[0]
    timelocal=int(time.time())
    #print (timelocal)
    timeremot=int(str[0])
    if timelocal - timeremot < -30:
       #print IPs[i],"fail 时间快了"
       statusfailone="time fail:",IPs[i]
       bot.sendMessage(chat_id=chatID, text=statusfailone)
    elif timelocal - timeremot > 30:
       #print IPs[i],"fail 时间慢了"
       statusfailtwo="time fail:",IPs[i]
       bot.sendMessage(chat_id=chatID, text=statusfailtwo)
    else:
       print IPs[i],"ok"
ssh.close()
