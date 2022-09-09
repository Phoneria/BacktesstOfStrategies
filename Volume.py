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
volume = df["Volume"]



def avg_vol(length =  100,volume= volume,index= 0):
    sum = 0
    for i in range(length):
        sum+= volume.iloc[index-i]

    return  sum / length


def trend_atr():
    balance = 100
    enter_value = 0
    stop_level = 0
    short_position = False
    long_position = False
    is_in_operation = False
    commision = 0.00
    leverage = 1
    positive = 0
    negative = 0
    cf =2

    pcf =1
    ncf= 1

    ema50 = ta.ma("ema", close_level, length=50)
    ema20 = ta.ma("ema", close_level, length=20)
    ema200 = ta.ma("ema", close_level, length=200)
    atr = ta.atr(high=high_level, low=low_level, close=close_level, length=14)


    for i in range(100,len(close_level)):
        if is_in_operation :
            if long_position:
                if high_level[i] > enter_value + stop_level* pcf :
                     balance +=balance* (stop_level/enter_value -commision) * leverage

                     positive+=1
                     is_in_operation = False
                     long_position = False
                     print(f"LONG EXITS POSITIVE : {calculate_time(i)}, BALANCE : {balance}")

                elif low_level[i] < enter_value - stop_level *ncf:
                    balance -= balance * (stop_level / enter_value-commision) * leverage

                    negative += 1
                    is_in_operation = False
                    long_position = False

                    print(f"LONG EXITS NEGATIVE : {calculate_time(i)}, BALANCE : {balance}")
            elif short_position :
                if high_level[i] > enter_value + stop_level * ncf:
                    balance -= balance * (stop_level / enter_value-commision) * leverage

                    negative += 1
                    is_in_operation = False
                    short_position = False
                    print(f"SHORT EXITS NEGATIVE : {calculate_time(i)}, BALANCE : {balance}")

                elif low_level[i] < enter_value - stop_level *pcf:
                    balance += balance * (stop_level / enter_value-commision) * leverage

                    positive += 1
                    is_in_operation = False
                    short_position = False
                    print(f"SHORT EXITS POSITIVE : {calculate_time(i)}, BALANCE : {balance}")

        if not is_in_operation and volume.iloc[i] > avg_vol(index=i):
            if  ema20.iloc[i] > ema50.iloc[i]  and close_level[i]> open_level[i]  and close_level[i] > ema20.iloc[i]: # LONG
                is_in_operation = True
                long_position = True
                enter_value = close_level[i]
                stop_level = atr.iloc[i] * cf
                print(f"\nLONG OPEN : {calculate_time(i)}")
            elif ema20.iloc[i] <  ema50.iloc[i]  and open_level[i]>close_level[i]  and close_level[i] < ema20.iloc[i]: # SHORT
                is_in_operation = True
                short_position = True
                enter_value = close_level[i]
                stop_level = atr.iloc[i] * cf
                print(f"\nSHORT OPEN : {calculate_time(i)}")



    print(positive)
    print(negative)
    print(positive/(positive+negative))
    print(balance)
trend_atr()