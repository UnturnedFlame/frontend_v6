import pandas as pd

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

"""
支持向量机(SVM)模型训练
"""

train_data = pd.read_csv('./vibration_features_with_labels.csv')
choose_features = [ '最大值','最小值','峰峰值','六阶累积量', '四阶累积量', '标准差', '方差', '均方根', '整流平均值', '方根幅值', '中位数', '频率方差', '频率标准差', '均方频率', '均方根频率', '裕度因子']

def train_SVC():
    scaler = StandardScaler()
    train_data[choose_features] = scaler.fit_transform(train_data[choose_features])
    
    # 加载标准化器
    joblib.dump(scaler, './your/path/scaler_2.pkl')

    X = train_data[choose_features]
    y = train_data['label']
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    SVC_model = SVC(kernel='rbf',  # 使用径向基函数核（rbf）以应对非线性问题
                    C=1,  # 正则化参数，值越大越容易过拟合
                    gamma='scale',  # 核函数的系数
                    random_state=42
                    )

    SVC_model.fit(X_train, y_train)

    svc_predictions = SVC_model.predict(X_val)
    y_hat = y_val.values
    num = np.sum((y_hat == 1) & (y_hat == svc_predictions))
    print(f'fault error {num / np.sum(y_hat == 1)}')
    accuracy = accuracy_score(y_val, svc_predictions)
    print("SVC Accuracy:", accuracy)

    joblib.dump(SVC_model, f'./your/path/models/svm/svm_{accuracy}.pkl')

if __name__ == '__main__':
   # 训练
    train_SVC()