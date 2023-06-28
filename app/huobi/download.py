import huobi.const as hbconst
import huobi.utils as hbutil
import datetime as dt

pre_url = "https://futures.huobi.com/data"

def b_download_daily_spot(data_type: str, start: dt.datetime, end: dt.datetime, all_period: list = [], all_symbols: list = []):
    '''return date is: [start, end)'''

    global pre_url
    if all_period is None:
        all_period = hbconst.ALL_PERIODS
    if start is None:
        start = hbconst.SPOT_START_DATE
    if end is None:
        end = hbconst.END_DATE

    if all_symbols is None:
        ok, all_symbols = hbutil.get_all_spot_symbols()
        if not ok:
            print(all_symbols)
            return
    for symbol in all_symbols:
        for period in all_period:
            if period in ['trades',]:
                path_url = f'{pre_url}/{data_type}/spot/daily/{symbol}'
            else:
                path_url = f'{pre_url}/{data_type}/spot/daily/{symbol}/{period}'
            all_oks, all_errs = hbutil.download_daily(
                path_url, symbol, period, start, end)
            print(f'success:{all_oks}')
            print(f'faild:{all_errs}')
    print('done')


def b_download_daily_future(data_type: str, start: dt.datetime, end: dt.datetime, all_period: list = [], all_symbols: list = []):
    '''return date is: [start, end)'''

    global pre_url
    if all_period is None:
        all_period = hbconst.ALL_PERIODS
    if start is None:
        start = hbconst.SPOT_START_DATE
    if end is None:
        end = hbconst.END_DATE

    if all_symbols is None:
        ok, all_symbols = hbutil.get_all_future_symbols()
        if not ok:
            print(all_symbols)
            return
    for symbol in all_symbols:
        for period in all_period:
            if period in ['trades',]:
                path_url = f'{pre_url}/{data_type}/future/daily/{symbol}'
            else:
                path_url = f'{pre_url}/{data_type}/future/daily/{symbol}/{period}'
            all_oks, all_errs = hbutil.download_daily(
                path_url, symbol, period, start, end)
            print(f'success:{all_oks}')
            print(f'faild:{all_errs}')
    print('done')


def b_download_daily_swap(data_type: str, start: dt.datetime , end: dt.datetime, all_period: list = [], all_symbols: list = []):
    '''return date is: [start, end)'''

    global pre_url
    if all_period is None:
        all_period = hbconst.ALL_PERIODS
    if start is None:
        start = hbconst.SPOT_START_DATE
    if end is None:
        end = hbconst.END_DATE

    if all_symbols is None:
        ok, all_symbols = hbutil.get_all_swap_symbols()
        if not ok:
            print(all_symbols)
            return
    for symbol in all_symbols:
        for period in all_period:
            if period in ['trades',]:
                path_url = f'{pre_url}/{data_type}/swap/daily/{symbol}'
            else:
                path_url = f'{pre_url}/{data_type}/swap/daily/{symbol}/{period}'
            all_oks, all_errs = hbutil.download_daily(
                path_url, symbol, period, start, end)
            print(f'success:{all_oks}')
            print(f'faild:{all_errs}')
    print('done')


def b_download_daily_linearswap(data_type: str, start: dt.datetime, end: dt.datetime, all_period: list = [], all_symbols: list = []):
    '''return date is: [start, end)'''

    global pre_url
    if all_period is None:
        all_period = hbconst.ALL_PERIODS
    if start is None:
        start = hbconst.SPOT_START_DATE
    if end is None:
        end = hbconst.END_DATE

    if all_symbols is None:
        ok, all_symbols = hbutil.get_all_linearswap_symbols()
        if not ok:
            print(all_symbols)
            return
    for symbol in all_symbols:
        for period in all_period:
            if period in ['trades',]:
                path_url = f'{pre_url}/{data_type}/linear-swap/daily/{symbol}'
            else:
                path_url = f'{pre_url}/{data_type}/linear-swap/daily/{symbol}/{period}'
            all_oks, all_errs = hbutil.download_daily(
                path_url, symbol, period, start, end)
            print(f'success:{all_oks}')
            print(f'faild:{all_errs}')
    print('done')


def b_download_daily_option(data_type: str, start: dt.datetime, end: dt.datetime, all_period: list = [], all_symbols: list = []):
    '''return date is: [start, end)'''

    global pre_url
    if all_period is None:
        all_period = hbconst.ALL_PERIODS
    if start is None:
        start = hbconst.SPOT_START_DATE
    if end is None:
        end = hbconst.END_DATE

    if all_symbols is None:
        ok, all_symbols = hbutil.get_all_option_symbols()
        if not ok:
            print(all_symbols)
            return
    for symbol in all_symbols:
        for period in all_period:
            if period in ['trades',]:
                path_url = f'{pre_url}/{data_type}/option/daily/{symbol}'
            else:
                path_url = f'{pre_url}/{data_type}/option/daily/{symbol}/{period}'
            all_oks, all_errs = hbutil.download_daily(
                path_url, symbol, period, start, end)
            print(f'success:{all_oks}')
            print(f'faild:{all_errs}')
    print('done')