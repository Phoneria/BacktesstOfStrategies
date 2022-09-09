import pandas as pd
from binance import Client
from datetime import datetime as dt
import pandas_ta as ta
import OTT
import numpy as np

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



def alsat():
    balance = 100
    commission = 0.002
    bullish = False
    bearish = False
    enter_level = 0
    leverage = 1

    ind = OTT.ott(df).fillna(value=0)
    ottl = ind.OTT
    MAvgl=ind.MAvg
    above =np.where(ta.cross(MAvgl,ottl,above=True),True,False)
    below = np.where(ta.cross(ottl,MAvgl,above=True),True,False)

    for i in range(len(close_level)):
        if above[i]:
            bullish = True
            if bearish:
                if enter_level > close_level[i]:
                    balance+= balance* enter_level-close_level/enter_level * leverage
                    balance-= balance*commission
                else:
                    balance -= balance * enter_level - close_level / enter_level * leverage
                    balance -= balance * commission

                bearish = False

            enter_level = close_level[i]
            print(f"BULLISH : {calculate_time(i)}\nBalance : {balance}\n")

        elif below[i]:
            bearish = True
            if bullish:
                if enter_level < close_level[i]:
                    balance += balance * enter_level - close_level / enter_level * leverage
                    balance -= balance * commission
                else:
                    balance -= balance * enter_level - close_level / enter_level * leverage
                    balance -= balance * commission

                bullish = False

            enter_level = close_level[i]
            print(f"BEARISH : {calculate_time(i)}\nBalance : {balance}\n")
    print(balance)
alsat()