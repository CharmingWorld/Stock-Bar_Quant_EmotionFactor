from atrader import *
import numpy as np
import pandas as pd
import datetime as dt


def init(context):
    set_backtest(initial_cash=10000000)  # 设置回测初始信息
    reg_kdata('day', 1)  # 注册K线数据
    days = get_trading_days('SSE', '2021-01-01', '2022-06-30')  # 交易日
    months = np.vectorize(lambda x: x.month)(days)  # 转换为月份数据
    month_begin = days[pd.Series(months) != pd.Series(months).shift(1)]  # 月初的日期
    month_end = days[pd.Series(months) != pd.Series(months).shift(-1)]  # 月末的日期

    context.month_begin = pd.Series(month_begin).dt.strftime('%Y-%m-%d').tolist()  # 月初日期列表
    context.month_end = pd.Series(month_end).dt.strftime('%Y-%m-%d').tolist()  # 月末日期列表
    context.date = 20  # 注册K线数据长度
    context.Tlen = len(context.target_list)  # 标的数量
    context.num = 0


# 策略逻辑运算实现
def on_data(context):
    # 按月调仓
    if dt.datetime.strftime(context.now, '%Y-%m-%d') not in context.month_begin[1:]:  # 调仓频率为月,2月开始调仓，根据上月（1月）因子数据进行调仓
        return
    if dt.datetime.strftime(context.now, '%Y-%m-%d') in context.month_begin[1:] :
        symbols_pool = get_senntiment_data(context.month_end[context.num][0:7])  # 买入上个月的因子排名前5的股票
        context.num += 1

    # 仓位数据查询
    positions = context.account().positions
    # 策略下单交易：
    # 卖不在标的池中的股票
    for target_idx in positions.target_idx.astype(int):
        if target_idx not in symbols_pool:
            if positions['volume_long'].iloc[target_idx] > 0:
                order_target_volume(account_idx=0, target_idx=target_idx, target_volume=0, side=1, order_type=2,
                                    price=0)
    # 买在标的池中的股票
    for target_idx in symbols_pool:
        order_target_value(account_idx=0, target_idx=target_idx, target_value=1e8/25, side=1, order_type=2, price=0)


def get_senntiment_data(date):
    sentiment_data = pd.read_excel(
        r'..\量化A题第2小题\30支股票舆情因子数据(月度).xlsx')
    # 获取上月月末因子值排名前五的股票（从2021年1月开始）
    sentiment_data = sentiment_data.sort_values(by=date, ascending=False)  # 当月按情感因子降序后的股票代码
    stock_portfolio_of_this_month = sentiment_data['code'].head(5)  # 上月情感因子值排名前五的股票（type=list）
    return stock_portfolio_of_this_month.index.tolist()


if __name__ == '__main__':
    begin = '2021-02-01'
    end = '2022-06-30'
    cons_date = dt.datetime.strptime(begin, '%Y-%m-%d') - dt.timedelta(days=1)
    hs300 = get_code_list('hs300', cons_date)
    run_backtest(strategy_name='点宽杯2022_250_基于东方财富股吧文本情感数据的单因子选股策略',
                 file_path='',
                 target_list=['sse.600012', 'sse.600018', 'sse.600048', 'sse.600132', 'sse.600152', 'sse.600309',
                              'sse.601117',
                              'sse.601229', 'sse.601390', 'sse.601799', 'sse.601808', 'sse.601858', 'sse.603486',
                              'szse.000301',
                              'szse.002001', 'szse.002008', 'szse.002116', 'szse.002181', 'szse.002271', 'szse.002414',
                              'szse.002568',
                              'szse.002728', 'szse.002736', 'szse.002821', 'szse.300413', 'szse.300628', 'szse.300661',
                              'szse.300751',
                              'szse.300759', 'szse.300760'],
                 frequency='day',
                 fre_num=1,
                 begin_date=begin,
                 end_date=end,
                 fq=1)

