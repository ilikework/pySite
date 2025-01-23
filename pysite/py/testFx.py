import numpy as np
import pandas as pd
import yfinance as yf
import talib
import mplfinance as mpf
import matplotlib.animation as animation

def test_01():
    while True:
        data = yf.download(tickers  = 'USDJPY=X',    # 通貨ペア
                           period   = '1d',         # データ取得期間
                           interval = '1m',          # データ表示間隔
                          )

        fig = mpf.figure(style='charles',figsize=(7,8))
        ax1 = fig.add_subplot(1,1,1)
        
        def animate(ival):
            #print(data)

            # 引数情報
            fast_period   = 10    # 短期指数移動平均線(EMA)の期間
            slow_period   = 25    # 長期指数移動平均線(EMA)の期間
            signal_period = 8     # シグナル (MACDの指数平滑移動平均線)の期間

            macd, macd_signal, macd_hist = talib.MACD(data['Close'], # データ取得元
                                                      fast_period,   # 短期EMAの期間
                                                      slow_period,   # 長期EMAの期間
                                                      signal_period) # シグナルの期間

            # データ追加
            data['macd'] = macd
            data['macd_signal'] = macd_signal


            # KDJ 值对应的函数是 STOCH
            data['slowk'], data['slowd'] = talib.STOCH(
                                    data['High'].values,
                                    data['Low'].values,
                                    data['Close'].values,
                                    fastk_period=9,
                                    slowk_period=3,
                                    slowk_matype=0,
                                    slowd_period=3,
                                    slowd_matype=0)
            # 求出J值，J = (3*K)-(2*D)
            data['slowj'] = list(map(lambda x,y: 3*x-2*y, data['slowk'], data['slowd']))

            RSI5 = talib.RSI(data['Close'],   # 外為データ
                            5)              # RSを計算するための期間
            RSI10 = talib.RSI(data['Close'],   # 外為データ
                            10)              # RSを計算するための期間
            RSI20 = talib.RSI(data['Close'],   # 外為データ
                            20)              # RSを計算するための期間
                            

            # データ分析範囲（直近6ヶ月分を指定）
            period = 5 * 24
            data   = data.tail(period)

            # グラフ可視化
            graph2  = [
                     mpf.make_addplot(data['macd'],        panel=2, color='red'),
                     mpf.make_addplot(data['macd_signal'], panel=2, color='blue'), 
                     ]
            graph3  = [
                     mpf.make_addplot(data['slowk'], panel=2, color='red'),
                     mpf.make_addplot(data['slowd'], panel=2, color='blue'), 
                     mpf.make_addplot(data['slowj'], panel=2, color='green'), 
                     ]
            graph  = [
                    mpf.make_addplot(RSI5, panel=1, ylabel='RSI', color='red'),
                    mpf.make_addplot(RSI10,panel=1, color='yellow'),
                    mpf.make_addplot(RSI20,panel=1, color='blue'),
                     mpf.make_addplot(data['slowk'],ylabel='KDJ', panel=2, color='red'),
                     mpf.make_addplot(data['slowd'], panel=2, color='blue'), 
                     mpf.make_addplot(data['slowj'], panel=2, color='green'),          ]

            mc = mpf.make_marketcolors(up='r',
                                       down='g',
                                       edge="black",  # 蜡烛图箱体的颜色
                                       #volume="blue",  # 成交量柱子的颜色
                                       wick="black")  # 蜡烛图影线的颜色
            s  = mpf.make_mpf_style(marketcolors=mc)

            mpf.plot(data, # データ 
                     type='candle',     # グラフの種類（'candle', 'line'等が指定可能）
                     #volume=True,       # 出来高の表示有無
                     mav=(5,15),        # 移動平均線(短期移動平均線の日数、長期移動平均線の日数)
                     style=s,     # グラフスタイル
                     addplot=graph,     # 連結するグラフ情報
                     figratio=(12,9),   # グラフ縦横の比率
                    )

        ani = animation.FuncAnimation(fig, animate, interval=5000)
        mpf.show()
        sleep(60)
        
def test_00():
    data = yf.download(tickers  = 'USDJPY=X',    # 通貨ペア
                       period   = '1d',         # データ取得期間
                       interval = '1m',          # データ表示間隔
                      )

    #print(data)

    # 引数情報
    fast_period   = 10    # 短期指数移動平均線(EMA)の期間
    slow_period   = 25    # 長期指数移動平均線(EMA)の期間
    signal_period = 8     # シグナル (MACDの指数平滑移動平均線)の期間

    macd, macd_signal, macd_hist = talib.MACD(data['Close'], # データ取得元
                                              fast_period,   # 短期EMAの期間
                                              slow_period,   # 長期EMAの期間
                                              signal_period) # シグナルの期間

    # データ追加
    data['macd'] = macd
    data['macd_signal'] = macd_signal


    # KDJ 值对应的函数是 STOCH
    data['slowk'], data['slowd'] = talib.STOCH(
                            data['High'].values,
                            data['Low'].values,
                            data['Close'].values,
                            fastk_period=9,
                            slowk_period=3,
                            slowk_matype=0,
                            slowd_period=3,
                            slowd_matype=0)
    # 求出J值，J = (3*K)-(2*D)
    data['slowj'] = list(map(lambda x,y: 3*x-2*y, data['slowk'], data['slowd']))

    RSI5 = talib.RSI(data['Close'],   # 外為データ
                    5)              # RSを計算するための期間
    RSI10 = talib.RSI(data['Close'],   # 外為データ
                    10)              # RSを計算するための期間
    RSI20 = talib.RSI(data['Close'],   # 外為データ
                    20)              # RSを計算するための期間
                    

    # データ分析範囲（直近6ヶ月分を指定）
    period = 1 * 24* 60
    data   = data.tail(period)

    # グラフ可視化
    graph2  = [
             mpf.make_addplot(data['macd'],        panel=2, color='red'),
             mpf.make_addplot(data['macd_signal'], panel=2, color='blue'), 
             ]
    graph  = [
            mpf.make_addplot(RSI5, panel=1, ylabel='RSI', color='red'),
            mpf.make_addplot(RSI10,panel=1, color='yellow'),
            mpf.make_addplot(RSI20,panel=1, color='blue'),
             mpf.make_addplot(data['slowk'],ylabel='KDJ', panel=2, color='red'),
             mpf.make_addplot(data['slowd'], panel=2, color='blue'), 
             mpf.make_addplot(data['slowj'], panel=2, color='green'),          
             ]

    mc = mpf.make_marketcolors(up='r',
                               down='g',
                               edge="black",  # 蜡烛图箱体的颜色
                               #volume="blue",  # 成交量柱子的颜色
                               wick="black")  # 蜡烛图影线的颜色
    s  = mpf.make_mpf_style(marketcolors=mc)

    mpf.plot(data, # データ 
             type='candle',     # グラフの種類（'candle', 'line'等が指定可能）
             #volume=True,       # 出来高の表示有無
             #mav=(5,15),        # 移動平均線(短期移動平均線の日数、長期移動平均線の日数)
             style=s,     # グラフスタイル
             addplot=graph,     # 連結するグラフ情報
             figratio=(12,9),   # グラフ縦横の比率
            )

test_00()