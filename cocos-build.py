# -*- coding:utf-8 -*-
import shutil
import platform
import os
import sys
import paramiko

def project_build():
    
    os.system("C:\CocosCreator_2.1.3\CocosCreator.exe --path D:\\jenkins\\workspace\\test_cocos_pack_new\\H5Framework_cc --build platform=web-mobile;debug=true;sourceMaps=true;mergeStartScene=true;md5Cache=true")

def remote_copy(branch):
    if branch == "develop":
        os.system("D:\jenkins\pscp.exe -l dev -pw dev -r D:\\jenkins\\workspace\\test_cocos_pack_new\\H5Framework_cc\\build\\web-mobile dev@172.18.11.254:/home/dev/")
    if branch == "test":
        os.system("D:\jenkins\pscp.exe -l test -pw test -r D:\\jenkins\\workspace\\test_cocos_pack_new\\H5Framework_cc\\build\\web-mobile test@172.18.11.254:/home/test/")
    if branch == "gate2":
        os.system("D:\jenkins\pscp.exe -l sihai -pw sihai -r D:\\jenkins\\workspace\\test_cocos_pack_new\\H5Framework_cc\\build\\web-mobile sihai@172.18.11.254:/home/sihai/")
def ssh_cmd(host, username, password, cmd):
    try:
        ssh_fd = paramiko.SSHClient()
        ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("ssh connecting now ...")
        ssh_fd.connect(host, username = username, password = password )
        print("ssh connected ...")
        stdin, stdout, stderr = ssh_fd.exec_command(cmd)
        list = stdout.readlines()     
        print( list )  
        ssh_fd.close()
    except Exception as e:
        print( 'ssh %s@%s: %s' % (username, host, e) )
        exit(1)
def remote_deployment(host, username, password, branch):
    print("remote deployment")
    cmd = "/usr/bin/echo no according branch"
    if branch == "develop":
        cmd = "/bin/sh /root/k8s-new/web_mobile/push_deploy_win_dev.sh"
    if branch == "test":
        cmd = "/bin/sh /root/k8s-new/web_mobile/push_deploy_win_test.sh"
    if branch == "gate2":
        cmd = "/bin/sh /root/k8s-new/web_mobile/push_deploy_win_gate2.sh"
    ssh_cmd(host, username, password, cmd)
def main():
    branch = "test"
    if(len(sys.argv) == 2):
        branch = sys.argv[1]
    else:
        print("no branch parameter")
        exit(100)     
    host = "172.18.11.254"
    username = "root"
    password = "sihai@2019"
    os.chdir("D:\jenkins")
    project_build()
    remote_copy(branch)
    remote_deployment(host, username, password, branch)
if __name__ == '__main__':
    main()
