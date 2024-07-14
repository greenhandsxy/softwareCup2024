import os
import random
import cv2
import dlib
import numpy as np
from tensorflow.keras.models import load_model
from PIL import ImageEnhance, Image


# 加载模型

model = load_model('./RLSBMX/tools/recognize_models/人脸表情识别模型.h5')
# model = load_model('./model_train/resnet_30次_最大池化_简化.h5')

# 定义表情标签
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
# 加载人脸检测器
face_cascade = cv2.CascadeClassifier('./RLSBMX/tools/haarcascade_frontalface_default.xml')
# 加载预测器
predictor = dlib.shape_predictor('./RLSBMX/tools/shape_predictor_68_face_landmarks.dat')


# opencv对象转换为pil对象
def cv2pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))


# pil对象转换为opencv对象
def pil2cv(img):
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


# 识别表情，返回表情
def det_emotion1(img):
    # 定义表情标签
    labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    # 进行人脸检测和表情识别
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        roi = np.expand_dims(roi_gray, axis=0)
        roi = np.expand_dims(roi, axis=-1)
        prediction = model.predict(roi)[0]
        label = labels[prediction.argmax()]
        return label


# 调色函数
def tiaose(face, c, b):
    contrast = ImageEnhance.Contrast(face)
    face = contrast.enhance(float(c))
    bright = ImageEnhance.Brightness(face)
    face = bright.enhance(float(b))
    return face


# 调整图片，截取人脸、旋转人脸、透明化处理、调色
def tiaozheng(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detector = dlib.get_frontal_face_detector()
    res = detector(gray, 1)

    shape = predictor(img, res[0])
    face = shape.parts()

    points = []
    point1 = [int((face[0].x + face[17].x) / 2), int((face[0].y + face[17].y) / 2)]
    point2 = [int((face[1].x + face[36].x) / 2), int((face[1].y + face[36].y) / 2)]
    point3 = [int((face[5].x + face[48].x) / 2), int((face[5].y + face[48].y) / 2)]
    point4 = [int((face[6].x + face[59].x) / 2), int((face[6].y + face[59].y) / 2)]
    point5 = [int((face[7].x + face[58].x) / 2), int((face[7].y + face[58].y) / 2)]
    point6 = [int((face[8].x + face[57].x) / 2), int((face[8].y + face[57].y) / 2)]
    point7 = [int((face[9].x + face[56].x) / 2), int((face[9].y + face[56].y) / 2)]
    point8 = [int((face[10].x + face[55].x) / 2), int((face[10].y + face[55].y) / 2)]
    point9 = [int((face[11].x + face[54].x) / 2), int((face[11].y + face[54].y) / 2)]
    point10 = [int((face[15].x + face[45].x) / 2), int((face[15].y + face[45].y) / 2)]
    point11 = [int((face[16].x + face[26].x) / 2), int((face[16].y + face[26].y) / 2)]
    for pos in face[17:27]:
        points.append([pos.x, pos.y])
    points.append(point11)
    points.append(point10)
    points.append(point11)
    points.append(point10)
    points.append(point9)
    points.append(point8)
    points.append(point7)
    points.append(point6)
    points.append(point5)
    points.append(point4)
    points.append(point3)
    points.append(point2)
    points.append(point1)
    # 面部提取
    face_pos = np.array(points, np.int32)
    mask = np.zeros(img.shape, np.uint8)
    mask = cv2.polylines(mask, [face_pos], True, (255, 255, 255))
    mask = cv2.fillPoly(mask, [face_pos], (255, 255, 255))
    mask = cv2.bitwise_and(mask, img)

    def cal_ang():
        faces = detector(img, 1)
        for face in faces:
            # 获取人脸特征点
            landmarks = predictor(img, face)
            # 提取左右眼中心点坐标
            left_eye_center = (landmarks.part(36).x + landmarks.part(39).x) // 2, (
                    landmarks.part(36).y + landmarks.part(39).y) // 2
            right_eye_center = (landmarks.part(42).x + landmarks.part(45).x) // 2, (
                    landmarks.part(42).y + landmarks.part(45).y) // 2
            # 计算旋转角度
            dy = right_eye_center[1] - left_eye_center[1]
            dx = right_eye_center[0] - left_eye_center[0]
            angle = cv2.fastAtan2(dy, dx)
            return angle

    angle = cal_ang()
    mask = cv2pil(mask)
    mask = mask.rotate(angle, expand=True)

    # 图像转为png格式
    mask = pil2cv(mask)  # PIL.Image转换为OpenCV格式
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)[1]  # 二值化
    contours = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]  # 查找轮廓
    max_con = sorted(contours, key=cv2.contourArea, reverse=True)[0]  # 获取最大轮廓
    x, y, w, h = cv2.boundingRect(max_con)  # 获取最大轮廓的边界框
    face = mask[y:(y + h), x:(x + w)]  # 裁剪出只包含人脸的图像区域
    # 转换为灰度图像和RGBA格式
    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    face = cv2.cvtColor(face, cv2.COLOR_GRAY2BGR)
    face = cv2pil(face)
    f_gray = face.convert('L')
    face = face.convert('RGBA')
    # 获取人脸图像的像素数据和灰度图像的像素数据
    f_data = face.getdata()
    g_data = f_gray.getdata()
    # 创建新的像素数据列表，根据灰度值设置透明度
    new_data = []
    for i in range(g_data.size[0] * g_data.size[1]):
        if g_data[i] == 0:
            new_data.append((f_data[i][0], f_data[i][1], f_data[i][2], 0))
        else:
            new_data.append((f_data[i][0], f_data[i][1], f_data[i][2], 255))
    # 将调整后的像素数据更新到人脸图像中
    face.putdata(new_data)

    # 调色
    # face = tiaose(face, ctrst_entry.get(), brt_entry.get())
    face = tiaose(face, 3.2, 2.2)

    # face.show()
    return face


# 图片合并
def hebing2(face, emotion):
    print(emotion)
    i = random.randint(0, 2)
    # template_path = "./tools/models/" + emotion + "_model/" + str(i + 1) + ".png"
    template_path = "./RLSBMX/tools/models/" + emotion + "_model/" + str(i + 1) + "_white.png"
    path = "./RLSBMX/adjust/" + emotion + ".txt"  # 文件夹路径
    print("调整path:" + path)
    print("模板path:" + template_path)
    list = []
    with open(path, 'r+', encoding='utf-8') as f:
        for line in f.readlines()[i:i + 1]:  # 按行读取每行
            list = line.split(" ")  # 切片去掉换行符，再以空格分割字符串，得到一个列表

    e_x, e_y, e_w, e_h, e_angle = (int(list[1]), int(list[2]),
                                   int(list[0]), int(list[0]), int(list[3]))

    face = face.rotate(e_angle, expand=True)
    fw, fh = face.size
    template = Image.open(template_path)
    face = face.resize((int(fw / (fh / e_h)), e_h), Image.ANTIALIAS)
    fw, fh = face.size
    face = face.crop((int((fw - e_w) / 2), 0, int((fw - e_w) / 2) + e_w, fh))
    # 实现透明
    template.paste(face, (e_x, e_y, e_x + e_w, e_y + e_h), mask=face.split()[-1])
    # template.save("result.png")  # 图片保存路径
    return template


def create_emoticon(input_image_path):
    # 加载模型
    # model = load_model('tools/recognize_models/人脸表情识别模型.h5')
    # ... 加载其他必要的库和资源 ...

    # 从输入路径加载图片
    input_image = cv2.imread(input_image_path)

    # 识别表情
    emotion = ""
    try:
        emotion = det_emotion1(input_image)
    except Exception as e:
        emotion = "Happy"

    # 调整图片
    adjusted_image = tiaozheng(input_image)

    if emotion == None:
        emotion = "Happy"

    # 合成表情包
    emoticon = hebing2(adjusted_image, emotion)

    return emoticon

    # 保存或返回表情包图片
    # emoticon.save("result6.png")  # 可以根据需求保存或返回结果


if __name__ == '__main__':
    input_image_path = "D:/code/show/test_img/saved_frame.jpg"
    create_emoticon(input_image_path)
