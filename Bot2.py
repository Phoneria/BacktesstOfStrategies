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



def bot2(value):
    balance = 100

    short_position = False
    long_position = False
    stop = 0
    enter_value= 0
    pos_coef = 1
    neg_coef = 2
    commission = 0.002
    leverage =value
    max_win = 0
    max_lose = 0
    positive = 0
    negative = 0
    max_balance = 0
    for i in range(48,len(close_level)):
        if balance < 10 :
            print("GAME OVER!!!!!")
            break

        if short_position:
            if high_level[i] > (enter_value + stop*neg_coef):
                short_position = False
                negative += 1

                balance -= balance * ((stop * neg_coef) / enter_value  * leverage) - balance * commission*leverage
                print("SHORT EXITS NEGATIVE : ", calculate_time(i))
                print("BALANCE : ", balance)
                if max_lose < ((stop * pos_coef) / enter_value * leverage):
                    max_lose = ((stop * pos_coef) / enter_value * leverage)


            elif low_level[i] < (enter_value - stop*pos_coef):
                short_position = False
                positive += 1
                balance += balance * ((stop * pos_coef) / enter_value * leverage) - balance * commission*leverage
                print("SHORT EXITS POSITIVE : ", calculate_time(i))
                print("BALANCE : ", balance)
                if max_win < ((stop * pos_coef) / enter_value * leverage):
                    max_win = ((stop * pos_coef) / enter_value * leverage)

        if long_position:
            if high_level[i] > (enter_value + stop*pos_coef)  :
                long_position = False
                positive += 1
                balance += balance*( (stop*pos_coef) /enter_value   * leverage   ) - balance*commission*leverage


                print("LONG EXITS POSITIVE : ", calculate_time(i))
                print("BALANCE : ",balance)

                if max_win < ((stop * pos_coef) / enter_value * leverage):
                    max_win = ((stop * pos_coef) / enter_value * leverage)

            elif low_level[i] < (enter_value - stop*neg_coef) :
                long_position = False
                negative += 1

                balance-= balance*((stop*neg_coef) / enter_value * leverage) -balance*commission*leverage

                print("LONG EXITS NEGATIVE : ", calculate_time(i))
                print("BALANCE : ",balance)

                if max_lose < ((stop * pos_coef) / enter_value * leverage):
                    max_lose = ((stop * pos_coef) / enter_value * leverage)

        if (not short_position and not long_position) :
            #LONG POSITION
            if (open_level[i] == low_level[i])    :


                long_position=True
                stop =abs(close_level[i] - open_level[i])
                enter_value = close_level[i]
                print("\nLONG OPEN : ", calculate_time(i))


                print("ENTER VALUE : ",enter_value)
                print("STOP : ", stop)
                print("TP : ",enter_value+stop)
                print("STOP LOSS : ",enter_value-stop*neg_coef)


            #SHORT POSITION
            elif  open_level[i] == high_level[i] :

                short_position= True
                stop = abs(close_level[i] - open_level[i])
                enter_value = close_level[i]
                print("\nSHORT OPEN : ", calculate_time(i))

                print("ENTER VALUE : ",enter_value)
                print("STOP : ", stop)
                print("TP : ", enter_value - stop)
                print("STOP LOSS : ", enter_value + stop*neg_coef)

            if balance > max_balance:
                max_balance = balance


    print("\n\n\nBALANCE : ",balance)
    print("POSITIVE : ",positive)
    print("NEGATIVE : ",negative)
    print("RATE :",positive/(positive+negative))
    print("MAX WIN : ",max_win)
    print("MAX LOSE : ",max_lose)
    print("LEVERAGE : ",leverage)
    print("MAX BALANCE : ",max_balance)
bot2(10)




"""
NEARUSDT
1 HOUR
BALANCE :  4263.164197034513
POSITIVE :  91
NEGATIVE :  36
RATE : 0.7165354330708661
MAX WIN :  0.6841870824053459
MAX LOSE :  0.3960396039603964
LEVERAGE :  10


30 MIN
BALANCE :  112718.48640101322
POSITIVE :  271
NEGATIVE :  125
RATE : 0.6843434343434344
MAX WIN :  0.587975633442218
MAX LOSE :  0.3662568885120817
LEVERAGE :  10


BTCUSDT
1 HOUR
BALANCE :  267.45562867574876
POSITIVE :  41
NEGATIVE :  19
RATE : 0.6833333333333333
MAX WIN :  0.24099078006823163
MAX LOSE :  0.10257198979826579
LEVERAGE :  10


30 MIN
BALANCE :  866.2231334356657
POSITIVE :  125
NEGATIVE :  67
RATE : 0.6510416666666666
MAX WIN :  0.7648085702693215
MAX LOSE :  0.12016516241793966
LEVERAGE :  10



"""

