from binance import Client
import csv


coin_name= "NEARUSDT"
time = "30MIN"
client =Client(None,None)

def bring_data(symbol,periot,open,end):
    candles=client.get_historical_klines(symbol,periot,open,end)
    return candles

def create_csv(symbol,candles):
    csv_file=open(symbol+time+".csv","w",newline="")
    writer=csv.writer(csv_file)
    for candle in candles:
        writer.writerow(candle)

    csv_file.close()

coin= create_csv(coin_name,bring_data(coin_name,Client.KLINE_INTERVAL_30MINUTE,"1 January 2022","20 September 2022"))

