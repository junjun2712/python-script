#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author:   Marathon <jsdymarathon@itcom888.com>
# Date:     2020/2/21 4:15
# Location: Manila
# Desc:     备份服务器上传服务

from flask import Flask, jsonify, request
import os
import hashlib
import subprocess

app = Flask(__name__)

FILE_SAVE_DIR = '/data/dyimage'
app.config['UPLOAD_FOLDER'] = FILE_SAVE_DIR


def get_file_md5(_file):
    """计算文件的md5
    :param _file: 要计算md5的文件
    :return md5
    """
    global ERROR_MSG
    md5_obj = hashlib.md5()
    try:
        with open(_file, 'rb') as f:
            for data in f:
                md5_obj.update(data)
            return md5_obj.hexdigest()
    except OSError as ERROR_MSG:
        print(ERROR_MSG)
        return False

def merge_upload_file(work_dir, merge_file):
    """合并上传的分片文件
    :param work_dir: 要执行合并操作时的工作目录
    :param merge_file: 要合并的文件
    """
    global ERROR_MSG
    merge_cmd = 'cd {} && cat {}.* > {}'.format(work_dir, merge_file, merge_file)
    p = subprocess.Popen(merge_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    if p.returncode == 0:
        print('run_code: {}; msg: {}'.format(p.returncode, p.stdout.read()))
    else:
        ERROR_MSG = p.stderr.read()
        print('run_code: {}; msg: {}'.format(p.returncode, ERROR_MSG))


def rm_split_file(work_dir, split_file):
    """删除分片文件
    :param work_dir: 要执行删除操作的工作目录
    :param split_file: 要删除的分片文件
    """
    global ERROR_MSG
    rm_cmd = 'cd {} && rm -f {}.*'.format(work_dir, split_file)
    p = subprocess.Popen(rm_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    if p.returncode == 0:
        print('run_code: {}; msg: {}'.format(p.returncode, p.stdout.read()))
    else:
        ERROR_MSG = p.stderr.read()
        print('run_code: {}; msg: {}'.format(p.returncode, ERROR_MSG))



@app.route('/api/merge', methods=['POST'], strict_slashes=False)
def api_merge():
    """大文件上传完毕后，文件合并接口"""
    root_dir = app.config['UPLOAD_FOLDER']
    end_tag = request.headers.get('End-tag')
    file_md5 = request.headers.get('Md5')
    file_name = request.headers.get('File')
    project_dir = request.headers.get('Project')
    #print(request.headers)

    if end_tag:
        save_dir_path = '{}/{}'.format(root_dir, project_dir)
        merge_upload_file(save_dir_path, file_name)
        save_file_md5 = get_file_md5('{}/{}'.format(save_dir_path, file_name))
        if save_file_md5 == file_md5:  # 校验文件OK，把分片删除
            rm_split_file(save_dir_path, file_name)
            return jsonify({"code": 200, "msg": "[{}] is merged with [{}]; MD5: {}".format(
                file_name, save_dir_path, save_file_md5)})
        else:
            return jsonify({"code": 555, "msg": "{}".format(ERROR_MSG)})
    else:
        return jsonify({"code": 444, "msg": "Missing necessary parameters"})



@app.route('/api/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    """文件上传接口"""
    root_dir = app.config['UPLOAD_FOLDER']
    upload_file = request.files.get('file_name')
    project_dir = request.headers.get('Project')
    #print(request.headers)

    if upload_file and project_dir:
        # 考虑上传的文件带不带路径，全处理成不带路径的
        _file = upload_file.filename.rsplit('/', 1)
        file_name = _file[1] if len(_file) == 2 else _file[0]
        # 各项目备份文件保存目录路径: /data/backup/gitlab
        save_dir_path = '{}/{}'.format(root_dir, project_dir)
        # 创建文件保存目录
        if not os.path.isdir(save_dir_path): os.makedirs(save_dir_path)
        save_file_path = '{}/{}'.format(save_dir_path, file_name)
        # 文件存在,则不再上传并返回提示信息
        if os.path.isfile(save_file_path):
            return jsonify({"code": 222, "msg": "file is exist"})
        upload_file.save(save_file_path)
        return jsonify({"code": 200, "msg": "{} is uploaded with {}".format(file_name, save_dir_path)})
    else:
        return jsonify({"code": 333, "msg": 'Please specify upload file and project name'})


if __name__ == '__main__':
    ERROR_MSG = ''
    app.run(host="0.0.0.0", port=8888, debug=True)
