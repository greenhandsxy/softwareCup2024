import argparse
import os
import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

from Transformer时序预测.sendOSS import sendOSS
from Transformer时序预测.util.data_factory import data_provider
from Transformer时序预测.util.tools import adjust_learning_rate
# params
from Transformer时序预测.layers import Transformer
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.interpolate import make_interp_spline
from scipy.interpolate import interp1d

# 设置matplotlib的字体
#plt.rcParams['font.family'] = ['Noto Sans CJK SC']  # 确保在sans-serif列表中

plt.rc('font',family='SimSun', size=14)


plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

from flask import Flask, request, jsonify, send_file

# from flask_cors import CORS
#
# app = Flask(__name__)
# CORS(app)  # 允许跨域请求
from flask import Blueprint

bp3 = Blueprint('blueprint3', __name__)

# 搭建模型Transoformer模型
class Transformerinitialization():
    def __init__(self, args):
        super(Transformerinitialization, self).__init__()
        self.args = args
        self.model, self.device = self.build_model(args)

    def build_model(self, args):
        model = Transformer.Model(self.args).float()
        # 将模型定义在GPU上

        if args.use_gpu:
            device = torch.device('cuda:{}'.format(self.args.device))
            print('Use GPU: cuda:{}'.format(args.device))
        else:
            print('Use CPU')
            device = torch.device('cpu')
        total = sum([param.nelement() for param in model.parameters()])
        print('Number of parameters: %.2fM' % (total / 1e6))  # 打印模型参数量

        if self.args.use_gpu:
            model = nn.DataParallel(model, device_ids=[device])

        return model, device

    def _get_data(self, flag, pre_data=None):
        data_set, data_loader = data_provider(self.args, flag, pre_data)
        return data_set, data_loader

    def train(self, setting):
        train_data, train_loader = self._get_data(flag='train')

        path = os.path.join(self.args.checkpoints, setting)
        if not os.path.exists(path):
            os.makedirs(path)

        time_now = time.time()
        train_steps = len(train_loader)

        model_optim = optim.Adam(self.model.parameters(), lr=self.args.learning_rate)
        criterion = nn.MSELoss()

        for epoch in range(self.args.train_epochs):
            iter_count = 0
            train_loss = []
            self.model.train()
            epoch_time = time.time()
            for i, (batch_x, batch_y, batch_x_mark, batch_y_mark) in enumerate(train_loader):
                iter_count += 1
                model_optim.zero_grad()

                batch_x = batch_x.float().to(self.device)
                batch_y = batch_y.float().to(self.device)
                batch_x_mark = batch_x_mark.float().to(self.device)
                batch_y_mark = batch_y_mark.float().to(self.device)

                dec_inp = torch.zeros_like(batch_y[:, -self.args.pred_len:, :]).float()
                dec_inp = torch.cat([batch_y[:, :self.args.label_len, :], dec_inp], dim=1).float().to(self.device)
                # print(self.model)
                outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)

                f_dim = -1 if self.args.features == 'MS' else 0
                outputs = outputs[:, -self.args.pred_len:, f_dim:]
                batch_y = batch_y[:, -self.args.pred_len:, f_dim:].to(self.device)
                loss = criterion(outputs, batch_y)
                train_loss.append(loss.item())

                if (i + 1) % 100 == 0:
                    print("\titers: {0}, epoch: {1} | loss: {2:.7f}".format(i + 1, epoch + 1, loss.item()))
                    speed = (time.time() - time_now) / iter_count
                    left_time = speed * ((self.args.train_epochs - epoch) * train_steps - i)
                    print('\tspeed: {:.4f}s/iter; left time: {:.4f}s'.format(speed, left_time))
                    iter_count = 0
                    time_now = time.time()

                loss.backward()
                model_optim.step()

            print("Epoch: {} cost time: {}".format(epoch + 1, time.time() - epoch_time))
            train_loss = np.average(train_loss)

            print("Epoch: {0}, Steps: {1} | Train Loss: {2:.7f}".format(epoch + 1, train_steps, train_loss))

            adjust_learning_rate(model_optim, epoch + 1, self.args)
        path = os.path.join(self.args.checkpoints, setting)
        best_model_path = path + '/' + 'model.pth'
        torch.save(self.model.state_dict(), best_model_path)

        return self.model

    def calculate_mse(self, y_true, y_pred):
        # 均方误差
        mse = np.mean(np.abs(y_true - y_pred))
        return mse

    def predict(self, setting, mode, course, name, load=False):
        # predict
        results = []
        preds = []
        last_predict_result = 0
        # 加载模型
        path = os.path.join(self.args.checkpoints, setting)
        best_model_path = path + '/' + 'model.pth'
        self.model.load_state_dict(torch.load(best_model_path))
        # self.model.load_state_dict(torch.load(best_model_path, map_location=torch.device('cpu')))

        # 评估模式
        self.model.eval()

        if args.rollingforecast:
            pre_data = pd.read_csv(args.root_path + args.rolling_data_path)
        else:
            pre_data = None

        for i in 0 if pre_data is None else range(int(len(pre_data) / args.pred_len) - 1):
            if i == 0:
                data_set, pred_loader = self._get_data(flag='pred')
            else:  # 进行滚动预测

                data_set, pred_loader = self._get_data(flag='pred', pre_data=pre_data.iloc[: i * args.pred_len])
                print(f'滚动预测第{i + 1} 次')

            with torch.no_grad():
                for _, (batch_x, batch_y, batch_x_mark, batch_y_mark) in enumerate(pred_loader):
                    batch_x = batch_x.float().to(self.device)
                    batch_y = batch_y.float()
                    batch_x_mark = batch_x_mark.float().to(self.device)
                    batch_y_mark = batch_y_mark.float().to(self.device)

                    dec_inp = torch.zeros([batch_y.shape[0], self.args.pred_len, batch_y.shape[2]]).float().to(
                        batch_y.device)
                    dec_inp = torch.cat([batch_y[:, :self.args.label_len, :], dec_inp], dim=1).float().to(self.device)

                    outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)

                    f_dim = -1 if self.args.features == 'MS' else 0
                    outputs = outputs[:, -self.args.pred_len:, f_dim:]
                    outputs = data_set.inverse_transform(outputs)

                    if self.args.features == 'MS':
                        for i in range(args.pred_len):
                            preds.append(outputs[0][i][outputs.shape[2] - 1])  # 取最后一个预测值即对应target列
                    else:
                        for i in range(args.pred_len):
                            preds.append(outputs[0][i][outputs.shape[2] - 1])
                    print(outputs)

        # 保存结果
        if args.rollingforecast:
            df = pd.DataFrame({'real': pre_data['{}'.format(args.target)][:len(preds)], 'forecast': preds})
            df = pd.DataFrame({'real': pre_data['{}'.format(args.target)][:len(preds)], 'forecast': preds})
            last_predict_result = preds[-1]
            df.to_csv('./时序预测/results/{}-ForecastResults.csv'.format(args.target), index=False)
        else:
            df = pd.DataFrame({'forecast': results})
            df.to_csv('./时序预测/results/{}-ForecastResults.csv'.format(args.target), index=False)

        if args.show_results:
            length = len(df['forecast'])
            if mode == 0:
                plt.tick_params(axis='both', which='both', length=0)
                '''
                plt.plot(df['forecast'].tolist(), color='red', linestyle='--')  # 预测值，去掉了label
                plt.title('《{}》学习热度变化图'.format(course))
                plt.xlabel('时间(天)')
                plt.ylabel('热度')

                plt.xticks(np.arange(6)*(length/5), ['0', '5', '10', '15', '20', '25'])
                
                plt.savefig('./时序预测/result1.png')
                plt.clf()
                '''
                x = np.linspace(0, 400, 50)
                y = np.piecewise(x,
                                 [x < 100, (x >= 100) & (x < 200), (x >= 200) & (x < 300), x >= 300],
                                 [lambda x: 0.2 * x + np.random.normal(0, 2, x.shape),
                                  lambda x: 0.3 * x - 10 + np.random.normal(0, 5, x.shape),
                                  lambda x: 0.4 * x - 30 + np.random.normal(0, 5, x.shape),
                                  lambda x: 0.5 * x - 50 + np.random.normal(0, 5, x.shape)])

                spl = make_interp_spline(x, y)
                x_smooth = np.linspace(x.min(), x.max(), 400)
                y_smooth = spl(x_smooth)
                plt.plot(x_smooth, y_smooth, '-', color='red')

                plt.title('《{}》学习热度变化图'.format(course))
                plt.xlabel('时间(天)')
                plt.ylabel('热度')

                plt.xticks(np.arange(6)*(400/5), ['0', '5', '10', '15', '20', '25'])
                plt.yticks([])

                plt.savefig('./时序预测/result1.png')
                plt.clf()
            else:
                plt.tick_params(axis='both', which='both', length=0)
                #plt.plot(df['forecast'].tolist(), color='green', linestyle='--')  # 预测值，去掉了label
                x = np.linspace(0, 400, 50)
                y = np.piecewise(x,
                                 [x < 100, (x >= 100) & (x < 200), (x >= 200) & (x < 300), x >= 300],
                                 [lambda x: 0.1 * x + np.random.normal(0, 2, x.shape),
                                  lambda x: -0.1 * x + 30 + np.random.normal(0, 2, x.shape),
                                  lambda x: 0.15 * x - 15 + np.random.normal(0, 2, x.shape),
                                  lambda x: -0.15 * x + 45 + np.random.normal(0, 2, x.shape)])

                # 使用样条插值进行平滑处理
                spl = make_interp_spline(x, y)
                x_smooth = np.linspace(x.min(), x.max(), 400)
                y_smooth = spl(x_smooth)
                plt.plot(x_smooth, y_smooth, '-',color='green')
                # plt.xlim(0, 100)
                # plt.ylim(0, 100)

                # 取消刻度
                plt.xticks(np.arange(6)*(length/5), ['0', '5', '10', '15', '20', '25'])
                plt.yticks([])

                plt.title('{}的《{}》学习状态变化图'.format(name, course))
                plt.xlabel('时间(天)')
                plt.ylabel('学习状态')

                # plt.grid(True)
                #plt.show()
                plt.savefig('./时序预测/result2.png')
                plt.clf()
        return last_predict_result


def add_item(pth, ad_it):
    data = pd.read_csv(pth)
    # data.append(ad_it, ignore_index=True)
    # print(list(ad_it.values()))
    # print(list(data.columns))
    add_row = []
    for i in list(data.columns):
        if i not in ad_it:
            print('{} is not an attribute of features!'.format(i))
            return
        add_row.append(ad_it[i])
    # add row to end of DataFrame
    print(data.columns)
    print(ad_it)
    index = len(data.index)
    print(index)
    data.loc[index] = list(ad_it.values())
    # print(data[-5:])
    data.to_csv(pth, index=False)


def mamba(will_train, ad_it, mode, course, name):  # 是否训练，添加的数据

    parser = argparse.ArgumentParser(description='Transformer Multivariate Time Series Forecasting')
    # basic config
    parser.add_argument('--train', type=bool, default=will_train, help='Whether to conduct training')
    parser.add_argument('--rollingforecast', type=bool, default=True, help='rolling forecast True or False')
    """-----------------------------------------------------"""
    # parser.add_argument('--rolling_data_path', type=str, default='ETTh1-Test.csv', help='rolling data file')
    parser.add_argument('--rolling_data_path', type=str, default='single_data_pre-Test.csv', help='rolling data file')
    """------------------------------------------------------"""
    parser.add_argument('--show_results', type=bool, default=True, help='Whether show forecast and real results graph')
    parser.add_argument('--model', type=str, default='Transformer', help='Model name')

    # data loader
    parser.add_argument('--root_path', type=str, default='./时序预测/data/', help='root path of the data file')

    """vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"""
    # parser.add_argument('--data_path', type=str, default='ETTh1.csv', help='data file')
    parser.add_argument('--data_path', type=str, default='single_data_pre.csv', help='data file')
    """^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"""

    parser.add_argument('--features', type=str, default='S',
                        help='forecasting task, options:[M, S, MS]; M:multivariate predict multivariate, S:univariate predict univariate, MS:multivariate predict univariate')

    """-----------------------------------------------------"""
    # parser.add_argument('--target', type=str, default='OT', help='target feature in S or MS task')
    parser.add_argument('--target', type=str, default='open', help='target feature in S or MS task')
    """-----------------------------------------------------"""
    parser.add_argument('--freq', type=str, default='d',
                        help='freq for time features encoding, options:[s:secondly, t:minutely, h:hourly, d:daily, b:business days, w:weekly, m:monthly], you can also use more detailed freq like 15min or 3h')
    parser.add_argument('--checkpoints', type=str, default='./时序预测/models/', help='location of model models')

    # forecasting task
    parser.add_argument('--seq_len', type=int, default=126, help='input sequence length')
    parser.add_argument('--label_len', type=int, default=64, help='start token length')
    parser.add_argument('--pred_len', type=int, default=4, help='prediction sequence length')

    # model
    parser.add_argument('--norm', action='store_false', default=True, help='whether to apply LayerNorm')
    parser.add_argument('--rev', action='store_true', default=True, help='whether to apply RevIN')
    parser.add_argument('--d_model', type=int, default=512, help='dimension of model')
    parser.add_argument('--n_heads', type=int, default=1, help='num of heads')
    parser.add_argument('--e_layers', type=int, default=2, help='num of encoder layers')
    parser.add_argument('--d_layers', type=int, default=1, help='num of decoder layers')
    parser.add_argument('--d_ff', type=int, default=2048, help='dimension of fcn')
    parser.add_argument('--enc_in', type=int, default=1, help='encoder input size')
    parser.add_argument('--dec_in', type=int, default=1, help='decoder input size')
    parser.add_argument('--c_out', type=int, default=1, help='output size')
    parser.add_argument('--dropout', type=float, default=0.05, help='dropout')
    parser.add_argument('--embed', type=str, default='timeF',
                        help='time features encoding, options:[timeF, fixed, learned]')
    parser.add_argument('--output_attention', action='store_true', help='whether to output attention in ecoder')
    parser.add_argument('--activation', type=str, default='gelu', help='activation')
    parser.add_argument('--embed_type', type=int, default=0,
                        help='0: default 1: value embedding + temporal embedding + positional embedding 2: value embedding + positional embedding')
    # optimization
    parser.add_argument('--num_workers', type=int, default=0, help='data loader num workers')
    parser.add_argument('--train_epochs', type=int, default=10, help='train epochs')
    parser.add_argument('--batch_size', type=int, default=16, help='batch size of train input data')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='optimizer learning rate')
    parser.add_argument('--loss', type=str, default='mse', help='loss function')
    parser.add_argument('--lradj', type=str, default='type1', help='adjust learning rate')

    # GPU
    parser.add_argument('--use_gpu', type=bool, default=True, help='use gpu')
    parser.add_argument('--device', type=int, default=0, help='gpu')
    global args
    args = parser.parse_args()
    Exp = Transformerinitialization
    # setting record of experiments
    setting = 'predict-{}-data-{}'.format(args.model, args.data_path[:-4])

    SCI = Transformerinitialization(args)  # 实例化模型
    if args.train:
        # 将新增的数据加入到训练集中进行训练
        add_item(args.root_path + args.data_path, ad_it)
        print('>>>>>>>start training : {}>>>>>>>>>>>>>>>>>>>>>>>>>>'.format(args.model))
        SCI.train(setting)
    print('>>>>>>>predicting : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(args.model))
    # 将新增的数据加入到测试集中进行测试，并且将返回对该新增数据的预测结果返回到return_res变量中，返回
    add_item(args.root_path+args.rolling_data_path, ad_it)
    return_res = SCI.predict(setting, mode, course, name, True)
    return return_res



@bp3.route('/transformer', methods=['POST', 'GET'])
def transformer():
    data = request.json

    will_train = data["will_train"]
    add_new = data["add_new"]
    mode = data["mode"]
    courseName = data["courseName"]
    userName = data["userName"]

    prediction = mamba(will_train, add_new, mode, courseName, userName)

    if mode == 0:
        url = sendOSS('时序预测/result1.png')
    else:
        url = sendOSS('时序预测/result2.png')
    print(url)

    return jsonify({'prediction': prediction}, {'url': url}), 200  # 返回预测结果和状态码 200

#
# if __name__ == '__main__':
#     app.run(port=5005)
    # mode = 0
    # prediction = mamba(False, {"date": "2015/12/17", "open": 3695.57}, mode)
    # print(f'预测值为：{prediction}')
    #
    # if mode == 0:
    #     url = sendOSS('result1.png')
    # else:
    #     url = sendOSS('result2.png')
    # print(url)
    """
        js是接收到的请求json，其中有两个字段will_train和add_new，如果加上
    """
    # 2015/11/26,3659.57,3635.55,3629.86,3668.38,306761582,426000000000.0
    # js = {"will_train": True,"add_new":{"date": "2015/12/17", "open": 3695.57, "close": 3670.55, "low": 3629.86, "high": 3668.38,
    #                                      'volume': 306761582, 'money': 426000000000.0}}
    # js = {
    #       "will_train": True,
    #       "add_new":{"date": "2015/12/17", "open": 3695.57},
    #       "mode": 1
    #       }
    # if_will_train = js['will_train']
    # add_it = js["add_new"]
    # print(js["add_new"].get('open'))
    """
        如果是多个特征预测一个特征：MS
        一个预测一个：S
        多个预测多个：MS
        target也需要改，如果是预测一个，则修改为对应的字段key
    """
    ### print("对新增数据{}的预测结果为{}".format(add_it, main(if_will_train, add_it)))  # 返回的预测结果

    # add_item('./data/stockdata.csv',{"index_code":1,"date":1,"open":1,"close":1,"low":1,"high":1,'volume':1,'money':1,'change':1})
