import huobi.const as hbconst
# import huobi.utils as hbutil
import huobi.download as hbdl
import datetime as dt

data_type = 'klines'


def download_daily_spot(start: dt.datetime, end: dt.datetime, all_period: list = [], all_symbols: list = []):
    '''return date is: [start, end)'''

    global data_type
    hbdl.b_download_daily_spot(data_type, start, end, all_period, all_symbols)


def download_daily_future(start: dt.datetime, end: dt.datetime, all_period: list = [], all_symbols: list = []):
    '''return date is: [start, end)'''

    global data_type
    hbdl.b_download_daily_future(data_type, start, end, all_period, all_symbols)


def download_daily_swap(start: dt.datetime, end: dt.datetime, all_period: list = [], all_symbols: list = []):
    '''
    return date is: [start, end)

    Downloads swap k-line data from HuoBi REST API. Specify a data range, period of data (5min, 1day), and a list of symbols to pull.

    Writes to ./app/data/zips
    '''

    global data_type
    hbdl.b_download_daily_swap(data_type, start, end, all_period, all_symbols)


def download_daily_linearswap(start: dt.datetime, end: dt.datetime, all_period: list = [], all_symbols: list = []):
    '''return date is: [start, end)'''

    global data_type
    hbdl.b_download_daily_linearswap(data_type, start, end, all_period, all_symbols)


def download_daily_option(start: dt.datetime, end: dt.datetime, all_period: list = [], all_symbols: list = []):
    '''return date is: [start, end)'''

    global data_type
    hbdl.b_download_daily_option(data_type, start, end, all_period, all_symbols)


# if __name__ == "__main__":
    # download_daily_spot(all_symbols=['BTCUSDT', 'ADAUSDT'],
    #                     start=datetime(2021, 5, 21),
    #                     end=datetime(2021, 5, 23),
    #                     all_period=['1min', '15min'])
    # download_daily_future(start=datetime(2021, 5, 21), end=datetime(2021, 5, 23), all_period=['60min'])
    #download_daily_swap()
    #download_daily_linearswap()
    #download_daily_option(all_period=['1min'])