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

ema = ta.ma("ema",close_level,length = 50)


def engulph():
    balance = 100
    enter_value = 0
    stop_level =0
    number_of_operation =0
    short_position = False
    long_position = False
    is_in_operation = False
    commision = 0.002
    leverage= 10
    positive = 0
    negative =0
    max_profit = 0
    max_lost = 0
    max_profit_time = 0
    max_lost_time =0
    for i in range(48,len(close_level)):
        if balance <= 10 :
            print("GAME OVER!!!!!")
            break
        # SHORT ENGULF
        if not (is_in_operation) and (open_level[i]> close_level[i]) and (close_level[i-1]> open_level[i-1])and(
                abs(close_level[i]-open_level[i])> abs(close_level[i]-low_level[i])) and(ema.iloc[i]>close_level[i]) and (
                close_level[i]< open_level[i-1]) :
            enter_value = close_level[i]
            stop_level = close_level[i-1]
            number_of_operation+=1
            is_in_operation = True
            short_position =True
            print(f"SHORT OPEN : {calculate_time(i)}")
       # LONG ENGULF
        if not (is_in_operation) and (open_level[i] < close_level[i]) and (close_level[i - 1] <open_level[i - 1]) and (
                abs(close_level[i] - open_level[i]) < abs(close_level[i] - high_level[i])) and (ema.iloc[i]<close_level[i])and(
            close_level[i]> open_level[i-1]
        ):
            enter_value = close_level[i]
            stop_level = close_level[i - 1]
            number_of_operation += 1
            is_in_operation = True
            long_position = True
            print(f"LONG OPEN : {calculate_time(i)}")
        if is_in_operation and short_position:
            if close_level[i]> stop_level:


                balance = balance - balance*(stop_level-enter_value)/stop_level*leverage
                is_in_operation= False
                short_position=False
                number_of_operation+=1
                negative+=1
                balance-= balance*commision


                if max_profit < (stop_level-enter_value)/stop_level*leverage:
                    max_profit = (stop_level-enter_value)/stop_level*leverage
                    max_profit_time =calculate_time(i)


                print(f"SHORT EXITS NEGATIVE , BAlANCE = {balance} , {calculate_time(i)}\n")
            elif close_level[i]> ema.iloc[i]:
                balance = balance + balance * (stop_level - enter_value) / stop_level*leverage
                is_in_operation = False
                short_position = False
                number_of_operation += 1
                positive+=1
                balance-= balance*commision
                if max_lost < (stop_level - enter_value) / stop_level*leverage:
                    max_lost = (stop_level - enter_value) / stop_level*leverage
                    max_lost_time = calculate_time(i)

                print(f"SHORT EXITS POSITIVE , BAlANCE = {balance} , {calculate_time(i)}\n")

        if is_in_operation and long_position:
            if close_level[i]<stop_level:
                balance = balance - balance*(stop_level-enter_value)/stop_level*leverage
                is_in_operation= False
                long_position=False
                number_of_operation+=1
                balance-= balance*commision
                negative+=1
                if max_lost < (stop_level - enter_value) / stop_level * leverage:
                    max_lost = (stop_level - enter_value) / stop_level * leverage
                    max_lost_time = calculate_time(i)

                print(f"LONG EXITS NEGATIVE , BAlANCE = {balance} , {calculate_time(i)}\n")
            elif close_level[i]< ema.iloc[i]:
                balance = balance + balance * (stop_level - enter_value) / stop_level*leverage
                is_in_operation = False
                long_position = False
                number_of_operation += 1
                balance-= balance*commision
                positive+=1
                if max_profit < (stop_level-enter_value)/stop_level*leverage:
                    max_profit = (stop_level-enter_value)/stop_level*leverage
                    max_profit_time = calculate_time(i)

                print(f"LONG EXITS POSITIVE , BAlANCE = {balance} , {calculate_time(i)}\n")
    print(f"Number Of Operation : {number_of_operation}\nBalance : {balance}\nPositive : {positive}\nNegative : {negative}\nRate : {positive/(positive+negative)*100}")
    print(f"Max Lost : {max_lost}")
    print(f"Max Profit : {max_profit}")
    print(f"Max Lost Time: {max_lost_time}")
    print(f"Max Profit Time: {max_profit_time}")



engulph()



"""
1 Hour
Number Of Operation : 875
Balance : 28106.685248952468
Positive : 174
Negative : 263
Rate : 19.885714285714286
Commision = 0.002
Leverage= 6
Date : 1 January 2021 - 30 June 2022

30 Min
Number Of Operation : 579
Balance : 12317.051651619306
Positive : 109
Negative : 180
Rate : 18.825561312607945
Date : 1 January 2021 - 30 June 2022

Number Of Operation : 1783
Balance : 160120333.61657864
Positive : 348
Negative : 543
Rate : 19.5176668536175
Date : 1 January 2021 - 30 June 2022

15 Min
Number Of Operation : 1139
Balance : 157820.24370655307
Positive : 216
Negative : 353
Rate : 18.964003511852503
Date : 1 January 2021 - 30 June 2022

5 Min
Number Of Operation : 3369
Balance : 2084753.1586049784
Positive : 649
Negative : 1035
Rate : 19.263876521222915
Date : 1 January 2021 - 30 June 2022

"""
