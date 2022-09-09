import pandas as pd
from binance import Client
from datetime import datetime as dt
import pandas_ta as ta


client = Client(None, None)


def calculate_time(number):
    return dt.fromtimestamp(open_time.iloc[number] / 1000)


titles = ["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time", "QAV", "NAT", "TBBAV", "TBQAV", "ignore"]

df = pd.read_csv("NEARUSDT1HOUR.csv", names=titles)

open_level = df["Open"]
close_level = df["Close"]
high_level = df["High"]
low_level = df["Low"]
open_time = df["Open Time"]

psar = ta.psar(high=high_level, low=low_level, af=0.01, af0=0.01, max_af=0.2)
stoch = ta.stochrsi(close=close_level)
macd = ta.macd(close_level, 12, 26, 9)
fisher = ta.fisher(high=high_level, low=low_level, length=10)
super_trend = ta.supertrend(high=high_level, close=close_level, low=low_level, length=10, multiplier=3)
atr = ta.atr(high=high_level, close=close_level, low=low_level, length=14)
rsi = ta.rsi(close_level)
def only_psar():
    balance = 100
    number_of_operation = 0
    commision = 0.002
    enter_level = 0
    exit_level = 0
    is_in_operation = False

    for i in range(len(close_level)):

        if (psar.iat[i, 0] > 0) and not (psar.iat[i - 1, 0] > 0) and not is_in_operation:  # Yükseliş sinyali
            enter_level = close_level[i]
            is_in_operation = True
            number_of_operation += 1

        elif (psar.iat[i, 1] > 0) and not (psar.iat[i - 1, 1] > 0) and is_in_operation:

            exit_level = psar.iat[i - 1, 0]

            if (exit_level > enter_level):
                balance = balance + (balance * (exit_level - enter_level) / enter_level)
            else:
                balance = balance - (balance * (enter_level - exit_level) / enter_level)

            is_in_operation = False
            balance -= balance * commision
    print(f"Balance : {balance} \nİşlem Sayısı : {number_of_operation}")
def only_macd():
    balance = 100
    number_of_operation = 0
    commision = 0.002
    enter_level = 0
    exit_level = 0
    is_in_operation = False

    for i in range(48, len(close_level)):
        if (macd.iat[i - 1, 1] <= 0) and (macd.iat[i, 1] > 0) and (macd.iat[i, 0] < 0) and not (
        is_in_operation):  # MACD'nin yükseliş sinyali.Mavi , turuncuyu 0'ın altında alttan kesiyor
            enter_level = close_level[i]
            is_in_operation = True
            number_of_operation += 1

        if is_in_operation and (macd.iat[i - 1, 1] >= 0) and (macd.iat[i, 1] < 0):
            exit_level = close_level[i]

            if (exit_level > enter_level):
                balance = balance + balance * (exit_level - enter_level) / enter_level
            else:
                balance = balance - balance * (enter_level - exit_level) / enter_level
            balance -= balance * commision

            is_in_operation = False
    print(f"Balance : {balance} \nİşlem Sayısı : {number_of_operation}")
def only_fisher():
    balance = 100
    number_of_operation = 0
    commision = 0.002
    enter_level = 0

    is_in_operation = False
    for i in range(48, len(close_level)):
        if not is_in_operation and (fisher.iat[i, 0] > fisher.iat[i, 1]) and (fisher.iat[i, 0] < -2):
            enter_level = close_level[i]
            is_in_operation = True
            number_of_operation += 1

        if is_in_operation and (fisher.iat[i, 0] < fisher.iat[i, 1]):
            exit_level = close_level[i]

            if (exit_level > enter_level):
                balance = balance + balance * (exit_level - enter_level) / enter_level
            else:
                balance = balance - balance * (enter_level - exit_level) / enter_level
            balance -= balance * commision

            is_in_operation = False
    print(f"Balance : {balance} \nİşlem Sayısı : {number_of_operation}")
def only_stoch():
    balance = 100
    number_of_operation = 0
    commision = 0.002
    enter_level = 0
    exit_level = 0
    is_in_operation = False
    for i in range(48, len(close_level)):
        if (stoch.iat[i - 1, 0] < stoch.iat[i - 1, 1]) and (stoch.iat[i, 0] > stoch.iat[i, 1]):
            enter_level = close_level[i]
            is_in_operation = True
            number_of_operation += 1

        if is_in_operation and (stoch.iat[i - 1, 0] > stoch.iat[i - 1, 1]) and (stoch.iat[i, 0] < stoch.iat[i, 1]):
            exit_level = close_level[i]

            if (exit_level > enter_level):
                balance = balance + balance * (exit_level - enter_level) / enter_level
            else:
                balance = balance - balance * (enter_level - exit_level) / enter_level
            balance -= balance * commision

            is_in_operation = False
    print(f"Balance : {balance} \nİşlem Sayısı : {number_of_operation}")
def only_supertrend():
    balance = 100
    number_of_operation = 0
    commision = 0.002
    enter_level = 0
    exit_level = 0
    is_in_operation = False
    for i in range(48, len(close_level)):
        if (super_trend.iat[i, 1] > 0) and not is_in_operation:
            enter_level = close_level[i]
            is_in_operation = True
            number_of_operation += 1

        if is_in_operation and super_trend.iat[i, 1] < 0:
            exit_level = close_level[i]

            if (exit_level > enter_level):
                balance = balance + balance * (exit_level - enter_level) / enter_level
            else:
                balance = balance - balance * (enter_level - exit_level) / enter_level
            balance -= balance * commision

            is_in_operation = False
    print(f"Balance : {balance} \nİşlem Sayısı : {number_of_operation}")
def only_rsi():
    balance = 100
    number_of_operation = 0
    commision = 0.002
    enter_level = 0
    exit_level = 0
    is_in_operation = False
    for i in range(48, len(close_level)):
        if (rsi.iloc[i-1]<30) and (rsi.iloc[i]>=30) and not is_in_operation :
            enter_level = close_level[i]
            is_in_operation = True
            number_of_operation += 1

        if is_in_operation and (super_trend.iat[i, 1] < 0):
            exit_level = close_level[i]

            if (exit_level > enter_level):
                balance = balance + balance * (exit_level - enter_level) / enter_level
            else:
                balance = balance - balance * (enter_level - exit_level) / enter_level
            balance -= balance * commision

            is_in_operation = False
    print(f"Balance : {balance} \nİşlem Sayısı : {number_of_operation}")

