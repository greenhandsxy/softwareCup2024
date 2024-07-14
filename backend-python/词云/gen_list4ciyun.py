import re

from flask import Flask, request, jsonify
from sparkai.llm.llm import ChatSparkLLM
from sparkai.core.messages import ChatMessage
# from flask_cors import CORS
from typing import Any
from sparkai.core.callbacks import BaseCallbackHandler

# 各模块公用API模块需要加上这几行，然后再参考一下调用格式
import os
from dotenv import load_dotenv

load_dotenv()

# app = Flask(__name__)
# CORS(app)  # 允许跨域请求
from flask import Blueprint

bp8 = Blueprint('blueprint8', __name__)

# 回调处理程序
class ChunkPrint(BaseCallbackHandler):

    def __init__(self) -> None:
        self.generated_text = ""  # 存储生成的文本

    def on_llm_new_token(self, token: str, *, chunk: None, **kwargs: Any) -> None:
        self.generated_text += token  # 将生成的文本添加到 generated_text 中


def process_text(text):
    spark = ChatSparkLLM(
        # spark_api_url=os.environ["SPARKAI_URL"],
        # spark_app_id=os.environ["SPARKAI_APP_ID"],
        # spark_api_key=os.environ["SPARKAI_API_KEY"],
        # spark_api_secret=os.environ["SPARKAI_API_SECRET"],
        # spark_llm_domain=os.environ["SPARKAI_DOMAIN"],
        # 修改
        spark_api_url="wss://spark-api.xf-yun.com/v3.5/chat",
        spark_app_id="560e7cbc",
        spark_api_key='2fece4d84ef307003b8589a81acfec6d',
        spark_api_secret='ODYwMDJiMDVkYmNiZmI1MTFjZjE3Nzhm',
        spark_llm_domain="generalv3.5",
        streaming=True,
    )

    messages = [ChatMessage(
        role="user",
        content=text
    )]
    handler = ChunkPrint()
    spark.generate([messages], callbacks=[handler])

    # print(handler.generated_text)

    return handler.generated_text


# 处理 OPTIONS 请求
@bp8.route('/word_cloud', methods=['POST', 'OPTIONS'])
def generate_word():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return '', 204, headers
    else:
        data = request.json
        text = data['text']
        res = '{}的关键词有哪些，请列举10个，每个关键词之间请用\",\"分隔，除了关键词和\",\"以外不要打印其他任何内容'.format(text)
        ls_keyword = process_text(res)
        ls_keyword = re.sub('\'', '', ls_keyword)
        ls_keyword = list(map(str, ls_keyword.split('，')))
        print(ls_keyword)
        return jsonify({'ls_keyword': ls_keyword})

# if __name__ == '__main__':
#     app.run(port=5008)
    # class_name = '网络测量与协议分析'
    # ls_keyword = process_text(
    #     '{}的关键词有哪些，请列举10个，每个关键词之间请用\",\"分隔，除了关键词和\",\"以外不要打印其他任何内容'.format(class_name))
    # ls_keyword = re.sub('\'', '', ls_keyword)
    # ls_keyword = list(map(str,ls_keyword.split('，')))
    # print(ls_keyword)  # 列表形式,选取前10个
