import pandas as pd
from binance import Client
from datetime import datetime as dt
import pandas_ta as ta


client =Client(None,None)

def calculate_time(number):
    return dt.fromtimestamp(open_time.iloc[number] / 1000)

titles=["Open Time","Open","High","Low","Close","Volume","Close Time","QAV","NAT","TBBAV","TBQAV","ignore"]

df = pd.read_csv("NEARUSDT30MIN.csv", names=titles)

open_level = df["Open"]
close_level = df["Close"]
high_level = df["High"]
low_level = df["Low"]
open_time = df["Open Time"]




def atr_ema(a,b):
    balance = 100
    enter_value = 0
    atr_level = 0
    short_position = False
    long_position = False
    is_in_operation = False
    commision = 0.002
    leverage = 10
    positive = 0
    negative = 0
    pc = a
    nc = b
    ema = ta.ma("ema", close_level, length=50)
    atr = ta.atr(high=high_level, low=low_level, close=close_level, length=14)

    for i in range(48,len(close_level)):
        if balance<=7:
            break
        if (not is_in_operation ) and (ema.iloc[i-1]>close_level[i-1]) and (ema.iloc[i]<close_level[i]):
            long_position = True
            is_in_operation =True
            atr_level = atr.iloc[i]
            enter_value = close_level[i]
            print(f"\nLONG OPEN : {calculate_time(i)}\nENTER PRICE : {enter_value}")
        elif not is_in_operation  and ema.iloc[i-1] < close_level[i-1] and ema.iloc[i]> close_level[i]:
            short_position = True
            is_in_operation = True
            atr_level = atr.iloc[i]
            enter_value = close_level[i]
            print(f"\nSHORT OPEN : {calculate_time(i)}\nENTER PRICE : {enter_value} ")
        elif long_position:
            if (low_level[i] < enter_value - atr_level * nc):
                negative -= 1
                balance -= balance * atr_level * nc / enter_value * leverage
                is_in_operation = False
                long_position = False
                balance -= balance * commision
                print(f"BAlANCE : {balance}")
                print(f"LONG EXITS NEGATIVE : {calculate_time(i)}\nEXIT PRICE : {enter_value - atr_level * nc}")
            elif (high_level[i]>enter_value + atr_level*pc):
                positive+=1
                balance +=  balance*atr_level*pc/enter_value *leverage
                is_in_operation = False
                long_position = False
                balance-=balance*commision
                print(f"BAlANCE : {balance}")
                print(f"LONG EXITS POSITIVE : {calculate_time(i)}\nEXIT PRICE : {enter_value + atr_level*pc}   ATR : {atr_level*pc}")

        elif short_position :
            if (high_level[i] > enter_value + atr_level * nc):
                negative -= 1
                balance -= balance * atr_level * nc / enter_value * leverage
                is_in_operation = False
                short_position = False
                balance -= balance * commision
                print(f"BAlANCE : {balance}")
                print(f"SHORT EXITS NEGATIVE : {calculate_time(i)}\nEXIT PRICE : {enter_value + atr_level * nc}")

            elif(low_level[i]< enter_value - atr_level*pc):
                positive+=1
                balance += balance * atr_level*pc / enter_value*leverage
                is_in_operation = False
                short_position = False
                balance-=balance*commision
                print(f"BAlANCE : {balance}")
                print(f"SHORT EXITS POSITIVE : {calculate_time(i)}\nEXIT PRICE : {enter_value - atr_level*pc}  ATR : {atr_level*pc}")

    print()
    print(f"Balance : {balance}\nPositive : {positive}\nNegative : {negative}   ")

print(calculate_time(0))



"""
30 min
1
0
25581.72782860863
"""