#!/usr/bin/python
import paramiko
import time

port=22
IPs=["172.18.230.91","172.18.230.101"]
usernames="root"
passwords="root"
#timelocal=int(time.time())
alarm_cmd="date +%s"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for i in range(len(IPs)):
    ssh.connect(IPs[i],port,usernames, passwords)
    stdin, stdout, stderr = ssh.exec_command(alarm_cmd)
    str=stdout.readlines()
    print str[0]
    timelocal=int(time.time())
    print (timelocal)
    timeremot=int(str[0])
    if timelocal - timeremot < -30:
       print IPs[i],"fail"
    elif timelocal - timeremot > 30:
       print IPs[i],"fail"
    else:
       print IPs[i],"ok"
ssh.close()
