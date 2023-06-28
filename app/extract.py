import pandas as pd
import glob
import datetime as dt

def read_and_combine(start_date, end_date, selected_data_period: list, selected_symbols: list):
    """
    Reads the directory for HuoBi zipped data files and appends them all into one single csv.
    """
    data_dir = "app/data"
    zip_data_dir = data_dir + "/zips"
    col_headers = ["id-time", "open", "close", "high", "low", "vol", "amount"]

    for symbols in selected_symbols:
        for period in selected_data_period: # for future expansion for more data periods
            li = []
            # future add parse for dates
            all_files = sorted(glob.glob(f"{zip_data_dir}/{symbols}-{period}*.zip"))
            for files in all_files:
                symbol_df = pd.read_csv(files, names=col_headers) # read csv zip
                li.append(symbol_df) # append to df

            full_df = pd.concat(li, ignore_index=True)
            print(f"{symbols} Swap Futures Data\n",full_df)
            full_df.to_csv(f"{data_dir}/{symbols}-{period}-{start_date.strftime('%Y-%B')}.csv")

    return

