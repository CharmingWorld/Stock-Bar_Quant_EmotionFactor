import time
import csv
import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier

start_time = time.time()
# 读取字典法总体文件（防止features不对应！！！！）
with open('情感分析中间数据集/label_dict_result.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    labels = []
    reviews = []
    for row in reader:
        labels.append(row['label'])  # 程序设计竞赛专题挑战教程-好评 -程序设计竞赛专题挑战教程-差评 3-中性
        reviews.append(row['review'])

# 数据预处理
# 将文本中的词语转换为词频矩阵
vectorizer = CountVectorizer(min_df=5)
# 统计每个词语的tf-idf权值
transformer = TfidfTransformer()
# 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
tfidf = transformer.fit_transform(vectorizer.fit_transform(reviews))
# 获取词袋模型中的所有词语
word = vectorizer.get_feature_names()
print("单词数量:", len(word))
X = coo_matrix(tfidf, dtype=np.float32).toarray()  # 稀疏矩阵

# 读取分好的good_result和bad_result
good_result = pd.read_csv('情感分析中间数据集/good_result.csv', encoding='utf-8-sig')
bad_result = pd.read_csv('情感分析中间数据集/bad_result.csv', encoding='utf-8-sig')

# 得出训练集和测试集
X_train = X[good_result['no'] - 1]
y_train = good_result['label']
X_test = X[bad_result['no'] - 1]
y_test = bad_result['label']
print('------训练集、测试集划分完毕')

# 随机森林分类方法模型
print('------正在进行机器学习模型训练及预测')
# n_estimators：森林中树的数量
clf = RandomForestClassifier()  # 默认100棵
clf.fit(X_train, y_train)
precision = clf.score(X_test, y_test)
print('模型的准确度:{}'.format(precision))
print("\n")
pre = clf.predict(X_test)
print(classification_report(y_test, pre))
classification_report(y_test, pre)

# 将预测的label填入bad_result中
bad_result['label'] = pre
bad_result.to_csv('情感分析中间数据集/bad_result.csv', encoding='utf-8-sig', index=False)

print('------机器学习模型训练及预测完毕')
print("\n")
end_time = time.time()
print('本程序运行时间 {:.2f} s.'.format(end_time - start_time))
