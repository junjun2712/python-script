#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author:   Marathon <jsdymarathon@itcom888.com>
# Date:     2020/11/17 4:15
# Location: Manila
# Desc:     DY管理后台内部使用文件上传模块

import shutil
from flask import Flask, jsonify, request, make_response
from werkzeug.utils import secure_filename
import os
import hashlib
import settings
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = settings.MAX_UPLOAD_SIZE


# 验证上传文件类型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS


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


@app.route('/api/v1/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    """文件上传接口"""
    rsp_data = {}
    if request.method == "POST":
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            tmp_save_path = os.path.join(settings.SERVER_TMP_UPLOADS, filename)
            file.save(tmp_save_path)
            

            file_md5 = get_file_md5(tmp_save_path)
            # 以md5做为文件存储名称并保留原文件名的后缀
            md5_file_suffix = filename.rsplit('.')[1]
            md5_file_name = '{}.{}'.format(file_md5, md5_file_suffix)
            md5_file_save_dir = os.path.join(app.config['UPLOAD_FOLDER'], md5_file_suffix)
            md5_file_save_path = os.path.join(md5_file_save_dir, md5_file_name)

            if not os.path.isdir(md5_file_save_dir): os.mkdir(md5_file_save_dir)
            if not os.path.exists(md5_file_save_path):
                shutil.move(tmp_save_path, md5_file_save_path)
                rsp_data['msg'] = "[{}] File upload Successful".format(filename)
                rsp_data['uri'] = os.path.join(md5_file_suffix, md5_file_name)
                rsp_data['code'] = 200
            else:
                if os.path.exists(tmp_save_path): os.remove(tmp_save_path)
                rsp_data['msg'] = "File already exists"
                rsp_data['code'] = 201
        else:
            rsp_data['msg'] = "Unsupported file types"
            rsp_data['code'] = 500

        res = make_response(jsonify(rsp_data))
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Method'] = '*'
        res.headers['Access-Control-Allow-Headers'] = '*'
        return res


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=18888, debug=True)
