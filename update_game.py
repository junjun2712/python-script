#!/usr/bin/env python
# -*- coding:utf-8 -*-



import sys
import os
import subprocess
import time


game_repo_list = sys.argv[1].strip().split()
repo_branch = sys.argv[2]
jenkins_job_name = sys.argv[3]

game_base_dir = r"D:\jenkins\workspace\{}\H5Framework_cc\assets\games".format(jenkins_job_name)
game_repo_base_url = "http://gitlab.sihai.com/cocos-game"



def get_last_git_commit_ct_time(repo_name):
    """
    获取当前所有提交中的最新一次提交的 时间戳
    :param repo_name:
    """
    git_cmd = 'git log -n 1 --pretty=format:"%ct"'
    git_p = subprocess.run(git_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    last_commit_ct_time = int(git_p.stdout) if git_p.returncode == 0 else 10000000000
    return last_commit_ct_time


def show_git_commit_log(since_time, repo_name):
    """
    显示指定时间前之后的所有提交记录
    :param since_time: 时间窗口
    :param repo_name: 仓库名称
    """
    if since_time < 1:
        git_show_cmd = 'git log -n 1 --pretty=format:"Author: %cn:<%ce> %nCommitID: %H %nCommitTime: %cd %nMessage: %s %nRef: %d %n"'
    else:
        git_show_cmd = 'git log --since={}second'.format(since_time)
    os.chdir('{}\{}'.format(game_base_dir, repo_name))
    show_p = subprocess.run(git_show_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('{}\n'.format(show_p.stdout.decode('utf-8')))


def main():
    print('游戏列表: ', game_repo_list)
    for game_repo in game_repo_list:
        os.chdir(game_base_dir)  # 进入游戏项目家目录
        pull_cmd = 'git pull origin {}'.format(repo_branch)
        clone_cmd = 'git clone -b {} {}/{}.git'.format(repo_branch, game_repo_base_url, game_repo)

        # 目录存在就执行pull操作
        if os.path.isdir('{}\{}'.format(game_base_dir, game_repo)):
            os.chdir('{}\{}'.format(game_base_dir, game_repo))
            last_commit_ct_time = get_last_git_commit_ct_time(game_repo)
            #print('last time:', last_commit_ct_time)
            #print('### Pull {} ...'.format(game_repo))
            #print('pwd:', os.getcwd())
            #print('cmd:', pull_cmd)
            ret = subprocess.run(pull_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       # 目录不存在执行clone操作
        else:
            last_commit_ct_time = 10000000000
            print('### Clone {} ...'.format(game_repo))
            ret = subprocess.run(clone_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
        # 根据执行结果打印执行日志
        if ret.returncode == 0:
            #print('#out:', ret.stdout.decode('utf-8'))
            if 'Already up to date.' in str(ret.stdout.decode('utf-8')):
                print('\n>>> [{}]本次无更新 <<<'.format(game_repo.upper()))
            else:
                print('\n>>> [{}]本次更新记录:\n'.format(game_repo.upper())) 
                # 打印提交记录
                offset_ct_time = int(time.time())-last_commit_ct_time
                show_git_commit_log(offset_ct_time,game_repo)                
        else:
            print('#err:', ret.stderr.decode('utf-8'))
            
            

if __name__ == "__main__":
    main()
