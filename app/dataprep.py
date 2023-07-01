import pandas as pd
import glob
import datetime as dt
import os

data_dir = "app/data"

def zips_to_csv_appended(start_date, end_date, selected_data_period: list, selected_symbols: list) -> None:
    """
    Reads the directory for HuoBi zipped data files and appends them all into one single csv.
    """
    zip_data_dir = data_dir + "/zips"
    col_headers = ["id-time", "open", "close", "high", "low", "vol", "amount"]

    wd = os.getcwd()
    savepath = wd + "/" + zip_data_dir
    if not os.path.exists(os.path.dirname(savepath)):
        os.mkdir(os.path.dirname(savepath))

    for symbols in selected_symbols:
        for period in selected_data_period: # for future expansion for more data periods
            li = []
            # future add parse for dates
            all_files = sorted(glob.glob(f"{zip_data_dir}/{symbols}-{period}*.zip"))
            for files in all_files:
                symbol_df = pd.read_csv(files, names=col_headers) # read csv zip
                # convert to SGT
                symbol_df["id-time"] = pd.to_datetime(symbol_df["id-time"], unit="s")
                symbol_df = symbol_df.set_index("id-time")
                symbol_df = symbol_df.tz_localize("UTC").tz_convert("Asia/Singapore")
                li.append(symbol_df) # append to df

            full_df = pd.concat(li)#ignore_index=True
            print(f"{symbols} Swap Futures Data\n",full_df)
            full_df.to_csv(f"{data_dir}/{symbols}-{period}.csv")
            # {start_date.strftime('%Y-%B')}

    return

def get_closing_price(start_datetime: dt.datetime,
                      end_datetime: dt.datetime,
                      period: str,
                      symbols: str) -> pd.DataFrame:
    """
    Func to get the closing price of the specified item over a specified time period.
    Adds the name of the symbol to the header of the closing price.

    You can specify the hour that you want to select from.
    """
    all_files = sorted(glob.glob(f"{data_dir}/{symbols}-{period}.csv"))
    df = pd.read_csv(f"{data_dir}/{symbols}-{period}.csv", index_col=0)[["close"]]
    renamed = f"{symbols}-close"
    df_col_renamed = df.rename(columns={"close": renamed})
    close_price = df_col_renamed.loc[str(start_datetime):str(end_datetime)]
    return close_price

def join_all_closing_price(start_date, end_date, selected_data_period: list, selected_symbols: list):
    df_list = []
    for symbol in selected_symbols:
        df_list.append(get_closing_price(start_date, end_date, selected_data_period[0], symbol))

    return pd.concat(df_list, axis="columns")

def save_weights(weights_array_list: list, filepath: str):
    wd = os.getcwd()
    savepath = wd + "/" + filepath
    if not os.path.exists(os.path.dirname(savepath)):
        os.makedirs(os.path.dirname(savepath))

    df = pd.DataFrame(weights_array_list)
    df.to_csv(filepath)
    print(f"Portfolio weights saved to: {filepath}")
