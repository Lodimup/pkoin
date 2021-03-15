import pandas as pd
from datetime import datetime
import numpy as np


def klines_to_df(klines):
    """ Turns klines to df with proper columns
    """

    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore']
    dtypes = {
        'timestamp': 'int',
        'open': 'float',
        'high': 'float',
        'low': 'float',
        'close': 'float',
        'volume': 'float',
        'close_time': 'int',
        'quote_av': 'float',
        'trades': 'int',
        'tb_base_av': 'float',
        'tb_quote_av': 'float',
        #'ignore': 'int'
        }

    df = pd.DataFrame(klines, columns=columns)
    df['date'] = df['timestamp'].apply(lambda x: datetime.fromtimestamp(x/1000))
    df = df.astype(dtypes)
    df = df.set_index('date', drop=True)
    return df


def add_log_return(df):
    """Adds a log return column to df
    """
    df['log_return'] = np.log(df['close']/df['close'].shift(1))
    return df


def add_rolling_vol_sd(df, period=60):
    """Adds a rolling volume sd
    """

    df['vol_sd'] = (df['volume']*df['close']).rolling(30).std()
    return df


def add_rolling_vol_mean(df, period=60):
    """Adds a rolling volume sd
    """
    df['vol_mean'] = (df['volume']*df['close']).rolling(30).mean()
    return df


def test_unusual_vol(df, sd_greater=2):
    """
    """
    df['unusual_vol'] = df['volume'] > (df['vol_sd']*sd_greater + df['vol_mean'])
    return df
