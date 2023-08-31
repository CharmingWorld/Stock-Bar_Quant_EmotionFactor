import atrader as at
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import statsmodels.api as sm
from scipy import stats

# 读取因子数据
factor = pd.read_excel(r'..\量化A题第2小题\30支股票舆情因子数据(月度).xlsx')
factor = factor.set_index('code')
# factor = factor.rename(index = str.lower)
factor.sort_values(by='code', inplace=True, ascending=True)

# 获取2021.程序设计竞赛专题挑战教程-2022.3行情数据
data_f = at.get_kdata(
    target_list=['sse.601390', 'szse.300628', 'szse.300759', 'szse.002008', 'sse.600018', 'szse.002736', 'szse.300751',
                 'sse.601808', 'szse.002414', 'sse.600309', 'sse.601229',
                 'szse.300413', 'szse.300760', 'szse.000301', 'sse.601799', 'szse.002001', 'sse.603486', 'szse.300661',
                 'szse.002821', 'sse.600152', 'szse.002181', 'sse.601858',
                 'szse.002568', 'szse.002116', 'sse.600132', 'sse.600048', 'szse.002271', 'szse.002728', 'sse.601117',
                 'sse.600012'], frequency='month', fre_num=1,
    begin_date='2021-01-01', end_date='2022-03-31', fq=1, fill_up=False, df=True, sort_by_date=False)
close_f = data_f.pivot_table(values='close', index='code', columns='time')

# 获取2022.4-2022.6行情数据
data_b = at.get_kdata(
    target_list=['sse.601390', 'szse.300628', 'szse.300759', 'szse.002008', 'sse.600018', 'szse.002736', 'szse.300751',
                 'sse.601808', 'szse.002414', 'sse.600309', 'sse.601229',
                 'szse.300413', 'szse.300760', 'szse.000301', 'sse.601799', 'szse.002001', 'sse.603486', 'szse.300661',
                 'szse.002821', 'sse.600152', 'szse.002181', 'sse.601858',
                 'szse.002568', 'szse.002116', 'sse.600132', 'sse.600048', 'szse.002271', 'szse.002728', 'sse.601117',
                 'sse.600012'], frequency='month', fre_num=1,
    begin_date='2022-04-01', end_date='2022-06-30', fq=1, fill_up=False, df=True, sort_by_date=False)
close_b = data_b.pivot_table(values='close', index='code', columns='time')

# 合并两段数据
close = pd.concat([close_f, close_b], axis=1, ignore_index=False)


def extreme_MAD(dt, n=5.2):
    median = dt.quantile(0.5)
    new_median = (abs((dt - median)).quantile(0.5))
    dt_up = median + n * new_median
    dt_down = median - n * new_median
    return dt.clip(dt_down, dt_up, axis=1)


# 核密度分布画图
fig = plt.figure(figsize=(14, 8))
factor.iloc[:, 0].plot(kind='kde', label='sentiment')
extreme_MAD(factor, n=5.2).iloc[:, 0].plot(kind='kde', label='MAD')
plt.legend()
plt.show()

# 去极值和标准化
# factor_S = standardize_r(extreme_3sigma(factor))
factor_S = extreme_MAD(factor, n=5.2).fillna(0)

# 中性化
# 申万一级行业
shenwan_industry = {
    'SWNLMY1': 'sse.801010',
    'SWCJ1': 'sse.801020',
    'SWHG1': 'sse.801030',
    'SWGT1': 'sse.801040',
    'SWYSJS1': 'sse.801050',
    'SWDZ1': 'sse.801080',
    'SWJYDQ1': 'sse.801110',
    'SWSPYL1': 'sse.801120',
    'SWFZFZ1': 'sse.801130',
    'SWQGZZ1': 'sse.801140',
    'SWYYSW1': 'sse.801150',
    'SWGYSY1': 'sse.801160',
    'SWJTYS1': 'sse.801170',
    'SWFDC1': 'sse.801180',
    'SWSYMY1': 'sse.801200',
    'SWXXFW1': 'sse.801210',
    'SWZH1': 'sse.801230',
    'SWJZCL1': 'sse.801710',
    'SWJZZS1': 'sse.801720',
    'SWDQSB1': 'sse.801730',
    'SWGFJG1': 'sse.801740',
    'SWJSJ1': 'sse.801750',
    'SWCM1': 'sse.801760',
    'SWTX1': 'sse.801770',
    'SWYH1': 'sse.801780',
    'SWFYJR1': 'sse.801790',
    'SWQC1': 'sse.801880',
    'SWJXSB1': 'sse.801890',
}


def industry_exposure(target_idx):
    # 构建DataFrame，存储行业哑变量
    df = pd.DataFrame(index=[x.lower() for x in target_idx], columns=shenwan_industry.keys())
    for m in df.columns:
        # 行标签集合和某个行业成分股集合的交集
        temp = list(set(df.index).intersection(set(at.get_code_list(m).code.tolist())))
        df.loc[temp, m] = 1
    return df.fillna(0)


ind = industry_exposure(factor.index.tolist())


# 需要传入因子值和总市值
def neutralization(factor, mkv, industry=True):
    Y = factor.fillna(0)
    # Y.rename(index = str.lower,inplace=True)
    df = pd.DataFrame(index=Y.index, columns=Y.columns)  # 构建输出矩阵
    for i in range(Y.shape[1]):  # 遍历每一个因子数据
        if (type(mkv) == pd.DataFrame) | (type(mkv) == pd.Series):
            # mkv.rename(index = str.lower,inplace=True)
            lnmkv = mkv.iloc[:, 0].apply(lambda x: math.log(x))  # 市值对数化
            lnmkv = lnmkv.fillna(0)
            if industry:  # 行业、市值
                dummy_industry = industry_exposure(Y.index.tolist())
                X = pd.concat([dummy_industry, lnmkv], axis=1, sort=False)  # 市值与行业合并
            else:
                X = lnmkv
        elif industry:
            dummy_industry = industry_exposure(Y.index.tolist())
            X = dummy_industry
        result = sm.OLS(Y.iloc[:, i].astype(float), X.astype(float)).fit()  # 线性回归
        df.iloc[:, i] = result.resid.tolist()  # 每个因子数据存储到df中
    return df


# 仅行业中性化
factor_ID = neutralization(factor_S, 0)


# 单因子测试——回归法
def factortest_regression(factor, stock):
    factor_return = list()  # 构建列表，用来放因子收益率
    tvalue = list()  # 构建列表，用来放t值
    stock_return = -stock.diff(-1, axis=1).div(stock)  # 利用收盘价计算股票的月收益率
    #   factor = factor.fillna(0)
    stock_return = stock_return.fillna(0)
    # 每月回归
    for i in range(factor.shape[1] - 1):  # 每个月的截面数据做回归
        result = sm.OLS(stock_return.iloc[:, i], factor.iloc[:, i])  # 线性回归
        results = result.fit()
        factor_return.append(list(results.params))  # 获取回归后的因子收益率
        tvalue.append(list(results.tvalues))  # 获取回归后的t值
    return np.c_[np.array(factor_return), np.array(tvalue)]  # 返回因子收益率和t值的数据


# 回归分析，获得因子收益率和t值
fr = factortest_regression(factor_ID, close)
df = pd.DataFrame(data=fr, index=factor_ID.columns[0:-1], columns=['factor_return', 'tvalue'])

# 因子评价
# t值序列绝对值平均值
t_ma = df['tvalue'].abs().mean()
print('t值序列绝对值平均值：', t_ma)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# t值序列绝对值大于2的占比：
t_ratio = len(df[(df['tvalue'].abs() > 2)]) / len(df['tvalue'])
print('t值序列绝对值大于2的占比：', t_ratio)

# t值序列均值的绝对值除以t值序列的标准差
t_div = abs(df['tvalue'].mean()) / df['tvalue'].std()
print('t值序列均值的绝对值除以t值序列的标准差：', t_div)

# 因子收益率序列平均值
factor_ma = df['factor_return'].mean()
print('因子收益率序列平均值：', factor_ma)

# 因子收益率积累曲线
print('因子收益率积累曲线:')
fig = plt.figure(figsize=(14, 8))
df['factor_return'].cumsum().plot(kind='line', label='factor_return')
plt.legend()
plt.show()


# 单因子测试-IC值法
def factortest_ICvalue(factor, stock):
    Rank_IC = list()  # 构建列表，用来存放spearman相关系数和P值
    stock_return = -stock.diff(-1, axis=1).div(stock)  # 利用收盘价计算股票月收益率
    # factor = factor.fillna(0)
    stock_return = stock_return.fillna(0)
    for i in range(factor.shape[1] - 1):  # 每个月的截面数据求相关系数
        spearman = stats.spearmanr(stock_return.iloc[:, i], factor.iloc[:, i])
        #        print(spearman)
        Rank_IC.append(list(spearman))  # 获取spearman相关系数和P值
    #        print(np.c_[np.array(Rank_IC)])
    return np.c_[np.array(Rank_IC)]


# 获取IC值
IC = factortest_ICvalue(factor_ID, close)
print(IC)
df = pd.DataFrame(data=IC, index=factor_ID.columns[0:-1],
                  columns=['Rank_IC', 'Rank_pvalue'])

# IC值评价
# a.IC值序列均值大小
ma = df['Rank_IC'].mean()
print("Rank_IC值序列均值：", ma)

# b.IC值序列的标准差
st = df['Rank_IC'].std()
print("Rank_IC值序列的标准差:", st)

# c.IR比率
IR = df['Rank_IC'].mean() / df['Rank_IC'].std()
print("IR比率:", IR)

# IC值序列大于0的占比
RankIC_ratio = len(df[(df['Rank_IC'] > 0)]) / len(df['Rank_IC'])
print('Rank_IC值序列大于0的占比：', RankIC_ratio)

# IC的P值序列小于0.1的占比
Rank_pvalue_ratio = len(df[(df['Rank_pvalue'] < 0.1)]) / len(df['Rank_pvalue'])
print('Rank_IC的P值序列小于0.1的占比：', Rank_pvalue_ratio)

# IC值积累曲线
fig = plt.figure(figsize=(14, 8))
df['Rank_IC'].cumsum().plot(kind='line', label='Rank_IC')
plt.legend()
plt.show()
