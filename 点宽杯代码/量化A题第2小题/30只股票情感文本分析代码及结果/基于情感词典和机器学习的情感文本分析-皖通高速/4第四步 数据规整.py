import pandas as pd
import datetime
import warnings
warnings.filterwarnings("ignore")

# 读取分好的good_result和bad_result
good_result = pd.read_csv(r'情感分析中间数据集/good_result.csv', encoding='utf-8-sig')
bad_result = pd.read_csv(r'情感分析中间数据集/bad_result.csv', encoding='utf-8-sig')
final_result = pd.concat([good_result, bad_result]).sort_values(by='no').dropna()

times = final_result['time'].values.tolist()

new_time_cols = [datetime.datetime.strptime(time, "%Y/%m/%d").date() for time in times]
final_result['time'] = new_time_cols
final_result.sort_values(by='time')
final_result_grouped = final_result.groupby('time')

time = [a for a in set([a for a in final_result['time']])]
all_score = []
all_num = []
weighted_mean_score = []
positive_num = []
positive_score = []
negative_num = []
negative_score = []

for a, b in final_result_grouped:
    all_score.append(sum(b['label']))
    all_num.append(len(b))
    positive_num_value = 0
    positive_score_value = 0
    negative_num_value = 0
    negative_score_value = 0
    for i in b['label']:
        if i == 1:
            positive_num_value += 1
            positive_score_value += i

        if i == -1:
            negative_num_value += 1
            negative_score_value += i
    try:
        numerator = 0
        for y in range(len(b['read_volume'])):
            each_numerator = b['label'].iloc[y]*b['read_volume'].iloc[y]
            numerator+=each_numerator
        weighted_mean_score.append(numerator/sum(b['read_volume']))
    except:
        weighted_mean_score.append(0)


    positive_num.append(positive_num_value)
    positive_score.append(positive_score_value)
    negative_num.append(negative_num_value)
    negative_score.append(negative_score_value)


time = pd.DataFrame({'time': time}).sort_values(by='time').reset_index()
del time['index']

all_num = pd.DataFrame({'all_num_皖通高速': all_num})
all_dic_score = pd.DataFrame({'all_dic_score': all_score})
weighted_mean_sentiment = pd.DataFrame({'皖通高速舆情因子值':  weighted_mean_score})
positive_num = pd.DataFrame({'positive_num': positive_num})
positive_sentiment = pd.DataFrame({'positive_sentiment': positive_score})
negative_num = pd.DataFrame({'negative_num': negative_num})
negative_sentiment = pd.DataFrame({'negative_sentiment': negative_score})
new = pd.concat([time, all_num, all_dic_score,  weighted_mean_sentiment, positive_num, positive_sentiment, negative_num, negative_sentiment],
                axis=1)

new['all_dic_score'] = new['all_dic_score'].apply(lambda x: format(x, '.2f'))
new['皖通高速舆情因子值'] = new['皖通高速舆情因子值'].apply(lambda x: format(x, '.2f'))
new['positive_sentiment'] = new['positive_sentiment'].apply(lambda x: format(x, '.2f'))
new['negative_sentiment'] = new['negative_sentiment'].apply(lambda x: format(x, '.2f'))



print(new)
new.to_csv('皖通高速舆情因子数据(每日).csv', encoding='utf-8-sig', index=False)
final_result.to_csv('皖通高速舆情因子数据(每条).csv', encoding='utf-8-sig', index=False)
