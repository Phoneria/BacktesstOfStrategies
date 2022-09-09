You can create new files using FileWriter.py



You just need to change coin_name and time which placed 5th line and timeframe that placed in the 21th line 


For example :




coin= create_csv(coin_name,bring_data(coin_name,Client.KLINE_INTERVAL_30MINUTE,"1 January 2022","20 September 2022"))
coin= create_csv(coin_name,bring_data(coin_name,Client.KLINE_INTERVAL_5MINUTE,"1 June 2022","20 July 2022"))
coin= create_csv(coin_name,bring_data(coin_name,Client.KLINE_INTERVAL_1HOUR,"1 January 2021","20 September 2022"))
coin= create_csv(coin_name,bring_data(coin_name,Client.KLINE_INTERVAL_1DAY,"1 January 2021","20 September 2030"))





The last parameter can be a date as distant as a you wish. I hope, it won't be a problem
