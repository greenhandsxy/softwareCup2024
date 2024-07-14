from flask import Flask, render_template
from flask_cors import CORS


from AI生成PPT.AIPPT import bp1
from OCR.ocr_mix_instig import bp2
from Transformer时序预测.main import bp3
from 机器翻译.WebITS import bp4
from 评估学生表现分数.main import bp5
from AutoCheck.httpserver_prob import bp6
from 讯飞星火认知大模型.后端 import bp7
from 词云.gen_list4ciyun import bp8
from 语音翻译.iat_ws_python3 import bp9
from RLSBMX.makeImg import bp10
from OCR.WebITRTeach import bp11

from AutoCheck.InterfaceAPI import *

app = Flask(__name__, template_folder='AutoCheck/templates')
CORS(app)

# 注册蓝图并指定路径
app.register_blueprint(bp1)
app.register_blueprint(bp2)
app.register_blueprint(bp3)
app.register_blueprint(bp4)
app.register_blueprint(bp5)
app.register_blueprint(bp6)
app.register_blueprint(bp7)
app.register_blueprint(bp8)
app.register_blueprint(bp9)
app.register_blueprint(bp10)
app.register_blueprint(bp11)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
