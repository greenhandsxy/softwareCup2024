import pandas as pd

data = pd.read_csv("./data/stockdata-Test.csv")
data = data.drop(data.columns[0], axis=1)
for i in range(6):
    data = data.drop(data.columns[-1], axis=1)
print(data.head(5))
data.to_csv("./data/single_data_pre-Test.csv", index=False)
