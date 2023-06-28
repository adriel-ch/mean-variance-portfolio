from huobi.const import *
from huobi.utils import *
from huobi.download import *

data_type = 'trades'


# def download_daily_spot(start: datetime, end: datetime, all_symbols: list = []):
#     '''return date is: [start, end)'''

#     global data_type
#     b_download_daily_spot(data_type, start, end, ['trades'], all_symbols)


def download_daily_future(start: datetime, end: datetime, all_symbols: list = []):
    '''return date is: [start, end)'''

    global data_type
    b_download_daily_future(data_type, start, end, ['trades'], all_symbols)


# def download_daily_swap(start: datetime, end: datetime, all_symbols: list = []):
#     '''return date is: [start, end)'''

#     global data_type
#     b_download_daily_swap(data_type, start, end, ['trades'], all_symbols)


# def download_daily_linearswap(start: datetime, end: datetime, all_symbols: list = []):
#     '''return date is: [start, end)'''

#     global data_type
#     b_download_daily_linearswap(data_type, start, end, ['trades'], all_symbols)


# def download_daily_option(start: datetime, end: datetime, all_symbols: list = []):
#     '''return date is: [start, end)'''

#     global data_type
#     b_download_daily_option(data_type, start, end, ['trades'], all_symbols)


# if __name__ == "__main__":
#     download_daily_spot(all_symbols=['btcusdt', 'ltcusdt'],
#                         start=datetime(2021, 1, 1),
#                         end=datetime(2021, 2, 1))
    #download_daily_future()
    #download_daily_swap()
    #download_daily_linearswap()
    #download_daily_option()