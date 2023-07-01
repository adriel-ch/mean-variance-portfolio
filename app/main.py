import logging
import sys
import huobi.download_klines as kline
import datetime as dt
import dataprep
import mvo.mvo

import huobi.const
import huobi.utils


if __name__ == "__main__":
    # start app

    # download data
    start_date = dt.datetime(2023, 5, 1)
    end_date = dt.datetime(2023, 6, 1)
    symbol_list = ["BTC-USD", "ETH-USD", "LTC-USD"]
    data_period = ["60min"]
    # kline.download_daily_future(start_date, end_date, ["60min"], ["BTC230630"])

    # ok, all_symbols = get_all_future_symbols()
    # if not ok:
    #     print(all_symbols)
    # print(all_symbols)

    # kline.download_daily_swap(start_date, end_date, data_period, symbol_list) # main ex

    #extract data
    # dataprep.zips_to_csv_appended(start_date, end_date, data_period, symbol_list)

    # Join into single df
    df = dataprep.join_all_closing_price(start_date, end_date, data_period, symbol_list)
    print(df)

    # import data into pandas for mean variance optim
    weights_array, risk_array, return_array = mvo.mvo.mean_variance_opt(df, symbol_list)
    weights_rows, weights_cols = weights_array.shape

    weights_list = []

    for i in range(weights_rows):
        weights_dict = {}
        for j in range(weights_cols):
            weights_dict[symbol_list[j]] = weights_array[i, j]
            
        weights_dict["annualised-risk"] = risk_array[i]
        weights_dict["annualised-return"] = return_array[i]
        weights_list.append(weights_dict)

    # for i in range(len(weights_list)):
    #     print(weights_list[i])

    mvo.mvo.eff_frontier(risk_array, return_array, True, save_output="app/output/plots/plot.png")
