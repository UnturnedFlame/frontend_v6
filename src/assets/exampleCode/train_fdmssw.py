import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
import random

# 基于多传感器信号级加权融合的故障检测与诊断技术，模型训练

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class FeatureExtractor:
    @staticmethod
    def knowledge_driven_features(signal):
        mean = np.mean(signal, axis=2, keepdims=True)
        variance = np.var(signal, axis=2, keepdims=True)
        max_value = np.max(signal, axis=2, keepdims=True)
        min_value = np.min(signal, axis=2, keepdims=True)
        return np.concatenate([mean, variance, max_value, min_value], axis=2)


class DeepFeatureExtractor(nn.Module):
    def __init__(self, input_channels, feature_dim):
        super(DeepFeatureExtractor, self).__init__()
        self.conv1d = nn.Conv1d(input_channels, feature_dim, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.AdaptiveMaxPool1d(1)

    def forward(self, x):
        x = self.conv1d(x)
        x = self.relu(x)
        x = self.pool(x)
        return x.squeeze(-1)


class Classifier(nn.Module):
    def __init__(self, input_dim):
        super(Classifier, self).__init__()
        self.fc_layers = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 2)  # Binary classification
        )

    def forward(self, x):
        return self.fc_layers(x)


class FaultPredictionModel(nn.Module):
    def __init__(self, num_sensors, input_length, deep_feature_dim):
        super(FaultPredictionModel, self).__init__()
        self.num_sensors = num_sensors
        self.deep_extractor = DeepFeatureExtractor(input_channels=1, feature_dim=deep_feature_dim)
        self.sensor_weights = nn.Parameter(torch.ones(num_sensors))  # Learnable sensor weights
        self.classifier = Classifier(
            input_dim=num_sensors * (deep_feature_dim + 4))  # Deep features + knowledge-driven features

    def forward(self, x):

        x = x.permute(0, 2, 1)
        # Apply learnable weights to each sensor's input
        weights = torch.softmax(self.sensor_weights, dim=0)
        x_weighted = x * weights.view(1, -1, 1)

        # Knowledge-driven features
        batch_size = x.shape[0]
        x_np = x_weighted.detach().cpu().numpy()
        kd_features = FeatureExtractor.knowledge_driven_features(x_np)
        kd_features = torch.tensor(kd_features, dtype=torch.float32, device=device)

        # 1D Deep learning features for each sensor
        deep_features = []
        for i in range(self.num_sensors):
            sensor_input = x_weighted[:, i, :]
            deep_feature = self.deep_extractor(sensor_input.unsqueeze(1))
            deep_features.append(deep_feature)
        deep_features = torch.stack(deep_features, dim=1)

        # Concatenate knowledge-driven and deep features for each sensor
        kd_features = kd_features.view(batch_size, self.num_sensors, -1)
        fused_features = torch.cat((deep_features, kd_features), dim=2)
        fused_features = fused_features.view(batch_size, -1)

        # Classification
        output = self.classifier(fused_features)
        return output


class RandomSequenceDataset(Dataset):
    def __init__(self, file_paths, seq_length=2048):
        """
        Custom Dataset for non-overlapping sequence loading with normalization.

        Args:
            file_paths (dict): Dictionary containing file paths for the datasets.
                Keys should be 'normal', 'initial_wear', 'sharp_wear', 'lose_efficacy'.
            seq_length (int): Length of each sequence to load.
        """
        # Load preprocessed data from files
        self.data = {
            'class_1': torch.tensor(
                np.load(file_paths['normal']), dtype=torch.float32
            ),
            'class_2': torch.tensor(
                np.load(file_paths['wear']), dtype=torch.float32
            )
        }
        self.seq_length = seq_length

        # Verify data dimensions (should be 2D: seq, sensor)
        assert self.data['class_1'].dim() == 2, "class_1 data must be 2D (seq, sensor)"
        assert self.data['class_2'].dim() == 2, "class_2 data must be 2D (seq, sensor)"

        # Normalize the data
        all_data = torch.cat([self.data['class_1'], self.data['class_2']], dim=0)
        self.mean = all_data.mean(dim=0)
        self.std = all_data.std(dim=0)

        self.data['class_1'] = (self.data['class_1'] - self.mean) / self.std
        self.data['class_2'] = (self.data['class_2'] - self.mean) / self.std

        # Initialize non-overlapping indices for each class
        self.indices = {
            'class_1': self._generate_non_overlapping_indices(self.data['class_1']),
            'class_2': self._generate_non_overlapping_indices(self.data['class_2'])
        }

        # Combine and shuffle indices once
        self.global_indices = []
        for class_name, indices in self.indices.items():
            self.global_indices.extend([(class_name, idx) for idx in indices])
        random.shuffle(self.global_indices)

        # Initialize an iterator to iterate over indices
        self.index_iterator = iter(self.global_indices)

    def _generate_non_overlapping_indices(self, data):
        """
        Generate non-overlapping start indices for sequences.

        Args:
            data (torch.Tensor): Tensor containing the dataset.

        Returns:
            list: List of non-overlapping start indices.
        """
        num_sequences = data.shape[0] // self.seq_length
        return [i * self.seq_length for i in range(num_sequences)]

    def __len__(self):
        # Total number of sequences (summed across all classes)
        return len(self.global_indices)

    def __getitem__(self, idx):
        """
        Get a non-overlapping sequence from the dataset.
        """
        try:
            # Get the class and start index for the sequence
            class_name, seq_start = next(self.index_iterator)
        except StopIteration:
            # Reset the iterator when exhausted
            self.index_iterator = iter(self.global_indices)
            raise StopIteration("All indices have been exhausted.")

        # Slice the sequence
        sequence = self.data[class_name][seq_start:seq_start + self.seq_length, :]
        label = 0 if class_name == 'class_1' else 1

        return sequence, label


# 模型训练方法
def train_model(model, dataloader, num_epochs, learning_rate, save_path):
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    best_loss = float('inf')
    history = {'loss': []}

    model.train()
    for epoch in range(num_epochs):
        epoch_loss = 0.0
        for batch_x, batch_y in dataloader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)

            # Forward pass
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)

            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        epoch_loss /= len(dataloader)
        history['loss'].append(epoch_loss)
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}")

        # Save the best model
        if epoch_loss < best_loss:
            best_loss = epoch_loss
            torch.save(model.state_dict(), save_path)
            print(f"Model saved at epoch {epoch+1} with loss {epoch_loss:.4f}")

    return history


def predict(model, signal, mean, std):
    model = model.to(device)
    model.eval()
    with torch.no_grad():
        # Normalize input signal
        signal_normalized = (signal - mean) / std

        # Convert to tensor and add batch dimension
        signal_tensor = torch.tensor(signal_normalized, dtype=torch.float32).unsqueeze(0).to(device)

        # Forward pass
        output = model(signal_tensor)

        # Get predicted class
        _, predicted_class = torch.max(output, dim=1)

    return predicted_class.item()


if __name__ == '__main__':
    # 数据集（正常与故障数据）加载路径，需改为本地路径
    file_paths = {
        'normal': 'your/path/of/mutli_normal.npy',
        'wear': 'your/path/of/mutli_wear.npy'
    }

    # 初始化超参数
    seq_length = 2048
    num_sensors = 7
    deep_feature_dim = 16
    batch_size = 64
    num_epochs = 100
    learning_rate = 0.001
    save_path = 'mutli_sensor_1_fault_model_best.pth'
    testing = True

    # 构造数据集
    dataset = RandomSequenceDataset(file_paths, seq_length=seq_length)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True,drop_last=True)

    # 构造模型训练
    model = FaultPredictionModel(num_sensors=num_sensors, input_length=seq_length, deep_feature_dim=deep_feature_dim)
    train_model(model, dataloader, num_epochs=num_epochs, learning_rate=learning_rate, save_path=save_path)
    
    # 保存均值和标准差，以用于之后的模型推理
    mean = dataset.mean.numpy()
    std = dataset.std.numpy()
    np.savez('./mutli_sensor_means_stds.npz ', mean=mean, std=std)

