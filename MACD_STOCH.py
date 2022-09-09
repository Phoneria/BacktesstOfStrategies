import pandas as pd
from binance import Client
from datetime import datetime as dt
import pandas_ta as ta


client =Client(None,None)

def calculate_time(number):
    return dt.fromtimestamp(open_time.iloc[number] / 1000)

titles=["Open Time","Open","High","Low","Close","Volume","Close Time","QAV","NAT","TBBAV","TBQAV","ignore"]

df = pd.read_csv("NEARUSDT1HOUR.csv", names=titles)

open_level = df["Open"]
close_level = df["Close"]
high_level = df["High"]
low_level = df["Low"]
open_time = df["Open Time"]

psar =ta.psar(high=high_level,low=low_level,af=0.01,af0=0.01,max_af=0.2)
stoch = ta.stochrsi(close=close_level)
macd = ta.macd(close_level, 12, 26, 9)
fisher=ta.fisher(high=high_level,low=low_level,length=10)
super_trend = ta.supertrend(high=high_level,close=close_level,low=low_level,length=10,multiplier=3)
atr= ta.atr(high=high_level,close=close_level,low=low_level,length=14)
ema100 = ta.ma("ema",close_level,length = 100)


"""
    Hepsini 5m, 15m ,30m , 1H da deniycez
    1-) MACD ve STOCH RSI aynı sinyalleri verdiğinde atr ve katları kadar deniycez
        a-) MACD yeşile döndüyse
        b-) MACD sinyali zayıflamaya başladıysa
        c-) STOCH RSI değerlerini değiştiricez
    2-) EMA ile aynı yönde ise işleme giricez
    3-) EMA ile kesiştiğinde işlemden çıkıcaz

"""

def atr_macd_stoch_first():
    """
    Stoch Rsi yükseliş veriyorsa , MACD yukarı kestiyse ve Stoch Rsi 50 altında ise LONG
    Stoch Rsi düşüş veriyorsa , MACD aşağı kestiyse ve Stoch Rsi 50 üstünde ise SHORT
    ATR değerine tp/sl



    :return:
    """
    balance = 100
    number_of_operation = 0
    commision = 0.002
    enter_level = 0
    exit_level = 0
    is_in_operation = False
    bullish = False
    bearish = False
    enter_atr=  0
    atr_coefficient = 1
    leverage= 1
    positive =0
    negative = 0
    for i in range(48,len(close_level)):

        if (not is_in_operation) and (stoch.iat[i,0]>stoch.iat[i,1]) and (macd.iat[i,1]>0) and (macd.iat[i-1,1]<=0) and(stoch.iat[i,0]<50) and(close_level[i]> ema100.iloc[i]): # BULISH SIGNAL
            enter_level = close_level[i]
            is_in_operation = True
            number_of_operation+=1
            bullish = True
            enter_atr = enter_level * 0.01
            #print(f"BULLISH : {calculate_time(i)}, ATR : {enter_atr},MACD : {macd.iat[i,1]},STOCH : {stoch.iat[i,0] , stoch.iat[i,1]}")
            #print(f"BALANCE : {balance},  {number_of_operation}")

        elif  (not is_in_operation) and (stoch.iat[i,0]<stoch.iat[i,1]) and (macd.iat[i,1]<0) and (macd.iat[i-1,1]>=0)and(stoch.iat[i,0]>50)and(close_level[i]< ema100.iloc[i]) : # BEARISH SIGNAL
            enter_level = close_level[i]
            is_in_operation = True
            number_of_operation += 1
            bearish = True
            enter_atr = enter_level*0.01
            #print(f"BEARISH : {calculate_time(i)}, ATR : {enter_atr},MACD : {macd.iat[i, 1]},STOCH : {stoch.iat[i, 0], stoch.iat[i, 1]}")
            #print(f"BALANCE : {balance},  {number_of_operation}")

        elif is_in_operation and bullish: # Long işleminde ise
            if high_level[i]>enter_level+enter_atr:
                exit_level= close_level[i]
                balance+= balance*(exit_level-enter_level)/enter_level * leverage
                balance-=balance*commision
                bullish = False
                is_in_operation= False
                #print(f"BULLISH EXITS POSITIVE : {calculate_time(i)}\n")
                positive+=1
            elif low_level[i]< enter_level-enter_atr:
                exit_level = close_level[i]
                balance-=balance*(enter_level-exit_level)/enter_level* leverage
                balance -= balance * commision
                bullish = False
                is_in_operation = False
                #print(f"BULLISH EXITS NEGATIVE : {calculate_time(i)}\n")
                negative+=1
        elif is_in_operation and bearish:
            if high_level[i] > enter_level + enter_atr:
                exit_level = close_level[i]
                balance -= balance * (exit_level - enter_level) / enter_level* leverage
                balance -= balance * commision
                bearish = False
                is_in_operation = False
                #print(f"BEARISH EXITS NEGATIVE : {calculate_time(i)}\n")
                negative+=1
            elif low_level[i] < enter_level - enter_atr:
                balance += balance * (enter_level - exit_level) / enter_level* leverage
                balance -= balance * commision
                bearish = False
                is_in_operation = False
                #print(f"BULLISH EXITS POSITIVE : {calculate_time(i)}\n")
                positive+=1
    print(f"Balance : {balance}\nNumber Of Operations : {number_of_operation}" )
    print(positive,negative)
    print(positive/number_of_operation*100)
atr_macd_stoch_first()


"""
----------------------SONUÇLAR----------------------


STOCH RSI positifken MACD'de kesişim varsa ve STOCH RSI 50'den küçükse atr kadar işleme giriyor
STOCH RSI negatifken MACD'de kesişim varsa ve STOCH RSI 50'den büyükse atr kadar işleme giriyor

Atr Coefficient = 1 :
    1 Ocak 2022den beri
    OPTIMUM KALDIRAC = 11
    Balance : 2413.5994342524045
    Number Of Operations : 54
    
    1 Ocak 2021den beri
    Balance : 0.0003517303876075198
    Number Of Operations : 171
    91 80

Balance : 60.18169922122775 
İşlem Sayısı : 340


"""
