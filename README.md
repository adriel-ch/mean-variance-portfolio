# mean-variance-portfolio

This python script calculates a vector of optimal weights that can be applied to assets in a portfolio that will obtain a desired return with the corresponding risk taken.

The variables below are required:

`start_date = dt.datetime(2023, 5, 1)` => Start date of the data sample | YYYY, M, D

`end_date = dt.datetime(2023, 6, 1)` => End date of the data sample | YYYY, M, D

`symbol_list = ["BTC-USD", "ETH-USD", "LTC-USD"]` => List of ticker symbols to be considered in the portfolio

`data_period = ["60min"]` => Data period interval

## Description

The script will pull data from HuoBi's publicly available data on perpetual futures prices for the assets listed in the symbol_list and appends the closing price for all assets into a DataFrame.

It will then perform mean variance optimisation to obtain the weights vector containing the optimal weights with their corresponding risk and return values.

The Efficient Frontier plot will also be generated.

The weights vector will be saved in: `./app/output/weights/`

The efficient frontier plot will be saved in: `./app/output/plots/`

## Mean Variance Optimisation

### Rate of Return
---

We first obtain the rate of return of the assets in question. The code block below calculates the hourly return for each of the assets at each hour for the data sample set.

```python
def rate_of_return(df: pd.DataFrame) -> np.ndarray
    closing_price_array = df.to_numpy()
    rows, cols = closing_price_array.shape
    array_returns = np.zeros([rows, cols])
    for j in range(cols):
        for i in range(rows):
            try:
                array_returns[i, j] = ((closing_price_array[i + 1, j] - closing_price_array[i, j]) / closing_price_array[i, j]) * 100
            except IndexError:
                array_returns[i, j] = ((closing_price_array[i, j] - closing_price_array[i, j]) / closing_price_array[i, j]) * 100
    return array_returns
```

### Mean Returns
---

The rate of return values are then used to obtain the mean returns of the assets.

`mean_ror = np.mean(ror, axis=0)`

### Covariance of Returns
---

The variance-covariance matrix of returns.

`covar_ror = np.cov(ror, rowvar=False)`

### Maximal Returns
---

To get the asset weights that give the maximal returns we use scipy.linprog to solve.

```python
def maximize_returns(mean_return: np.ndarray, portfolio_size: int) -> scp.OptimizeResult:
    """Function to obtain weights to get maximal return in the portfolio

    Parameters
    ----------
    mean_returns : Input 1-D array of mean return of assets in the portfolio
    portfolio_size : number of assets in the portfolio
    """
    c = (np.multiply(-1, mean_return))
    A = np.ones([portfolio_size, 1]).T
    b = [1]
    res = scp.linprog(c,
                      A_ub = A,
                      b_ub = b,
                      bounds = (0,1),
                      method = 'highs'
                      )
    
    return res
```

The weights obtained are then used to calculate the maximal return.

```python
max_returns = maximize_returns(mean_ror, cols)
max_returns_weight = max_returns.x
max_expect_portfolio_ror = np.matmul(mean_ror.T, max_returns_weight)
```

### Minimise Risk
---

This function returns the asset weights that provide the lowest level of risk and its corresponding return.

```python
def minimize_risk(covar_returns: np.ndarray, portfolio_size: int) -> scp.OptimizeResult:
    """Function obtains weights to get the return for the minimal risk in the portfolio

    Parameters
    ----------
    covar_returns : Input covariance matrix of assets
    portfolio_size : number of assets in the portfolio
    """
    def f(x, covar_returns: np.ndarray):
        """The non-linear objective function."""
        func = np.sqrt(np.matmul(np.matmul(x, covar_returns), x.T))
        return func

    def constraintEq(x):
        """Fully invested weights contraint i.e. Sum of all weights = 1"""
        A = np.ones(x.shape)
        b = 1
        constraintVal = np.matmul(A, x.T) - b 
        return constraintVal
    
    xinit = np.repeat(0.1, portfolio_size) # array of initial guess values of weights
    cons = ({'type': 'eq',
             'fun': constraintEq})
    lb = 0
    ub = 1
    bnds = tuple([(lb, ub) for x in xinit])

    opt = scp.minimize (f,
                        x0 = xinit,
                        args = (covar_returns),
                        bounds = bnds,
                        constraints = cons,
                        tol = 10**-3
                        )
    
    return opt
```

The weights obtained are then used to calculate the return that provides minimal risk.

```python
min_risk_return = minimize_risk(covar_ror, cols)
min_risk_return_weight = min_risk_return.x
min_risk_expected_portfolio_ror = np.matmul(mean_ror.T, min_risk_return_weight)
```

### Optimal Weights for Minimal risk and Maximal Returns
---

The optimal weights are obtained by plugging this function with varying values of R(returns)

```python
def minimize_risk_constr(mean_returns: np.ndarray,
                         covar_returns: np.ndarray,
                         portfolio_size: int,
                         R: float
                         ) -> scp.OptimizeResult:
    """Function obtains optimal weights sets given min_risk and max_return constraints

    Parameters
    ----------
    mean_returns : Input 1-D array of mean return of assets in the portfolio
    covar_returns : Input covariance matrix of assets
    portfolio_size : Number of assets in the portfolio
    R : Input return value
    """
    def f(x, covar_returns):
        """The non-linear objective function."""
        func = np.sqrt(np.matmul(np.matmul(x, covar_returns ), x.T))
        return func

    def constraintEq(x):
        """Fully invested weights contraint i.e. Sum of all weights = 1"""
        AEq = np.ones(x.shape)
        bEq = 1
        EqconstraintVal = np.matmul(AEq, x.T) - bEq 
        return EqconstraintVal
    
    def constraintIneq(x, mean_returns, R):
        """Sum of weighted returns <= return R from input"""
        AIneq = np.array(mean_returns)
        bIneq = R
        IneqconstraintVal = np.matmul(AIneq, x.T) - bIneq
        return IneqconstraintVal
    
    xinit = np.repeat(0.1, portfolio_size) # array of initial values of weights
    cons = ({'type': 'eq', 'fun': constraintEq},
            {'type': 'ineq', 'fun': constraintIneq, 'args': (mean_returns, R)})
    lb = 0
    ub = 1
    bnds = tuple([(lb, ub) for x in xinit])

    opt = scp.minimize(f,
                       args = (covar_returns),
                       method ='trust-constr',
                       x0 = xinit,
                       bounds = bnds,
                       constraints = cons,
                       tol = 10**-3
                       )
    
    return opt
```

```python
# Compute efficient set for the maximum return and minimum risk portfolios
increment = 0.001
low = min_risk_expected_portfolio_ror
high = max_expect_portfolio_ror

# Initialize optimal weight set and risk-return point set
x_optimal = [] # optimal weights set
min_risk_point = []
expected_portfolio_return_point = []

while (low < high):
    result = minimize_risk_constr(mean_ror, covar_ror, cols, low)
    x_optimal.append(result.x)
    expected_portfolio_return_point.append(low)
    low += increment

x_optimal_array = np.array(x_optimal) # optimal weights set
min_risk_point = np.diagonal(np.matmul((np.matmul(x_optimal_array, covar_ror)),
                                        np.transpose(x_optimal_array)))
risk_point = np.sqrt(min_risk_point * 365) # annualised
return_point = 365 * np.array(expected_portfolio_return_point) # annualised
```

### Efficient Frontier
---

Utilising the risk and return of the various sets of weights, the efficient frontier can be plotted.

```python
def eff_frontier(risk_point: np.ndarray,
                 return_point: np.ndarray,
                 save_plot: bool = False,
                 filepath: str = ""
                 ) -> None:
    no_points = risk_point.size

    colours = "red"
    area = np.pi*3

    plt.title(f'Efficient Frontier for selected portfolio')
    plt.xlabel('Annualized Risk(%)')
    plt.ylabel('Annualized Expected Portfolio Return(%)' )
    plt.scatter(risk_point, return_point, s=area, c=colours, alpha =0.5)
    plt.show()
    return
```

# References

https://github.com/hbdmapi/huobi_public_data/tree/master

