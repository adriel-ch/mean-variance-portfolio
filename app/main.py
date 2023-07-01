import huobi.download_klines as kline
import datetime as dt
import dataprep
import mvo.mvo

if __name__ == "__main__":
    # Values
    start_date = dt.datetime(2023, 5, 1)
    end_date = dt.datetime(2023, 6, 1)
    symbol_list = ["BTC-USD", "ETH-USD", "LTC-USD"]
    data_period = ["60min"]
    # Download data from Huobi
    kline.download_daily_swap(start_date, end_date, data_period, symbol_list)

    # Extract and prepare data
    dataprep.zips_to_csv_appended(start_date, end_date, data_period, symbol_list)
    df = dataprep.join_all_closing_price(start_date, end_date, data_period, symbol_list)
    print(df)

    # import data into pandas for mean variance optim
    weights_array, risk_array, return_array = mvo.mvo.mean_variance_opt(df, symbol_list)
    weights_rows, weights_cols = weights_array.shape

    weights_list = []

    for i in range(weights_rows):
        weights_dict = {}
        for j in range(weights_cols):
            weights_dict[symbol_list[j] + "-weight"] = weights_array[i, j]
            
        weights_dict["annualised-risk"] = risk_array[i]
        weights_dict["annualised-return"] = return_array[i]
        weights_list.append(weights_dict)

    for i in range(len(weights_list)):
        print(weights_list[i])
    
    dataprep.save_weights(weights_list, filepath="app/output/weights/portfolio_weights.csv")
    mvo.mvo.eff_frontier(risk_array, return_array, True, filepath="app/output/plots/plot.png")
