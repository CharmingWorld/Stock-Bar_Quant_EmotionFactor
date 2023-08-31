import pandas as pd
print('------开始读取情感分析初步结果')
dict_result = pd.read_csv(r'情感分析中间数据集/字典法情感分析初步结果.csv', encoding='utf-8-sig')
label = []
for i in dict_result['score']:
    if i < 0:
        label.append(-1)
    elif i > 0:
        label.append(1)
    else:
        label.append(0)
dict_result['label'] = label
bad_result = dict_result[dict_result['score'].apply(lambda x: abs(int(x)) < 5)]  # 通过字典法没有较好赋值效果的文本集——测试集
good_result = dict_result[~dict_result.index.isin(bad_result.index)]  # 通过字典法有较好赋值效果的文本集——训练集

bad_result.to_csv('情感分析中间数据集/bad_result.csv', encoding='utf-8-sig', index=False)
good_result.to_csv('情感分析中间数据集/good_result.csv', encoding='utf-8-sig', index=False)
dict_result.to_csv('情感分析中间数据集/label_dict_result.csv', encoding='utf-8-sig', index=False)
print('------修订、区分后的初步结果数据已输出')