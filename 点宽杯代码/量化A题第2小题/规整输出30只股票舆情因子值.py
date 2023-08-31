import datetime
import numpy as np
import pandas as pd

# 读取股吧评论文本舆情因子值
whhx = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-万华化学/万华化学舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
shyh = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-上海银行/上海银行舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
sgjt = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-上港集团/上港集团舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
dfsh = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-东方盛虹/东方盛虹舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
dfyh = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-东方雨虹/东方雨虹舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
zgzt = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-中国中铁/中国中铁舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
zghx = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-中国化学/中国化学舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
zghc = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-中国海诚/中国海诚舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
zgkc = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-中国科传/中国科传舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
zhyf = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-中海油服/中海油服舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
ylwl = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-亿联网络/亿联网络舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
blfz = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-保利发展/保利发展舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
kly = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-凯莱英/凯莱英舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
gxzq = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-国信证券/国信证券舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
sbgf = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-圣邦股份/圣邦股份舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
dzjg = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-大族激光/大族激光舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
klhc = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-康龙化成/康龙化成舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
xhc = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-新和成/新和成舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
xygf = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-星宇股份/星宇股份舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
tyyy = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-特一药业/特一药业舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
brgf = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-百润股份/百润股份舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
wtgs = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-皖通高速/皖通高速舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
kws = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-科沃斯/科沃斯舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
ycm = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-粤传媒/粤传媒舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
wkjs = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-维科技术/维科技术舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
mgcm = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-芒果超媒/芒果超媒舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
mwgf = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-迈为股份/迈为股份舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
mryl = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-迈瑞医疗/迈瑞医疗舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
cqpj = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-重庆啤酒/重庆啤酒舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])
gdhw = pd.read_csv(
    r'30只股票情感文本分析代码及结果/基于情感词典和机器学习的情感文本分析-高德红外/高德红外舆情因子数据(每日).csv',
    encoding='utf-8-sig', usecols=[0, 1, 3])

# 读取回测区间每日日期
date = pd.read_csv('2021年1月1日-2022年6月30日日期列表.csv', usecols=[0]).values.tolist()
time = []
for x in date:
    for y in x:
        time.append(y)
each_date = pd.DataFrame({'time': time, 'date': [0 for i in range(len(time))]})
data = each_date.merge(whhx, on='time', how='left')
data = data.merge(shyh, on='time', how='left')
data = data.merge(sgjt, on='time', how='left')
data = data.merge(dfsh, on='time', how='left')
data = data.merge(dfyh, on='time', how='left')
data = data.merge(zgzt, on='time', how='left')
data = data.merge(zghx, on='time', how='left')
data = data.merge(zghc, on='time', how='left')
data = data.merge(zgkc, on='time', how='left')
data = data.merge(zhyf, on='time', how='left')
data = data.merge(ylwl, on='time', how='left')
data = data.merge(blfz, on='time', how='left')
data = data.merge(kly, on='time', how='left')
data = data.merge(gxzq, on='time', how='left')
data = data.merge(sbgf, on='time', how='left')
data = data.merge(dzjg, on='time', how='left')
data = data.merge(klhc, on='time', how='left')
data = data.merge(xhc, on='time', how='left')
data = data.merge(xygf, on='time', how='left')
data = data.merge(tyyy, on='time', how='left')
data = data.merge(brgf, on='time', how='left')
data = data.merge(wtgs, on='time', how='left')
data = data.merge(kws, on='time', how='left')
data = data.merge(ycm, on='time', how='left')
data = data.merge(wkjs, on='time', how='left')
data = data.merge(mgcm, on='time', how='left')
data = data.merge(mwgf, on='time', how='left')
data = data.merge(mryl, on='time', how='left')
data = data.merge(cqpj, on='time', how='left')
data = data.merge(gdhw, on='time', how='left')
data.fillna(0, inplace=True)
# 形成月份日期列
for a in range(len(data)):
    data['date'].iloc[a] = data['time'].iloc[a][0:7]
date_dic = {}
date_dic = date_dic.fromkeys(data['date'].tolist()).keys()
# 按月统计舆情值
data = data.groupby('date')
value_whhx = []
value_shyh = []
value_sgjt = []
value_dfsh = []
value_dfyh = []
value_zgzt = []
value_zghx = []
value_zghc = []
value_zgkc = []
value_zhyf = []
value_ylwl = []
value_blfz = []
value_kly = []
value_gxzq = []
value_sbgf = []
value_dzjg = []
value_klhc = []
value_xhc = []
value_xygf = []
value_tyyy = []
value_brgf = []
value_wtgs = []
value_kws = []
value_ycm = []
value_wkjs = []
value_mgcm = []
value_mwgf = []
value_mryl = []
value_cqpj = []
value_gdhw = []


# 获取极值
def very_value(data):
    max = np.max(data)
    min = np.min(data)
    if np.abs(max) > np.abs(min):
        return max
    else:
        return min


# 按月计算月度情感方差波动
for a, b in data:
    value_whhx.append(round(np.var(b['万华化学舆情因子值']), 4))
    value_shyh.append(round(np.var(b['上海银行舆情因子值']), 4))
    value_sgjt.append(round(np.var(b['上港集团舆情因子值']), 4))
    value_dfsh.append(round(np.var(b['东方盛虹舆情因子值']), 4))
    value_dfyh.append(round(np.var(b['东方雨虹舆情因子值']), 4))
    value_zgzt.append(round(np.var(b['中国中铁舆情因子值']), 4))
    value_zghx.append(round(np.var(b['中国化学舆情因子值']), 4))
    value_zghc.append(round(np.var(b['中国海诚舆情因子值']), 4))
    value_zgkc.append(round(np.var(b['中国科传舆情因子值']), 4))
    value_zhyf.append(round(np.var(b['中海油服舆情因子值']), 4))
    value_ylwl.append(round(np.var(b['亿联网络舆情因子值']), 4))
    value_blfz.append(round(np.var(b['保利发展舆情因子值']), 4))
    value_kly.append(round(np.var(b['凯莱英舆情因子值']), 4))
    value_gxzq.append(round(np.var(b['国信证券舆情因子值']), 4))
    value_sbgf.append(round(np.var(b['圣邦股份舆情因子值']), 4))
    value_dzjg.append(round(np.var(b['大族激光舆情因子值']), 4))
    value_klhc.append(round(np.var(b['康龙化成舆情因子值']), 4))
    value_xhc.append(round(np.var(b['新和成舆情因子值']), 4))
    value_xygf.append(round(np.var(b['星宇股份舆情因子值']), 4))
    value_tyyy.append(round(np.var(b['特一药业舆情因子值']), 4))
    value_brgf.append(round(np.var(b['百润股份舆情因子值']), 4))
    value_wtgs.append(round(np.var(b['皖通高速舆情因子值']), 4))
    value_kws.append(round(np.var(b['科沃斯舆情因子值']), 4))
    value_ycm.append(round(np.var(b['粤传媒舆情因子值']), 4))
    value_wkjs.append(round(np.var(b['维科技术舆情因子值']), 4))
    value_mgcm.append(round(np.var(b['芒果超媒舆情因子值']), 4))
    value_mwgf.append(round(np.var(b['迈为股份舆情因子值']), 4))
    value_mryl.append(round(np.var(b['迈瑞医疗舆情因子值']), 4))
    value_cqpj.append(round(np.var(b['重庆啤酒舆情因子值']), 4))
    value_gdhw.append(round(np.var(b['高德红外舆情因子值']), 4))

sentiment_result = pd.DataFrame(
    {'code': list(date_dic), 'sse.600309': value_whhx, 'sse.601229': value_shyh,
     'sse.600018': value_sgjt, 'szse.000301': value_dfsh, 'szse.002271': value_dfyh,
     'sse.601390': value_zgzt, 'sse.601117': value_zghx, 'szse.002116': value_zghc,
     'sse.601858': value_zgkc, 'sse.601808': value_zhyf, 'szse.300628': value_ylwl,
     'sse.600048': value_blfz, 'szse.002821': value_kly, 'szse.002736': value_gxzq,
     'szse.300661': value_sbgf, 'szse.002008': value_dzjg, 'szse.300759': value_klhc,
     'szse.002001': value_xhc, 'sse.601799': value_xygf, 'szse.002728': value_tyyy,
     'szse.002568': value_brgf, 'sse.600012': value_wtgs, 'sse.603486': value_kws,
     'szse.002181': value_ycm, 'sse.600152': value_wkjs, 'szse.300413': value_mgcm,
     'szse.300751': value_mwgf, 'szse.300760': value_mryl, 'sse.600132': value_cqpj,
     'szse.002414': value_gdhw}).replace(0, np.nan).fillna(method='bfill').fillna(method='ffill')
sentiment_result.set_index('code', inplace=True)
sentiment_result = sentiment_result.T
sentiment_result.index.name = 'code'
sentiment_result.to_excel('30支股票舆情因子数据(月度).xlsx', encoding='utf-8-sig')
print('\n30支股票舆情因子数据输出完毕！\n')
