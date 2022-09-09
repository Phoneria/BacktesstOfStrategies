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

ema = ta.ma("ema",close_level,length = 50)
atr = ta.atr(high=high_level,low=low_level,close=close_level,length=14)

def engulph():
    """
    Giriş Yeriş :
    1-) EMA 50'nin altında bir kırmızı mum ve bunun ardından gelen , bundan daha büyük bir yeşil mum
    2-) EMA 50'nin üstünde bir yeşil mum ve bunun ardından gelen , bundan daha büyük bir kırmızı mum

    Dikkat Edilmesi Gerekenler :
    1-) LONG işlemi için ; bir önceki mum (kırmızı) EMA 50'nin altında olmak zorunda ama şu anki mum (yeşil)mum EMA 50 üstü kapatabilir
    2-) SHORT işlemi için ; bir önceki mum (yeşil) EMA 50'nin üstünde olmak zorunda ama şu anki mum (kırmızı)mum EMA 50 altı kapatabilir
    3-) Mumların Hacimleri çok düşük olmamalı. Önceki mum doji olabilir ama şu anki mum doji olmamalı.
    Mesela LONG işlemi arıyorsak eğer, şu anki mumun üst fitili gövdeden büyük olmamalı.
    Aynı şekilde SHORT işleminde de şu anki mumun alt fitili gövdeden büyük olmamalı


    STOP LOSS:
    LONG pozisyonunda bir önceki mumun en küçük değeri şu anki mumdan daha küçükse burası - atr değerine değilse şu anki mumun en küçük değeri - atr değerine stop koyulur
    En küçük değerin altında bir mum kapanışında stop olmadan çıkmalı


    SHORT pozisyonunda bir önceki mumun en büyük değeri şu anki mumdan daha büyükse burası + atr değerine değilse şu anki mumun en büyük değeri + atr değerine stop koyulur
    En büyük değerin üstünde bir mum kapanışında stop olmadan çıkmalı


    TAKE PROFİT:
    Asıl TP yeri LONG'da isek, EMA 50 altına indikten sonra üstünde bir kapanış, SHORT'ta isek EMA 50 altına indikten sonra üstünde kapanış

    OPTİMİZASYON :

    EMA'nın farklı değerleri denenebilir
    Farklı zaman aralıkları denenebilir
    Diğer indikatörlerden onay alınabilir
    TP yeri için başka indikatör veya formasyonlarla back test yapılarak daha verimli sonuçlar alınabilir
    SuperTrend veya Parabolik Sar'a stop koyulabilir
    İşlemden çıkışı EMA üstünd veya altında kapanışa göre yapıyoruz ama küçük mumlar can sıkabiliyor. Bu yüzden ema + atr gibi bir şey yapabiliriz

    :return:
    """
    balance = 100
    enter_value = 0
    stop_level =0

    short_position = False
    long_position = False
    is_in_operation = False
    commision = 0.002
    leverage= 6
    positive = 0
    negative =0
    min_level = 0 # Long levelin stopu
    max_level = 0 # High Leveli Stopu
    for i in range(3650,len(close_level)):

        if (not is_in_operation) and(ema.iloc[i] > open_level[i])  and (close_level[i]> open_level[i]) and (close_level[i-1]<open_level[i-1]) \
                and (high_level[i]-close_level[i]<close_level[i]-open_level[i]) and(close_level[i]> open_level[i-1]) : # LONG POSITION
            # İşlemde Değil , emanın altında , şimdi yeşil mum , öncesi kırmızı mum, gövdesi üst fitilden daha büyük
            # Mumların hacimlerini de koşula ekleyebilir. İndikatör durumları da koşula eklenebilir
            is_in_operation = True
            long_position = True
            enter_value = close_level[i]
            stop_level_long = open_level[i]

            if(low_level[i]> low_level[i-1]): # Stop Seviyesini ayarladık.
                # Stopumuz Burada olucak ama yeşil mumun açılışının altında bir mum kapanışında çıkış yapıcaz
                min_level = low_level[i-1]
            else:
                min_level = low_level[i]
            min_level-=atr.iloc[i]
        #    print("\nLONG POSITION ")
         #   print(f"ENTER VALUE : {enter_value}, ZAMAN : {calculate_time(i)}")

        if (not is_in_operation) and (ema.iloc[i]<open_level[i]) and (close_level[i]< open_level[i]) and (close_level[i-1]> open_level[i-1]) \
            and (close_level[i]-low_level[i]<open_level[i]-close_level[i]) and (close_level[i]<open_level[i-1]):# SHORT POSITION
            # İşlemde Değil , EMA mumun açılışında daha küçük, şu anki kırmızı mum, bir önceki yeşil mum , gövdesi fitilinden daha büyük
            # Mumların hacimlerini de koşula ekleyebilir. İndikatör durumları da koşula eklenebilir
            is_in_operation = True
            short_position = True
            enter_value = close_level[i]
            stop_level_short = open_level[i]

            if(high_level[i]> high_level[i-1]):
                max_level= high_level[i]
            else:
                max_level= high_level[i-1]
            max_level+= atr.iloc[i]
          #  print("\nSHORT POSITION ")
          #  print(f"ENTER VALUE : {enter_value}, ZAMAN : {calculate_time(i)}")

        elif (is_in_operation) and (short_position) : # Eğer short pozisyonda ise
            # STOP LOSS
            if(high_level[i] > max_level):
                is_in_operation = False  # İşlem Kapatıldı
                short_position = False

                balance -= balance * (max_level - enter_value) / enter_value * 5  # Bakiyeden Düştük
                balance -= balance * commision  # Komisyon Kestik
            #    print(f"İŞLEM ZARARDA KAPADI, ZAMAN : {calculate_time(i)}")
            #    print(f"BALANCE : {balance}, MAX LEVEL : {max_level}")

            elif(close_level[i]>stop_level_short):
                is_in_operation = False # İşlem Kapatıldı
                short_position =False

                balance -= balance*(stop_level_short-enter_value)/enter_value *5# Bakiyeden Düştük
                balance -=balance*commision # Komisyon Kestik

              #  print(f"İŞLEM ZARARDA KAPADI, ZAMAN : {calculate_time(i)}")
             #   print(f"BALANCE : {balance}, STOP LEVEL : {stop_level_short}")


            # TAKE PROFIT
            elif(open_level[i]<ema.iloc[i]) and (close_level[i]> ema.iloc[i]): # Mum EMA'nın altında açılıp üstünde kapanış yapıcak
                is_in_operation = False # İşlem Kapatıldı
                short_position =False

                balance += balance * (enter_value-close_level[i])/enter_value*5
                balance -= balance * commision  # Komisyon Kestik

             #   print(f"İŞLEM KARDA KAPADI, ZAMAN : {calculate_time(i)}")
             #   print(f"BALANCE : {balance}, ÇIKIŞ YERİ : {close_level[i]}")


        elif (is_in_operation) and (long_position):  # Eğer long pozisyonda ise
            # STOP LOSS
            if (low_level[i]<min_level):
                is_in_operation = False
                long_position = False

                balance -= balance*(enter_value-min_level)/enter_value*5
                balance-=balance*commision
             #   print(f"İŞLEM ZARARDA KAPADI, ZAMAN : {calculate_time(i)}")
              #  print(f"BALANCE : {balance}, MINLEVEL : {min_level}")

            elif (close_level[i]<stop_level_long):
                is_in_operation = False
                long_position = False

                balance -= balance*(enter_value-close_level[i])/enter_value*5
                balance-= balance*commision
              #  print(f"İŞLEM ZARARDA KAPADI, ZAMAN : {calculate_time(i)}")
                #print(f"BALANCE : {balance}, STOP LEVEL : {stop_level_long}")
            # TAKE PROFIT

            elif(open_level[i]> ema.iloc[i]) and (close_level[i]< ema.iloc[i]):
                is_in_operation = False
                long_position= False

                balance += balance*(close_level[i]-enter_value)/enter_value*5
                balance-=balance*commision
               # print(f"İŞLEM KARDA KAPADI, ZAMAN : {calculate_time(i)}")
               # print(f"BALANCE : {balance}, ÇIKIŞ YERİ : {close_level[i]}")


    print(f"BAKİYE : {balance}")

engulph()
"""
1 Saatlik
Number Of Operation : 875
Balance : 28106.685248952468
Positive : 174
Negative : 263
Rate : 19.885714285714286
Commision = 0.002
Leverage= 6
Tarih : 1 Ocak 2021 - 30 Haziran 2022

30 Dakikalık
Number Of Operation : 579
Balance : 12317.051651619306
Positive : 109
Negative : 180
Rate : 18.825561312607945
Tarih: 1 Ocak 2022 - 30 Haziran 2022

Number Of Operation : 1783
Balance : 160120333.61657864
Positive : 348
Negative : 543
Rate : 19.5176668536175
Tarih : 1 Ocak 2021 - 30 Haziran 2022

15 Dakikalık
Number Of Operation : 1139
Balance : 157820.24370655307
Positive : 216
Negative : 353
Rate : 18.964003511852503
Tarih : 1 Ocak 2022 - 30 Haziran 2022

5 Dakikalık
Number Of Operation : 3369
Balance : 2084753.1586049784
Positive : 649
Negative : 1035
Rate : 19.263876521222915
Tarih : 1 Ocak 2022 - 30 Haziran 2022

"""

"""
# SHORT ENGULF
        if not (is_in_operation) and (open_level[i]> close_level[i]) and (close_level[i-1]> open_level[i-1])and(
                abs(close_level[i]-open_level[i])> abs(close_level[i]-low_level[i])) and(ema.iloc[i]>close_level[i-1]) and (
                close_level[i]< open_level[i-1]) : # Kırmızı bir mumsa
            enter_value = close_level[i]
            stop_level = close_level[i-1]
            number_of_operation+=1
            is_in_operation = True
            short_position =True
            print(f"ENTER SHORT POSITION : {calculate_time(i)}")
       # LONG ENGULPF
        if not (is_in_operation) and (open_level[i] < close_level[i]) and (close_level[i - 1] <open_level[i - 1]) and (
                abs(close_level[i] - open_level[i]) < abs(close_level[i] - high_level[i])) and (ema.iloc[i]<close_level[i])and(
            close_level[i]> open_level[i-1]
        ):  # Yeşil bir mumsa
            enter_value = close_level[i]
            stop_level = close_level[i - 1]
            number_of_operation += 1
            is_in_operation = True
            long_position = True
            print(f"ENTER LONG POSITION : {calculate_time(i)}")
        if is_in_operation and short_position:
            if close_level[i]> stop_level:#Olumsuz Kapanış
                balance = balance - balance*(stop_level-enter_value)/stop_level*leverage
                is_in_operation= False
                short_position=False
                number_of_operation+=1
                positive+=1
                balance-= balance*commision
                print(f"SHORT EXITS NEGATIVE , BAlANCE = {balance} ,LOSS = {balance*(stop_level-enter_value)/stop_level*leverage} {calculate_time(i)}\n")
            elif (close_level[i]> ema.iloc[i]): #Olumlu Kapanış
                balance = balance + balance * (stop_level - enter_value) / stop_level*leverage
                is_in_operation = False
                short_position = False
                number_of_operation += 1
                negative+=1
                balance-= balance*commision
                print(f"SHORT EXITS POSITIVE , BAlANCE = {balance} , {calculate_time(i)}\n")

        if is_in_operation and long_position:
            if close_level[i]<stop_level:#Olumsuz Kapanış
                balance = balance - balance*(stop_level-enter_value)/stop_level*leverage
                is_in_operation= False
                long_position=False
                number_of_operation+=1
                balance-= balance*commision
                negative+=1
                print(f"SHORT EXITS NEGATIVE , BAlANCE = {balance} , {calculate_time(i)}\n")
            elif close_level[i]< ema.iloc[i]: #Olumlu Kapanış
                balance = balance + balance * (stop_level - enter_value) / stop_level*leverage
                is_in_operation = False
                long_position = False
                number_of_operation += 1
                balance-= balance*commision
                positive+=1
                print(f"SHORT EXITS POSITIVE , BAlANCE = {balance} , {calculate_time(i)}\n")
    print(f"Number Of Operation : {number_of_operation}\nBalance : {balance}\nPositive : {positive}\nNegative : {negative}\nRate : {positive/number_of_operation*100}")
"""