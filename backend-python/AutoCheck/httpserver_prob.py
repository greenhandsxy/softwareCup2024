import json
import logging
import threading
import base64
import flask
import os
from flask import Flask, request
# from 自动批改.InterfaceAPI import *
# from flask_cors import CORS
from AutoCheck.WebITR import *

# app = Flask(__name__, template_folder='templates')
# CORS(app)  # 允许所有域名的跨域请求
from flask import Blueprint

bp6 = Blueprint('blueprint6', __name__)

def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """

    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        # print(img_stream)
        img_stream = base64.b64encode(img_stream).decode()

    return img_stream

@bp6.route('/autocheck', methods=["GET", 'POST'])
def model_upload():
    # try:
    # We will save the file to disk for possible data collection.
    #print(request.files.keys())
    model_file = flask.request.files['file']

    # filename_ = werkzeug.secure_filename(model_file.filename)
    # filename = os.path.join(UPLOAD_MODEL_FOLDER, filename_)
    # filename = './img/{}'.format(model_file.filename.split('.')[0]+'_check_result.'+model_file.filename.split('.')[1])
    filename = './AutoCheck/img/{}'.format(model_file.filename)
    model_file.save(filename)
    func_cal(filename)

    print(filename)
    # filename = filename
    # imagefile.save(filename)
    # print(filename.split('.')[0]+'_check_result.'+filename.split('.')[1])
    img_stream_ = return_img_stream(os.path.abspath(filename[:-4]+'_check_result'+filename[-4:]))
    logging.info('Saving to %s.', filename)
    # image = exifutil.open_oriented_im(filename)
    return flask.render_template(
        'ret_img.html', img_stream=img_stream_,
        result=(True, '上传成功')
    )
    # return json.dumps({"return": 2})
    # start_from_terminal(app)


# except Exception as err:
#     print('error', err)
#     logging.info('Uploaded model open error: %s', err)
#     # return flask.render_template(
#     #     'client_html_func', has_result=True,
#     #     result=(False, 'Cannot open uploaded caffemodel.')
#     # )
#     return json.dumps({"return": 3})


# def worker(host, port):
#     # 启动端口监控
#     app.run(host=host, port=port)
#
#
# if __name__ == "__main__":
#     host = "127.0.0.1"  # 服务端IP地址
#     port = 5002  # 服务端监听端口号
#     new = threading.Thread(target=worker, args=(host, port,), name='test')
#     new.start()
