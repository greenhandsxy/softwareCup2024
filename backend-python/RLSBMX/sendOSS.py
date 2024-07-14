import oss2
import os
from datetime import datetime, timedelta


def sendOSS(file_path):
    # 配置你的阿里云OSS信息
    #auth = oss2.Auth('', '')
    # 请将下面的endpoint替换为你的实际OSS服务地址
    #bucket = oss2.Bucket(auth, '', '')

    # 定义OSS中的目标路径，包括目录
    #target_dir = ''
    # 从文件名中获取不带路径的纯文件名
    filename = os.path.basename(file_path)
    object_key = target_dir + filename

    # 检查文件是否存在
    if os.path.isfile(file_path):
        # 上传文件到OSS指定目录
        try:
            bucket.put_object_from_file(object_key, file_path)
            print(f"File '{filename}' uploaded to OSS directory '{target_dir}' successfully.")

            # 设置预签名URL的有效期为10年
            presigned_url = bucket.sign_url('GET', object_key, 60*60*24*365)

            return presigned_url
        except oss2.exceptions.OSSException as e:
            print(f"Error occurred: {e}")
    else:
        print("File not found at the specified path.")
        return None

if __name__ == '__main__':
    file_path = 'D:\\A_MASTER\\software-cup-python\\RLSBMX\\uploads\\img_from_frontend_emoticon.png'
    result = sendOSS(file_path)
    if result:
        print(f"Public URL for the image: {result}")
