import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

"""
使用pytorch框架搭建lstm网络进行训练，
模型结构为：
    LSTM(input_size=7, hidden_size=64, num_layers=4, output_size=1)
损失函数为BCEWithLogitsLoss
优化器为Adam；

注意：需要将数据集和标签的读取路径设置为本地的正确路径    
"""

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# 读取数据集
dataset = torch.from_numpy(np.load('your/path/of/dataset.npy')).type(torch.FloatTensor).to(device)
labels = torch.from_numpy(np.load('your/path/of/labels.npy')).to(device)


# lstm网络架构
class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_size = output_size
        self.num_directions = 1  # 单向LSTM
        self.lstm = nn.LSTM(self.input_size, self.hidden_size, self.num_layers, batch_first=True)
        self.linear = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, input_seq):
        # batch_size, seq_len = input_seq.shape[0], input_seq.shape[1]
        # h_0 = torch.randn(self.num_directions * self.num_layers, self.batch_size, self.hidden_size).to(device)
        # c_0 = torch.randn(self.num_directions * self.num_layers, self.batch_size, self.hidden_size).to(device)
        # output(batch_size, seq_len, num_directions * hidden_size)
        output, _ = self.lstm(input_seq)  # output(40, 2048, 100)
        pred = self.linear(output)  # (40, 2048, 1)
        pred = pred[:, -1, :]  # (40, 1)
        return pred.squeeze(1)
    
# 评估准确率
def get_accuracy(prediction, truth):
    true_num = 0
    for pre, tru in zip(prediction, truth):
        if torch.abs(pre - tru).item() <= 0.5:
            true_num += 1

    return true_num


# 构造数据集
train_dataset = TensorDataset(dataset, labels)
train_dataloader = DataLoader(dataset=train_dataset, batch_size=40, shuffle=True)


# 模型定义以及超参数设置
# 在定义lstm模型时，指定input_size为传感器的数量
lstm_model = LSTM(input_size=7, hidden_size=64, num_layers=4, output_size=1).to(device)

loss = nn.BCEWithLogitsLoss()
# loss = nn.MSELoss()

optimizer = torch.optim.Adam(lstm_model.parameters())
# optimizer = torch.optim.ASGD(lstm_model.parameters())

epochs = 20

# 训练模型
for epoch in range(epochs):
    lstm_model.train()
    for X, y in train_dataloader:
        pre = lstm_model(X)
        l = loss(pre, y)
        
        l.backward()
        optimizer.step()
        optimizer.zero_grad()
        
    lstm_model.eval()
    with torch.no_grad():
        loss_per_epoch = sum(loss(lstm_model(xb.to(device)), yb.to(device)) for xb, yb in train_dataloader).item()
        accuracy_per_epoch = sum(get_accuracy(lstm_model(xb.to(device)), yb) for xb, yb in train_dataloader) / dataset.shape[0]
        
    print(f'epoch:{epoch + 1}, loss:{loss_per_epoch}, accuracy:{accuracy_per_epoch}')