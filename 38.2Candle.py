import pandas as pd
from binance import Client
from datetime import datetime as dt
import pandas_ta as ta


client =Client(None,None)

def calculate_time(number):
    return dt.fromtimestamp(open_time.iloc[number] / 1000)

titles=["Open Time","Open","High","Low","Close","Volume","Close Time","QAV","NAT","TBBAV","TBQAV","ignore"]

df = pd.read_csv("BTCUSDT1HOUR.csv", names=titles)

open_level = df["Open"]
close_level = df["Close"]
high_level = df["High"]
low_level = df["Low"]
open_time = df["Open Time"]
ema = ta.ma("ema", close_level, length=21)
atr= ta.atr(high=high_level,close=close_level,low=low_level,length=14)





def doji():
    balance = 100
    positive = 0
    negative =0
    bullish_doji = False
    bearish_doji = False
    commision = 0.002
    is_in_operation =False
    leverage= 0
    enter_value =0
    stop_level = 0
    for i in range(48,len(close_level)):
        if not  is_in_operation:
            if  (close_level[i-1] > open_level[i-1])and close_level[i-1] > ema.iloc[i-1] and(close_level[i]<open_level[i])and (open_level[i]-close_level[i])/(high_level[i]-low_level[i])>0.1:  # Yeşil mum
                if (close_level[i-1] - low_level[i-1]) / (high_level[i-1] - low_level[i-1]) < 0.383:
                    enter_value = close_level[i]
                    stop_level = atr.iloc[i]
                    bullish_doji = True
                    is_in_operation = True
                    print(f"\nYEŞİL DOJIİ : {calculate_time(i)}")
            elif (open_level[i-1] > close_level[i-1]) and close_level[i-1]< ema.iloc[i-1]   and(close_level[i]>open_level[i])and (close_level[i]-open_level[i])/(high_level[i]-low_level[i])>0.1:  # Kırmızı mum
                if (open_level[i-1] - low_level[i-1]) / (high_level[i-1] - low_level[i-1]) < 0.383:
                    enter_value = close_level[i]
                    stop_level = atr.iloc[i]
                    bearish_doji = True
                    is_in_operation = True
                    print(f"\nKIRMIZI DOJİ : {calculate_time(i)}")
        else:

            if bullish_doji :
                if low_level[i]< enter_value-stop_level :
                    balance -= balance * stop_level/ enter_value * leverage
                    is_in_operation = False
                    long_position = False
                    balance -= balance * commision
                    negative +=1
                    print(f"BULLISH EXITS NEGATIVE : {calculate_time(i)} , {balance}")

                elif high_level[i] > enter_value + stop_level:
                    balance += balance * stop_level / enter_value * leverage
                    is_in_operation = False
                    long_position = False
                    balance -= balance * commision
                    positive +=1
                    print(f"BULLISH EXITS POSITIVE : {calculate_time(i)} , {balance}")
            else :
                if low_level[i] < enter_value - stop_level:
                    balance += balance * stop_level / enter_value * leverage
                    is_in_operation = False
                    long_position = False
                    balance -= balance * commision
                    positive += 1
                    print(f"BULLISH EXITS POSITIVE : {calculate_time(i)} , {balance}")
                elif high_level[i] > enter_value + stop_level:
                    balance -= balance * stop_level / enter_value * leverage
                    is_in_operation = False
                    long_position = False
                    balance -= balance * commision
                    negative += 1
                    print(f"BULLISH EXITS NEGATIVE : {calculate_time(i)} , {balance}")

    print(negative,positive)








doji()



