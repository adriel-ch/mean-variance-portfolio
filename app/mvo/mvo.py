import datetime as dt

import dataprep
import numpy as np
import pandas as pd
import scipy.optimize as scp

np.set_printoptions(suppress=True) # suppress sci notation


start_date = dt.datetime(2023, 5, 1)
end_date = dt.datetime(2023, 5, 2)
symbol_list = ["BTC-USD", "ETH-USD", "LTC-USD"]
data_period = ["60min"]

df = dataprep.join_all_closing_price(start_date, end_date, data_period, symbol_list)
print(df)

def rate_of_return(df: pd.DataFrame) -> np.ndarray:
    """
    Calculates the rate of return "Returns" for each element of the input DataFrame.
    Expressed as a percentage of input data.
    """
    closing_price_array = df.to_numpy()
    rows, cols = closing_price_array.shape
    array_returns = np.zeros([rows, cols])
    for j in range(cols):
        for i in range(rows):
            try:
                array_returns[i, j] = ((closing_price_array[i + 1, j] - closing_price_array[i, j]) / closing_price_array[i, j]) * 100
            except IndexError:
                array_returns[i, j] = ((closing_price_array[i, j] - closing_price_array[i, j]) / closing_price_array[i, j]) * 100
    
    # print(array_returns)
    return array_returns

ror = rate_of_return(df)

# mean returns
mean_ror = np.mean(ror, axis=0)
print("Mean ROR\n", mean_ror)

# Mean return of the entire portfolio per interval (hr)
# Equally weighted cotribution to the mean
portfolio_ror = np.mean(ror, axis=1) # or market ror
print("Portfolio ROR\n", portfolio_ror)

# Covariance matrix of the assets within ror against each other
covar_ror = np.cov(ror, rowvar=False) # rowvar = False because variables(assets) are in the cols
print("Covariance Matrix assets within portfolio\n", covar_ror)

# compute betas of assets in the portfolio
cols = ror.shape[1]
beta = []
portfolio_ror_variance = np.var(portfolio_ror, ddof = 1)
for i in range(cols):
    # covar_matrix = np.cov(portfolio_ror[:, 0], ror[:, i])
    covar_matrix = np.cov(portfolio_ror, ror[:, i])
    print(f"Covar Matrix for asset: {symbol_list[i]} with Portfolio mean ROR\n", covar_matrix)
    covar  = covar_matrix[1,0]
    print("Covar Value: ", covar) 
    beta.append(covar/portfolio_ror_variance)

print("Beta Values: ", beta)

weights = np.array([0.33333, 0.33333, 0.33333])

portfolio_return = np.matmul(np.array(mean_ror), weights.T)
print(portfolio_return)
annual_return = 365 * np.array(portfolio_return)
print("Portfolio Return\n", portfolio_return)
print("Annualized return\n", annual_return)

portfolio_risk = np.matmul((np.matmul(weights, covar_ror)), np.transpose(weights))
daily_portfolio_risk = np.sqrt(portfolio_risk)
annual_risk = np.sqrt(portfolio_risk*365)
print("Portfolio Risk\n", daily_portfolio_risk)
print("Annual Risk\n", annual_risk)

