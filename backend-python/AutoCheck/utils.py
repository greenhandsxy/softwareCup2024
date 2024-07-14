import base64

import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# 定义LSTM模型
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)  # 隐藏状态初始化
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)  # 单元状态初始化

        out, _ = self.lstm(x, (h0, c0))  # LSTM前向传播
        out = self.linear(out[:, -1, :])  # 取序列最后一个时间点的输出
        return out


def prepare_data(seq, input_size):
    """
    将一维时序数据转换为适合LSTM模型的三维张量。
    """
    seq = torch.tensor(seq, dtype=torch.float32)  # 将序列转换为张量
    seq = seq.view(1, -1, input_size)  # 重塑为 (batch_size, seq_length, input_size)
    return seq


def time_series_prediction(seq, model, device, input_size, output_size):

    seq = prepare_data(seq, input_size).to(device)  # 准备数据并移动到指定设备
    model.to(device)
    # model.load_state_dict(torch.load('model.pth\pkl\pt')  # 载入check_point，即先前训练好的参数
    model.eval()  # 设置模型为评估模式
    with torch.no_grad():  # 关闭梯度计算
        prediction = model(seq)

    return prediction.item()

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

def forcast_w(time_series_data):
    # 一维时序数据，到时候可以从数据库传入，这里只是一个测试
    # time_series_data = [0.0738, 1.3730, 0.9317, 0.9053, 0.9336, 0.7675, 0.1406, 0.6969, 1.3919, 0.6989, 3.14, 5.68]

    input_size = len(time_series_data)

    output_size = 1

    # model需要是一个已经训练好的LSTM模型实例
    model = LSTMModel(input_size, hidden_size=50, num_layers=2, output_size=output_size)
    # device = torch.device('cuda')  # 若有GPU也可以使用 'cuda'

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # 进行预测
    prediction = time_series_prediction(time_series_data, model, device, input_size, output_size)
    print('prediction:',prediction)

    # 绘制时序数据和预测值
    plt.figure(figsize=(8, 5))  # 设置图形的大小
    plt.plot(time_series_data, label='Original Data', color='blue')  # 绘制原始数据
    plt.plot(len(time_series_data), prediction, 'ro', label='Prediction')  # 绘制预测点，使用红色圆圈

    # 添加图例
    plt.legend()

    # 添加标题和轴标签
    plt.title('Time Series Data and Predictions')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.savefig('./img/time_series.png')
    # 显示图形
    plt.show()

    return return_img_stream('./img/time_series.png'), prediction

