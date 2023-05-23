import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score


def data_preprocessing(df):
    df.dropna()
    df.info()
    df = df[df['예상'].apply(len) == 5]
    df = df[df['도착'].astype(str).apply(len) == 5]

    df['연월일'] = df['연월일'].astype(str)
    df['년'] = df['연월일'].str[:4].astype(int)/1000.
    df['월'] = df['연월일'].str[5:7].astype(int)/12.
    df['일'] = df['연월일'].str[8:10].astype(int)/31.

    df['예상'] = df['예상'].astype(str)
    df['예상_1'] = df['예상'].str[:2].astype(int)/24.
    df['예상_2'] = df['예상'].str[3:].astype(int)/60.

    df['도착'] = df['도착'].astype(str)
    df['도착_1'] = df['도착'].str[:2].astype(int)/24.
    df['도착_2'] = df['도착'].str[3:].astype(int)/60.   

    categorical = ['항공사', '편명', '출발지', '현황']
    label_encoder = LabelEncoder()
    for col in categorical:
        df[col] = label_encoder.fit_transform(df[col])

    df = df[['년', '월', '일', '항공사', '편명', '출발지', '예상_1', '예상_2', '도착_1', '도착_2', '현황']]
    return df


data_train = pd.read_csv('./airportal/train_airportal.csv')
data_train = data_preprocessing(data_train)

data_test = pd.read_csv('./airportal/train_airportal.csv')
data_test = data_preprocessing(data_train)
print(data_train.head())

# data_test.info()

# data_train.head()
# data_test.info()




x_train_tmp = data_train.iloc[:, :8]  # 0번부터 7번 열까지를 X로 설정
y_train_tmp = data_train.iloc[:, 8]   # 8번 열을 y로 설정




x_test_tmp = data_test.iloc[:, :8]  # 0번부터 7번 열까지를 X로 설정
y_test_tmp = data_test.iloc[:, 8]   # 8번 열을 y로 설정



model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print("정확도:", accuracy)