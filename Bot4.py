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


def bot4():
    balance =100
    short = False
    long = False
    enter_value = 0
    stop = 0

    pos_coef=1
    neg_coef =1

    positive= 0
    negative= 0

    commission = 0.002
    leverage =10

    max_win = 0
    max_lose = 0

    for i in range(5,len(close_level)):
        if balance <= 10:
            print("GAME OVER!!!!")
            break


        if long:
            if (low_level[i] < enter_value - stop):
                negative+=1
                print("LONG EXITS NEGAITVE : ",calculate_time(i) )
                balance -= balance * (stop / enter_value - commission) * leverage
                long = False
            elif high_level[i] >enter_value+ stop   :
                positive+=1
                print("LONG EXITS POSITIVE : ", calculate_time(i))
                balance+= balance*(stop/enter_value-commission)*leverage


                long = False

           
        if short :

            if high_level[i] > enter_value+stop:
                negative += 1
                print("SHORT EXITS NEGATIVE : ", calculate_time(i))
                balance -= balance * (stop / enter_value - commission) * leverage


                short = False
            elif (low_level[i] < enter_value-stop):
                positive += 1
                print("SHORT EXITS POSITIVE : ", calculate_time(i))
                balance += balance * (stop / enter_value - commission) * leverage
                short = False


        if not short and not  long:
            if  (close_level[i] < open_level[i]) and (close_level[i] < open_level[i-1]) and (close_level[i]< close_level[i-2]) \
                and (open_level[i-1]< close_level[i-1])  \
                and (close_level[i-2] < open_level[i-2]) and \
                    (close_level[i-3] > open_level[i-3] ) and (open_level[i-3] < close_level[i-2]) and (open_level[i-3] < open_level[i-1] ):

                # and close_level[i]<open_level[i-3]
                short = True
                print("\nSHORT OPEN : ", calculate_time(i))
                enter_value = close_level[i]
                stop = open_level[i] - close_level[i]
                print( "BALANCE : ", balance)

            if (close_level[i] > open_level[i]) and (close_level[i] > open_level[i-1]) and (close_level[i] > close_level[i-2]) and \
                 (close_level[i-1] < open_level[i-1]) and (close_level[i-2]> open_level[i-2])and \
                 (close_level[i-3]< open_level[i-3]) and (open_level[i-3] > close_level[i-2]) and (open_level[i-3] > close_level[i-3]) :
                long = True
                print("\nLONG OPEN : ",calculate_time(i))
                print( "BALANCE : ", balance)
                enter_value = close_level[i]
                stop =close_level[i]- open_level[i]


    print("\n\n\n\n",balance)
    print(positive)
    print(negative)
    print(positive/(positive+negative))



bot4()
"""
NEARUSDT 30MIN
29859796.254920706
234
86
0.73125
"""