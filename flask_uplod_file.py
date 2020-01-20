# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request
import time, zipfile, os, base64

app = Flask(__name__)
FILE_SAVE_DIR = '/data/bin-game-app'
#UPLOAD_FOLDER = 'D:\\test'
app.config['UPLOAD_FOLDER'] = FILE_SAVE_DIR
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'jar','gz','bin','yaml','yml','json'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@app.route('/api/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files.get("file_name")
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = f.filename
        app_name = f.filename.rsplit('-')[0]
        app_dir = os.path.join(file_dir, app_name)
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        if fname.rsplit('.', 1)[1] == 'gz':
            tar_dir_name = fname.split('-')[1].split('.')[0]
            tar_dir_path = os.path.join(app_dir, tar_dir_name)
            if not os.path.exists(tar_dir_path):
                os.makedirs(tar_dir_path)
            tar_path = os.path.join(tar_dir_path, fname)
            f.save(tar_path)
            return jsonify({"code": 200, "msg":tar_path})
        else:
            file_path = os.path.join(app_dir, fname)
            f.save(file_path)
            return jsonify({"code": 200, "msg":file_path})
    else:
        return jsonify({"code": 1001, "errmsg": "上传失败"})




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)
