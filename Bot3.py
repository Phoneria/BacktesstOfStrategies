import pandas as pd
from binance import Client
from datetime import datetime as dt
import pandas_ta as ta


client =Client(None,None)

def calculate_time(number):
    return dt.fromtimestamp(open_time.iloc[number] / 1000)

titles=["Open Time","Open","High","Low","Close","Volume","Close Time","QAV","NAT","TBBAV","TBQAV","ignore"]

df = pd.read_csv("NEARUSDT3OMIN.csv", names=titles)

open_level = df["Open"]
close_level = df["Close"]
high_level = df["High"]
low_level = df["Low"]
open_time = df["Open Time"]



def bot2():
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

    for i in range(48,len(close_level)):
        if balance <= 10:
            print("GAME OVER!!!!")
            break
        if long :
            if low_level[i] < enter_value-stop*neg_coef:
                balance -= balance * ((stop * pos_coef) / enter_value  * leverage) - balance * commission*leverage

                negative+=1


                if max_lose < ((stop * pos_coef) / enter_value * leverage):
                    max_lose = ((stop * pos_coef) / enter_value * leverage)


                print("LONG EXITS NEGATIVE : ",calculate_time(i))
                print("BALANCE : ",balance)

                long = False
            elif high_level[i] > enter_value + stop *pos_coef:
                balance += balance * ((stop * pos_coef) / enter_value  * leverage) - balance * commission*leverage

                if max_win < ((stop * pos_coef) / enter_value * leverage):
                    max_win = ((stop * pos_coef) / enter_value * leverage)

                positive+=1
                print("LONG EXITS POSITIVE : ",calculate_time(i))
                print("BALANCE : ",balance)

                long = False


        if short:
            if high_level[i] > enter_value+stop*neg_coef:
                negative+=1
                balance -= balance * ((stop * pos_coef) / enter_value  * leverage) - balance * commission*leverage

                if max_lose < ((stop * pos_coef) / enter_value * leverage):
                    max_lose = ((stop * pos_coef) / enter_value * leverage)
                print("SHORT EXITS NEGATIVE : ",calculate_time(i))
                print("BALANCE : ",balance)
                short =False
            elif low_level[i] < enter_value-stop*neg_coef:
                positive+=1
                balance += balance * ((stop * pos_coef) / enter_value  * leverage) - balance * commission*leverage

                if max_win < ((stop * pos_coef) / enter_value * leverage):
                    max_win = ((stop * pos_coef) / enter_value * leverage)


                print("SHORT EXITS POSITIVE : ",calculate_time(i))
                print("BALANCE : ",balance)

                short =False


        if ( not short and not long):

            if (close_level[i] > open_level[i]) and (close_level[i-2] > open_level[i-2]) and (close_level[i-1] < open_level[i-1]) and  (
                close_level[i]-open_level[i] > open_level[i-1]-close_level[i-1] )and (close_level[i-2]-open_level[i-2] > open_level[i-1]-close_level[i-1] ):
                enter_value = close_level[i]
                stop = abs(close_level[i]-open_level[i])
                print("\nLONG OPEN : ",calculate_time(i))
                long = True

            if (close_level[i] < open_level[i]) and (close_level[i-2]  <open_level[i-2]) and (close_level[i-1] > open_level[i-1]) and  (
                 open_level[i] - close_level[i] > close_level[i-1]-open_level[i-1]   )and (open_level[i-2] - close_level[i-2] > close_level[i-1]-open_level[i-1]   ):
                enter_value = close_level[i]
                stop = abs(close_level[i] - open_level[i])
                print("\nSHORT OPEN : ",calculate_time(i))
                short = True


    print("\n\n\nBALANCE : ", balance)
    print("POSITIVE : ", positive)
    print("NEGATIVE : ", negative)
    print("RATE :", positive / (positive + negative))
    print("MAX WIN : ", max_win)
    print("MAX LOSE : ", max_lose)
    print("LEVERAGE : ", leverage)


bot2()


"""
1 HOUR NEAR

BALANCE :  11282359.73406757
POSITIVE :  275
NEGATIVE :  189
RATE : 0.5926724137931034
MAX WIN :  0.6309181827854047
MAX LOSE :  0.585210806768254
LEVERAGE :  10

30 MIN

BALANCE :  256673706197.07138
POSITIVE :  553
NEGATIVE :  343
RATE : 0.6171875
MAX WIN :  3.326602725896013
MAX LOSE :  0.7869080779944283
LEVERAGE :  10

"""