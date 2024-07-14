from flask import Flask, request, jsonify
from sparkai.llm.llm import ChatSparkLLM
from sparkai.core.messages import ChatMessage
from flask_cors import CORS
from typing import Any
from sparkai.core.callbacks import BaseCallbackHandler
from flask import Blueprint

bp7 = Blueprint('blueprint7', __name__)

#各模块公用API模块需要加上这几行，然后再参考一下调用格式
import os
from dotenv import load_dotenv
load_dotenv()

# app = Flask(__name__)
# CORS(app)  # 允许跨域请求

#回调处理程序
class ChunkPrint(BaseCallbackHandler):

    def __init__(self) -> None:
        self.generated_text = ""  # 存储生成的文本

    def on_llm_new_token(self, token: str, *, chunk: None, **kwargs: Any) -> None:
        self.generated_text += token  # 将生成的文本添加到 generated_text 中

def process_text(text):
    spark = ChatSparkLLM(
        spark_api_url=os.environ["SPARKAI_URL"],
        spark_app_id=os.environ["SPARKAI_APP_ID"],
        spark_api_key=os.environ["SPARKAI_API_KEY"],
        spark_api_secret=os.environ["SPARKAI_API_SECRET"],
        spark_llm_domain=os.environ["SPARKAI_DOMAIN"],
        streaming=True,
    )

    messages = [ChatMessage(
        role="user",
        content=text
    )]
    handler = ChunkPrint()
    spark.generate([messages], callbacks=[handler])

    print(handler.generated_text)

    return handler.generated_text

# 处理 OPTIONS 请求
@bp7.route('/process_text', methods=['POST', 'OPTIONS'])
def handle_text():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return '', 204, headers
    else:
        data = request.json
        text = data['text']
        result_text = process_text(text)
        return jsonify({'result': result_text})
