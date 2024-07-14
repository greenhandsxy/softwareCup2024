import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from test import ret_rank
from tqdm import tqdm


# dataset = pd.read_csv('./data/Courses.csv', dtype={"grade":float,"nevents":float,"ndays_act":float,"nplay_video":float,"nchapters":float})
# dataset = pd.read_csv('./data/Courses.csv')
#
# # 获取所有列名
# col = list(dataset.columns)
#
# # 分别对每一列调用apply方法，出错的地方填入NaN
# dataset[col] = dataset[col].apply(pd.to_numeric, errors='coerce')
#
# # 删除含有NaN的行
# data = dataset.dropna(axis=0, how='all')
#
# dataset = dataset.fillna(0.0)
# dataset['grade'].fillna(0.0, inplace=True)
# dataset['grade'].astype(float)
# print("total:", len(dataset))
# print("grade==0:", len(dataset[dataset['grade'] == 0]))
# dataset_no_Zero = dataset[dataset['grade'] != 0]
# dataset_no_Zero.to_csv('./data/Courses_no_Zero.csv', index=False)
# 写入preprocess文件，用于模型训练
# dataset.to_csv('./data/Courses_after_preprocess.csv')

def construct_up_dateset():
    dataset = pd.read_csv('./data/Courses_no_Zero.csv')
    dataset['grade'] = 0
    colname = ['nevents', 'ndays_act', 'nplay_video', 'nchapters']
    weight = [0.05, 0.15, 0.55, 0.25]
    rank_df = dataset.rank(ascending=True)
    total_len = len(dataset)
    for index, value in tqdm(dataset.iterrows(),desc='Processing'):
        for j, i in enumerate(colname):
            # print(i, dataset.loc[index, i],
            #       (ret_rank(dataset, rank_df, dataset.loc[index, i], i) / len(dataset)) * weight[j])
            if dataset.loc[index, i] == 0:
                continue
            dataset.loc[index, 'grade'] += (ret_rank(dataset, rank_df, dataset.loc[index, i], i) / total_len) * \
                                           weight[j]
            # print(index, dataset.loc[index, 'grade'])
    # df = dataset['grade']
    # for i in ['nevents', 'ndays_act', 'nplay_video', 'nchapters']:
    #     df = pd.concat([df, dataset[i]], axis=1)
    # df.loc[df['grade'] > 1, 'grade'] = 1.0
    # print(df.head(50))
    dataset.loc[dataset['grade'] > 1, 'grade'] = 1.0
    return dataset

construct_up_dateset().to_csv('./data/Courses_reconstruct.csv', index=False)
# dataset = pd.read_csv('./data/Courses_no_Zero.csv')
# dataset['grade'] = 0
# # dataset['grade'] = dataset['nevents'] / max(dataset['nevent']) * 0.25
# dataset['grade'] = 0
# colname = ['nevents', 'ndays_act', 'nplay_video', 'nchapters']
# weight = [0.05, 0.15, 0.55, 0.25]
# rank_df = dataset.rank(ascending=True)
# for index, value in dataset.iterrows():
#     for j, i in enumerate(colname):
#         print(i, dataset.loc[index, i],
#               (ret_rank(dataset, rank_df, dataset.loc[index, i], i) / len(dataset)) * weight[j])
#         if dataset.loc[index, i] == 0:
#             continue
#         dataset.loc[index, 'grade'] += (ret_rank(dataset, rank_df, dataset.loc[index, i], i) / len(dataset)) * weight[j]
#         print(index, dataset.loc[index, 'grade'])
# df = dataset['grade']
# for i in ['nevents', 'ndays_act', 'nplay_video', 'nchapters']:
#     df = pd.concat([df, dataset[i]], axis=1)
# df.loc[df['grade'] > 1, 'grade'] = 1.0
# print(df)
