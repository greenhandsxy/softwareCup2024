import pymysql
import threading
import flask
from flask import Flask, request
from flask_cors import CORS
from AutoCheck.utils import *

app = Flask(__name__, template_folder='templates')
CORS(app)  # 允许所有域名的跨域请求


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


@app.route('/forecast/', methods=["GET", 'POST'])
def forecast():
    # 这里接收到一个数据，即用户当天的学习时长
    request_data = request.get_json()
    print(request_data)
    request_data = dict(request_data)
    # print(ret_id_fortnight(request_data['id'],request_data['today']))
    a = ret_id_fortnight(request_data['id'], request_data['today'])
    print(a)
    return a


def ret_id_fortnight(id, new):
    # 每一次访问都重新建立连接，避免不同连接访问冲突
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        db='test',
        charset='utf8'
    )
    cursor = connection.cursor()
    sql = 'select * from student_course where id = {}'.format(id)
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    # result = cursor.fetchone()   返回数据库查询的第一条信息，用元组显示
    # print(result)
    fortnight = list(map(int, result[0][7].split(',')))
    print(fortnight)
    # 更新14天数据，去掉最旧的，加上最新的
    fortnight.append(new)
    fortnight.pop(0)
    new_fortnight_str = ','.join(list(map(str, fortnight)))
    sql_update = 'update student_course set two_week_study = "{}" where id = {}'.format(new_fortnight_str, id)
    cursor.execute(sql_update)
    connection.commit()
    print(fortnight)
    img, prd = forcast_w(fortnight)
    # print(len(result[0][7].split(',')))
    # cursor.close()
    # connection.close()   #
    # return json.dumps({'return': fortnight})
    return flask.render_template(
        'ret_img.html', img_stream=img, fct_res=prd,
        result=(True, '上传成功')
    )


# ret_id_fortnight(5,6)

def worker(host, port):
    # 启动端口监控
    app.run(host=host, port=port)


if __name__ == "__main__":
    host = "127.0.0.1"  # 服务端IP地址
    port = 33000  # 服务端监听端口号
    new = threading.Thread(target=worker, args=(host, port,), name='test')
    new.start()
