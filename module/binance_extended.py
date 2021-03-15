from binance.client import Client
import pandas as pd
import requests
from time import sleep
import logging
from cfg import cfg_logging


def get_symbols(filter='USDT'):
    client = Client()
    logging.info('Getting symbols')
    exchange_info = client.get_exchange_info()
    logging.info('Done!')
    df_symbol = pd.DataFrame(exchange_info['symbols'])
    df_symbol = df_symbol[df_symbol['quoteAsset'] == filter]
    lst_pairs = df_symbol['symbol']
    return lst_pairs
