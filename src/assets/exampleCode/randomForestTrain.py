import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

train_data = pd.read_csv('./your/path/vibration_features_with_labels.csv')

# 数据集中包含的特征
features = [ '最大值','最小值','峰峰值','六阶累积量', '四阶累积量', '标准差', '方差', '均方根', '整流平均值', '方根幅值', '中位数', '频率方差', '频率标准差', '均方频率', '均方根频率', '裕度因子']

# 训练随机森林模型
def train_Rf_model():
    X = train_data[features]
    y = train_data['label']

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    randomForest_model = RandomForestClassifier(n_estimators=40,
                                                max_depth=4,
                                                min_samples_split=10,
                                                min_samples_leaf=3,
                                                criterion='entropy',
                                                random_state=42,
                                                n_jobs=-1
                                                )

    randomForest_model.fit(X_train, y_train)
    # 测试预测
    rf_predictions = randomForest_model.predict(X_val)
    y_hat = y_val.values
    num = np.sum((y_hat == 1) & (y_hat == rf_predictions))
    print(f'fault error {num / np.sum(y_hat == 1)}')
    accuracy = accuracy_score(y_val, rf_predictions)
    print("Random Forest Accuracy:", accuracy)
    joblib.dump(randomForest_model, f'./your/path/models/random_forest/rndomforest_{accuracy}.pkl')

if __name__ == '__main__':
   # 训练
    train_Rf_model()
