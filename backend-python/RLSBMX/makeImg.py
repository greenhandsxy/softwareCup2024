import base64

from PIL import Image  # 确保已经导入PIL或Pillow库
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
from RLSBMX.tool import *
import os

from RLSBMX.sendOSS import sendOSS

bp10 = Blueprint('upload', __name__)

# app = Flask(__name__)
# api = Api(app)
# CORS(app)  # 允许跨域请求
# CORS(app, resources={r"/uploads/*": {"origins": "*"}})

# 指定上传图片的保存目录
current_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(current_dir, "uploads")

@bp10.route('/uploadImage', methods=['POST'])
def upload_image():
    # 确保“uploads”目录存在
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    if 'image' not in request.files:
        return jsonify({"message": "No image file found"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    # 验证文件扩展名
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    # if not file.filename.lower().endswith(allowed_extensions):
    #     return jsonify({"message": "Invalid file format"}), 400

    # 生成安全的文件名
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    print(file_path)

    # 保存文件
    file.save(file_path)
    print(f"Image '{filename}' uploaded successfully.")

    # 调用工具方法处理图片
    try:
        # # 加载并转换图像模式
        # original_image = Image.open(file_path)
        # if original_image.mode == 'RGBA':
        #     original_image = original_image.convert('RGB')  # 将RGBA转换为RGB模式

        # emoticon = tool.create_emoticon(file_path)
        emoticon = create_emoticon(file_path)  # 确保create_emoticon能处理RGB模式的图像
        emoticon_path = file_path.replace(".png", "_emoticon.png")  # 保存处理后的图片

        # 确保emoticon对象是PIL.Image类型，并且在保存前进行必要的模式检查或转换
        if emoticon.mode == 'RGBA':
            emoticon = emoticon.convert('RGB')  # 转换为RGB模式再保存

        emoticon.save(emoticon_path)
        ossUrl = sendOSS(emoticon_path)
        # print(ossUrl)

        return jsonify({"message": "Image processed successfully", "url": ossUrl})

        # return jsonify({"message": "Image processed successfully"})
    except Exception as e:
        print(f"Error processing image: {e}")
        os.remove(file_path)  # 删除处理失败的图片
        return jsonify({"message": "Failed to process image"})

# api.add_resource(UploadImage, '/uploadImage')

# if __name__ == '__main__':
    # app.run(debug=True, port=5002)

