# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  本demo测试时运行的环境为：Windows + Python3.7
#  本demo测试成功运行时所安装的第三方库及其版本如下，您可自行逐一或者复制到一个新的txt文件利用pip一次性安装：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#
#  语音听写流式 WebAPI 接口调用示例 接口文档（必看）：https://doc.xfyun.cn/rest_api/语音听写（流式版）.html
#  webapi 听写服务参考帖子（必看）：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=38947&extra=
#  语音听写流式WebAPI 服务，热词使用方式：登陆开放平台https://www.xfyun.cn/后，找到控制台--我的应用---语音听写（流式）---服务管理--个性化热词，
#  设置热词
#  注意：热词只能在识别的时候会增加热词的识别权重，需要注意的是增加相应词条的识别率，但并不是绝对的，具体效果以您测试为准。
#  语音听写流式WebAPI 服务，方言试用方法：登陆开放平台https://www.xfyun.cn/后，找到控制台--我的应用---语音听写（流式）---服务管理--识别语种列表
#  可添加语种或方言，添加后会显示该方言的参数值
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import json
import os
from io import BytesIO

import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
import subprocess
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import json
from flask import Flask, request, jsonify
# from flask_cors import CORS
from werkzeug.utils import secure_filename
#
# app = Flask(__name__)
# CORS(app)  # 允许跨域请求
from flask import Blueprint

bp9 = Blueprint('blueprint9', __name__)

#FILE_NAME = 'voice.mp3'

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识
AUDIO_STYLE_LAG = ''
ALL_RESULT = ''

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, AudioFile):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.AudioFile = AudioFile

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo":1,"vad_eos":10000}

    # 生成url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        #print("date: ",date)
        #print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        #print('websocket url :', url)
        return url


# 收到websocket消息的处理
def on_message(ws, message):
    global ALL_RESULT
    try:
        code = json.loads(message)["code"]
        sid = json.loads(message)["sid"]
        if code != 0:
            errMsg = json.loads(message)["message"]
            #print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))

        else:
            # print('message:', message)
            data = json.loads(message)["data"]["result"]["ws"]
            # print(json.loads(message))
            result = ""
            for i in data:
                for w in i["cw"]:
                    result += w["w"]
            # print("sid:%s call success!,data is:%s" % (sid, json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ':'))))
            # print("result:%s" % result)
            ALL_RESULT += result
    except Exception as e:
        print("receive msg,but parse exception:", e)



# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws,a,b):
    pass
    # print("### closed ###")


# 收到websocket连接建立的处理
def on_open(ws):
    def run(*args):
        frameSize = 8000  # 每一帧的音频大小
        intervel = 1  # 发送音频间隔(单位:s)
        status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

        with open(wsParam.AudioFile, "rb") as fp:
            while True:
                buf = fp.read(frameSize)
                # 文件结束
                if not buf:
                    status = STATUS_LAST_FRAME
                    # print('not buf')
                # 第一帧处理
                # 发送第一帧音频，带business 参数
                # appid 必须带上，只需第一帧发送
                if status == STATUS_FIRST_FRAME:
                    # print('first frame')
                    d = {"common": wsParam.CommonArgs,
                         "business": wsParam.BusinessArgs,
                         "data": {"status": 0, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": AUDIO_STYLE_LAG}}
                                  # "encoding": "lame"}}
                                  # "encoding": "lame"}}
                    d = json.dumps(d)
                    ws.send(d)
                    status = STATUS_CONTINUE_FRAME
                # 中间帧处理
                elif status == STATUS_CONTINUE_FRAME:
                    d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": AUDIO_STYLE_LAG}}
                                  # "encoding": "lame"}}
                                  # "encoding": "lame"}}
                    ws.send(json.dumps(d))
                # 最后一帧处理
                elif status == STATUS_LAST_FRAME:
                    d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": AUDIO_STYLE_LAG}}
                                  # "encoding": "lame"}}
                                  # "encoding": "lame"}}
                    ws.send(json.dumps(d))
                    time.sleep(1)
                    break
                # print(d)
                # 模拟音频采样间隔
                time.sleep(intervel)
        ws.close()

    thread.start_new_thread(run, ())

def type2Encoding(file_name):
    global AUDIO_STYLE_LAG
    if '.mp3' in file_name:
        AUDIO_STYLE_LAG = "lame"
    elif '.pcm' in file_name:
        AUDIO_STYLE_LAG = "raw"
    elif '.speex' in file_name and '8k' in file_name:
        AUDIO_STYLE_LAG = "speex"
    elif '.speex' in file_name and '16k' in file_name:
        AUDIO_STYLE_LAG = "speex-wb"
    # print(AUDIO_STYLE_LAG)

def interpret_audio(audio_file):
    time1 = datetime.now()
    # audio_file_name = 'iat_mp3_16k.mp3'
    audio_file_name = 'voice.mp3'
    global wsParam
    type2Encoding(audio_file_name)
    wsParam = Ws_Param(APPID='6620d657', APISecret='MGZlMmNmMjk4NzRkNDAxYjM1YzA3NDkx',
                       APIKey='6f7b83161e12d7cc20c8bd2db6211914',
                       AudioFile=audio_file)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    time2 = datetime.now()
    # print(time2 - time1)
    # print(ALL_RESULT)
    return ALL_RESULT

@bp9.route('/voice', methods=['POST'])
def voice_upload():
    # 检查是否有文件在请求中
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400
    file = request.files['file']
    # 如果用户没有选择文件，浏览器也会提交一个没有文件名的空部分
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    # 直接使用固定文件名保存文件
    filename = secure_filename('input.mp3')
    input_filepath = os.path.join('语音翻译', filename)
    output_filepath = os.path.join('语音翻译', 'voice.mp3')


    # 保存文件
    file.save(input_filepath)
    
    # 构建ffmpeg命令
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_filepath,  # 输入文件
        '-ar', '16000',  # 设置音频采样率为16000Hz
        '-ac', '1',      # 设置音频通道数为1（单声道）
        output_filepath   # 输出文件
    ]

    try:
        # 调用ffmpeg命令
        result = subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 如果命令执行成功，输出文件应该已经生成
        print(f"Conversion successful. Output file: {'voice.mp3'}")
    except subprocess.CalledProcessError as e:
        # 如果ffmpeg命令执行失败，打印错误信息
        print(f"An error occurred while converting the audio file: {e.stderr.decode()}")

    # 处理文件
    global ALL_RESULT
    ALL_RESULT=''
    result = interpret_audio(output_filepath)
    os.remove(input_filepath)
    os.remove(output_filepath)

    # 返回结果
    return jsonify({'message': result})

# if __name__ == "__main__":
#     app.run(port=5000)
    # audio_file_name = 'tts.mp3'
    # print('最终结果为：', interpret_audio(audio_file_name))
