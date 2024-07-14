# -*- coding: UTF-8 -*-

import torch
from torch.nn import Module, LSTM, Linear, Conv1d, ReLU
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import torch.nn as nn


class Net(Module):
    '''
    pytorch预测模型，包括LSTM时序预测层和Linear回归输出层
    可以根据自己的情况增加模型结构
    '''

    def __init__(self, config):
        super(Net, self).__init__()
        # self.conv = nn.Sequential(
        #     nn.Conv1d(in_channels=config.input_size, out_channels=args.out_channels, kernel_size=3),
        #     nn.ReLU(),
        #     nn.MaxPool1d(kernel_size=3, stride=1)
        # )
        # self.relu = nn.ReLU()
        # self.conv1 = Conv1d(in_channels=64, out_channels=config.hidden_size, kernel_size=5, stride=1, padding=2)
        # self.lstm = LSTM(input_size=config.input_size, hidden_size=config.hidden_size,
        #                  num_layers=config.lstm_layers, batch_first=True, dropout=config.dropout_rate)
        # self.lstm_new = LSTM(input_size=32, hidden_size=config.hidden_size,
        #                      num_layers=config.lstm_layers, batch_first=True, dropout=config.dropout_rate)
        # self.linear = Linear(in_features=config.hidden_size, out_features=config.output_size)
        # # self.linear_conv = Linear(in_features=64, out_features=32)
        # self.linear_conv = Linear(in_features=64, out_features=config.output_size)
        # self.linear_input = Linear(in_features=config.input_size, out_features=64)
        input_dim = config.input_size
        hidden_dims = [8, 16, 64, config.output_size]
        layers = []
        for hidden_dim in hidden_dims:
            layers.append(Linear(in_features=input_dim, out_features=hidden_dim))
            layers.append(ReLU())
            input_dim = hidden_dim
        self.linear_agg = nn.Sequential(*layers)

    def forward(self, x, hidden=None):
        # x = x.permute(1, 0)
        # x = self.conv1(x)
        # x = x.permute(1, 0)
        # x = self.relu(x)
        # x = self.linear_conv(x)
        # print(self.linear_agg)
        return self.linear_agg(x)


def train(config, logger, train_and_valid_data):
    if config.do_train_visualized:
        import visdom
        vis = visdom.Visdom(env='model_pytorch')

    train_X, train_Y, valid_X, valid_Y = train_and_valid_data
    train_X, train_Y = torch.from_numpy(train_X).float(), torch.from_numpy(train_Y).float()  # 先转为Tensor
    train_loader = DataLoader(TensorDataset(train_X, train_Y),
                              batch_size=config.batch_size)  # DataLoader可自动生成可训练的batch数据

    valid_X, valid_Y = torch.from_numpy(valid_X).float(), torch.from_numpy(valid_Y).float()
    valid_loader = DataLoader(TensorDataset(valid_X, valid_Y), batch_size=config.batch_size)

    device = torch.device("cuda:0" if config.use_cuda and torch.cuda.is_available() else "cpu")  # CPU训练还是GPU
    model = Net(config).to(device)  # 如果是GPU训练， .to(device) 会把模型/数据复制到GPU显存中
    if config.add_train:  # 如果是增量训练，会先加载原模型参数
        model.load_state_dict(torch.load(config.model_save_path + config.model_name))
    else:
        # 初始化模型参数
        def init_weights(m):
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0)
        model.apply(init_weights)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = torch.nn.MSELoss()  # 这两句是定义优化器和loss

    valid_loss_min = float("inf")
    bad_epoch = 0
    global_step = 0
    for epoch in range(config.epoch):
        logger.info("Epoch {}/{}".format(epoch, config.epoch))
        model.train()  # pytorch中，训练时要转换成训练模式
        train_loss_array = []
        hidden_train = None
        for i, _data in enumerate(train_loader):
            _train_X, _train_Y = _data[0].to(device), _data[1].to(device)
            _train_Y = _train_Y.reshape(-1, 1)
            # print("_train_x", _train_X.shape)
            optimizer.zero_grad()  # 训练前要将梯度信息置 0
            # pred_Y, hidden_train = model(_train_X, hidden_train)    # 这里走的就是前向计算forward函数,lstm
            pred_Y = model(_train_X)  # 这里走的就是前向计算forward函数,cnn
            # print("pred_Y", pred_Y[:5])
            # print("pred_Y.shape:",pred_Y.shape)
            # print("_train_Y.shape:",_train_Y.shape)
            if not config.do_continue_train:
                hidden_train = None  # 如果非连续训练，把hidden重置即可
            else:
                h_0, c_0 = hidden_train
                h_0.detach_(), c_0.detach_()  # 去掉梯度信息
                hidden_train = (h_0, c_0)
            # print("pred_Y",pred_Y)
            # print("_train_Y",_train_Y)
            loss = criterion(pred_Y, _train_Y)  # 计算loss
            loss.backward()  # 将loss反向传播
            optimizer.step()  # 用优化器更新参数
            train_loss_array.append(loss.item())
            global_step += 1
            if config.do_train_visualized and global_step % 100 == 0:  # 每一百步显示一次
                vis.line(X=np.array([global_step]), Y=np.array([loss.item()]), win='Train_Loss',
                         update='append' if global_step > 0 else None, name='Train', opts=dict(showlegend=True))

        # 以下为早停机制，当模型训练连续config.patience个epoch都没有使验证集预测效果提升时，就停止，防止过拟合
        model.eval()  # pytorch中，预测时要转换成预测模式
        valid_loss_array = []
        hidden_valid = None
        for _valid_X, _valid_Y in valid_loader:
            _valid_X, _valid_Y = _valid_X.to(device), _valid_Y.to(device)
            _valid_Y = _valid_Y.reshape(-1, 1)
            # pred_Y, hidden_valid = model(_valid_X, hidden_valid)  # lstm
            pred_Y = model(_valid_X)  # cnn
            if not config.do_continue_train: hidden_valid = None
            loss = criterion(pred_Y, _valid_Y)  # 验证过程只有前向计算，无反向传播过程
            valid_loss_array.append(loss.item())

        train_loss_cur = np.mean(train_loss_array)
        valid_loss_cur = np.mean(valid_loss_array)
        logger.info("The train loss is {:.6f}. ".format(train_loss_cur) +
                    "The valid loss is {:.6f}.".format(valid_loss_cur))
        if config.do_train_visualized:  # 第一个train_loss_cur太大，导致没有显示在visdom中
            vis.line(X=np.array([epoch]), Y=np.array([train_loss_cur]), win='Epoch_Loss',
                     update='append' if epoch > 0 else None, name='Train', opts=dict(showlegend=True))
            vis.line(X=np.array([epoch]), Y=np.array([valid_loss_cur]), win='Epoch_Loss',
                     update='append' if epoch > 0 else None, name='Eval', opts=dict(showlegend=True))

        if valid_loss_cur < valid_loss_min:
            valid_loss_min = valid_loss_cur
            bad_epoch = 0
            torch.save(model.state_dict(), config.model_save_path + config.model_name)  # 模型保存
        else:
            bad_epoch += 1
            if bad_epoch >= config.patience:  # 如果验证集指标连续patience个epoch没有提升，就停掉训练
                logger.info(" The training stops early in epoch {}".format(epoch))
                break


def predict(config, test_X):
    # 获取测试数据
    test_X = torch.from_numpy(test_X).float()
    test_set = TensorDataset(test_X)
    test_loader = DataLoader(test_set, batch_size=1)

    # 加载模型
    device = torch.device("cuda:0" if config.use_cuda and torch.cuda.is_available() else "cpu")
    model = Net(config).to(device)
    model.load_state_dict(torch.load(config.model_save_path + config.model_name))  # 加载模型参数

    # 先定义一个tensor保存预测结果
    result = torch.Tensor().to(device)

    # 预测过程
    model.eval()
    hidden_predict = None
    for _data in test_loader:
        data_X = _data[0].to(device)
        # pred_X, hidden_predict = model(data_X, hidden_predict)  # lstm
        pred_X = model(data_X)  # cnn
        # if not config.do_continue_train: hidden_predict = None    # 实验发现无论是否是连续训练模式，把上一个time_step的hidden传入下一个效果都更好
        cur_pred = torch.squeeze(pred_X, dim=0)
        result = torch.cat((result, cur_pred), dim=0)

    return result.detach().cpu().numpy()  # 先去梯度信息，如果在gpu要转到cpu，最后要返回numpy数据
