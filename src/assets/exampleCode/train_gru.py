import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

"""
使用pytorch框架搭建gru网络进行训练，
模型结构为：
    GRUModel(input_size=7, hidden_size=64, num_layers=4, output_size=1)
损失函数为BCEWithLogitsLoss
优化器为Adam；

注意：需要将数据集和标签的读取路径设置为本地的正确路径    
"""

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# 读取数据集
dataset = torch.from_numpy(np.load('your/path/of/dataset.npy')).type(torch.FloatTensor).to(device)
labels = torch.from_numpy(np.load('your/path/of/labels.npy')).to(device)


# 定义GRU模型  
class GRUModel(nn.Module):  
    def __init__(self, input_size, hidden_size, num_layers, output_size):  
        super(GRUModel, self).__init__()  
        self.hidden_size = hidden_size  
        self.num_layers = num_layers  
        self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)  
        self.fc = nn.Linear(hidden_size, output_size)  # 输出层
  
    def forward(self, x):  

        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)  
        out, _ = self.gru(x, h0)  
        out = out[:, -1, :]   
        out = self.fc(out)  
  
        return out.squeeze(1)
    
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
# 在定义GRU模型时，指定input_size为传感器的数量
gru_model = GRUModel(input_size=7, hidden_size=64, num_layers=4, output_size=1).to(device)
loss = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(gru_model.parameters())
epochs = 20

# 训练模型
for epoch in range(epochs):
    gru_model.train()
    for X, y in train_dataloader:
        # X = X.to(device)
        # y = y.to(device)
        pre = gru_model(X)
        l = loss(pre, y)
        
        l.backward()
        optimizer.step()
        optimizer.zero_grad()
        
    gru_model.eval()
    with torch.no_grad():
        loss_per_epoch = sum(loss(gru_model(xb.to(device)), yb.to(device)) for xb, yb in train_dataloader).item()
        accuracy_per_epoch = sum(get_accuracy(gru_model(xb.to(device)), yb) for xb, yb in train_dataloader) / dataset.shape[0]
        
    print(f'epoch:{epoch + 1}, loss:{loss_per_epoch}, accuracy:{accuracy_per_epoch}')