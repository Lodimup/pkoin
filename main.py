import logging
import pandas as pd
from time import sleep
from binance.client import Client
from module import binance_extended as be
from cfg import cfg_logging
from helper.dataframe import (
    klines_to_df,
)

import settings

target_close = settings.target_close
target_volume = settings.target_volume
target_sd = settings.target_sd
since = settings.since

# TODO: use rate limit for sleep
rate_limit = 0.1


def main():
    logging.info(f'Looking for SHIT COINS that:\nprice < {target_close} USDT\nvolume < {target_volume/1000000}M USDT\nHave not got above mean + {target_sd}SD\nSince {since}')
    logging.info('-'*40)
    lst_symbols = be.get_symbols(filter='USDT')

    lst_shit_coins = []
    for symbol in lst_symbols:
        client = Client()
        logging.info(f'Getting {symbol}...')
        
        try:
            klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, "2 weeks ago UTC", "today")
        except Exception as e:
            logging.info(e)

        try:
            df = klines_to_df(klines)
            df['volume_usdt'] = df['volume']*df['close']
            close_mean = df['close'].mean()
            close_sd = df['close'].std()
            vol_mean = df['volume_usdt'].mean()
            last_price = df['close'][-1]
        except Exception as e:
            logging.info(e)
        sleep(rate_limit)

        if (last_price < target_close) and (vol_mean < target_volume) and (last_price < close_mean + close_sd*target_sd):
            logging.info(f'Found: {symbol}!')
            lst_shit_coins.append(symbol)

    pd.DataFrame({'shit_coins': lst_shit_coins}).to_csv('list_of_shit_coins.csv')

if __name__ == '__main__':
    main()
