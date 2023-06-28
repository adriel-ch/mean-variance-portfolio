import logging
import sys
import huobi.download_klines as kline
from datetime import datetime
import extract as extr

import huobi.const
import huobi.utils


if __name__ == "__main__":
    # start app

    # download data
    start_date = datetime(2023, 5, 1)
    end_date = datetime(2023, 5, 2)
    symbol_list = ["BTC-USD", "ETH-USD", "LTC-USD"]
    data_period = ["60min"]
    # kline.download_daily_future(start_date, end_date, ["60min"], ["BTC230630"])

    # ok, all_symbols = get_all_future_symbols()
    # if not ok:
    #     print(all_symbols)
    # print(all_symbols)

    kline.download_daily_swap(start_date, end_date, data_period, symbol_list) # main ex

    #extract data
    extr.read_and_combine(start_date, end_date, data_period, symbol_list)

    # import data into pandas for mean variance optim
