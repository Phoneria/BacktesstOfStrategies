import pandas as pd
from binance import Client
from datetime import datetime as dt
import pandas_ta as ta
from random import randint

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
atr = ta.atr(high=high_level,close=close_level,low=low_level,length=14)

def random():
    balance = 100
    number_of_operation = 0
    commision = 0.00
    enter_level = 0

    is_in_operation = False
    bullish = False
    bearish = False
    enter_atr  = 0

    leverage = 1
    positive = 0
    negative = 0
    for i in range(48, len(close_level)):
        random_number =randint(0,1)

        if not is_in_operation and  random_number == 0:
            enter_level = close_level[i]
            is_in_operation = True
            number_of_operation += 1
            bullish = True
            enter_atr = atr.iloc[i]

            # print(f"BULLISH : {calculate_time(i)}, ATR : {enter_atr},MACD : {macd.iat[i,1]},STOCH : {stoch.iat[i,0] , stoch.iat[i,1]}")
            # print(f"BALANCE : {balance},  {number_of_operation}")

        elif not is_in_operation and random_number== 1:
            enter_level = close_level[i]
            is_in_operation = True
            number_of_operation += 1
            bearish = True
            enter_atr = atr.iloc[i]
            # print(f"BEARISH : {calculate_time(i)}, ATR : {enter_atr},MACD : {macd.iat[i, 1]},STOCH : {stoch.iat[i, 0], stoch.iat[i, 1]}")
            # print(f"BALANCE : {balance},  {number_of_operation}")

        elif  bullish:  # Long işleminde ise
            if high_level[i] > enter_level + enter_atr*3:  # İşlem olumlu kapandıysa
                exit_level = close_level[i]
                balance += balance * (exit_level - enter_level) / enter_level * leverage
                balance -= balance * commision
                bullish = False
                is_in_operation = False
                # print(f"BULLISH EXITS POSITIVE : {calculate_time(i)}\n")
                positive += 1
            elif low_level[i] < enter_level - enter_atr:  # İşlem olumsuz kapandıysa
                exit_level = close_level[i]
                balance -= balance * (enter_level - exit_level) / enter_level * leverage
                balance -= balance * commision
                bullish = False
                is_in_operation = False
                # print(f"BULLISH EXITS NEGATIVE : {calculate_time(i)}\n")
                negative += 1
        elif  bearish:
            if high_level[i] > enter_level + enter_atr:  # İşlem olumsuz kapandıysa
                exit_level = close_level[i]
                balance -= balance * (exit_level - enter_level) / enter_level * leverage
                balance -= balance * commision
                bearish = False
                is_in_operation = False
                # print(f"BEARISH EXITS NEGATIVE : {calculate_time(i)}\n")
                negative += 1
            elif low_level[i] < enter_level - enter_atr*3:  # İşlem olumlu kapandıysa
                exit_level = close_level[i]
                balance += balance * (enter_level - exit_level) / enter_level * leverage
                balance -= balance * commision
                bearish = False
                is_in_operation = False
                # print(f"BULLISH EXITS POSITIVE : {calculate_time(i)}\n")
                positive += 1
    print(f"Balance : {balance}\nNumber Of Operations : {number_of_operation}")
    print(positive, negative)


random()