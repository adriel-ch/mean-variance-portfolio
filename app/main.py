import logging
import sys
import api.download_klines as kline
from datetime import datetime

if __name__ == "__main__":
    # start app
    # download data
    start_date = datetime(2023, 5, 1)
    end_date = datetime(2023, 6, 1)
    kline.download_daily_future(start_date, end_date, ["60min"], ["BTC"])
    #extract data
    # import data into pandas for mean variance optim
