import torch
import torch.nn as nn
import torchaudio
from torch.utils.data import DataLoader, TensorDataset
import numpy as np


"""
SIM Model故障诊断模型训练
"""

class SEBottleneck(nn.Module):
    expansion = 1

    def __init__(self, inplanes, planes, kernel=3,padding=1):
        super(SEBottleneck, self).__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=kernel, stride=1,
                               padding=padding, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, planes * 1, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(planes * 1)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)
        out = self.relu(out)

        return out


class SimModelSingle(nn.Module):
    def __init__(self, num_features):
        super().__init__()
        n_mels = 40

        self.instancenorm = nn.InstanceNorm1d(n_mels)
        self.torchfb = torchaudio.transforms.MelSpectrogram(sample_rate=50000, n_fft=512, win_length=400,
                                                            hop_length=200, window_fn=torch.hamming_window,
                                                            n_mels=n_mels)

        self.conv = nn.Conv2d(in_channels=num_features, out_channels=16, kernel_size=7, stride=1, padding=3, bias=False)
        self.bn = nn.BatchNorm2d(16)
        self.hidden1 = SEBottleneck(inplanes=16, planes=32, kernel=3)
        self.hidden2 = SEBottleneck(inplanes=32, planes=64, kernel=3)

        self.avg = nn.AdaptiveAvgPool2d((1,1))
        self.log_input = True
        self.fc = nn.Linear(64,2)
        self.relu = nn.ReLU()
        self.sig = nn.Sigmoid()
    def forward(self, x):

        B, _ = x.size()

        with torch.no_grad():
            with torch.cuda.amp.autocast(enabled=False):
                x = self.torchfb(x)+1e-6
                if self.log_input: x = x.log()
                x = self.instancenorm(x).unsqueeze(1).detach()

        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        x = self.hidden1(x)
        x = self.hidden2(x)

        x = self.avg(x)
        x = x.view(B,-1)
        x = self.fc(x)
        x = self.sig(x)
        return x
    
    
# 加载数据
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# 文件路径改为本地路径
dataset = torch.from_numpy(np.load('your/path/of/dataset.npy')).type(torch.FloatTensor).to(device)
labels = torch.from_numpy(np.load('your/path/of/labels.npy')).to(device)

# 构造数据集
train_dataset = TensorDataset(dataset.mT, labels)
train_dataloader = DataLoader(dataset=train_dataset, batch_size=40, shuffle=True)

# 定义模型以及设置超参数
# 设置模型超参数时，num_features为传感器的数量
model = SimModelSingle(num_features=1).to(device)
loss = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
epochs = 100

# 训练模型
for epoch in range(epochs):
    model.train()
    for X, y in train_dataloader:
        X = X.to(device)
        y = y.to(device)
        pre = model(X)
        l = loss(pre, y)

        l.backward()
        optimizer.step()
        optimizer.zero_grad()

    model.eval()
    with torch.no_grad():
        loss_per_epoch = sum(loss(model(xb.to(device)), yb.to(device)) for xb, yb in train_dataloader).item()
        # accuracy_per_epoch = sum(get_accuracy(sim_model(xb.to(device)), yb) for xb, yb in train_dataloader) / \
        #                      all_data.shape[0]

    print(f'epoch:{epoch + 1}, loss:{loss_per_epoch}')
    
    # 保存模型权重
    torch.save(model.state_dict(), f'./model/ulcnn/ulcnn_model_loss_{loss_per_epoch}.pth')