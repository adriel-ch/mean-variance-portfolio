import datetime as dt

import numpy as np
import pandas as pd
import scipy.optimize as scp
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True) # suppress sci notation

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
                array_returns[i, j] = ((closing_price_array[i + 1, j] - closing_price_array[i, j])
                                       / closing_price_array[i, j]) * 100
            except IndexError:
                array_returns[i, j] = ((closing_price_array[i, j] - closing_price_array[i, j])
                                       / closing_price_array[i, j]) * 100
    
    # print(array_returns)
    return array_returns

def maximize_returns(mean_return: np.ndarray, portfolio_size: int) -> scp.OptimizeResult:
    """Function to obtain weights to get maximal return in the portfolio

    Parameters
    ----------
    mean_returns : Input 1-D array of mean return of assets in the portfolio
    portfolio_size : number of assets in the portfolio
    """
    c = (np.multiply(-1, mean_return)) # not sure what the -1 is for
    # print("mean return * -1\n", c)
    A = np.ones([portfolio_size, 1]).T
    # print("A_ub * x <= bub\n", A)
    b = [1]
    # print("b_ub value\n", b)
    res = scp.linprog(c,
                      A_ub = A,
                      b_ub = b,
                      bounds = (0,1),
                      method = 'highs'
                      )
    
    return res

def minimize_risk(covar_returns: np.ndarray, portfolio_size: int) -> scp.OptimizeResult:
    """Function obtains weights to get the return for the minimal risk in the portfolio

    Parameters
    ----------
    covar_returns : Input covariance matrix of assets
    portfolio_size : number of assets in the portfolio
    """
    def f(x, covar_returns: np.ndarray):
        """The non-linear objective function."""
        # func = np.matmul(np.matmul(x, covar_returns), x.T) # need sqrt?
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
        # func = np.matmul(np.matmul(x, covar_returns ), x.T) # missing sqrt?
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

def mean_variance_opt(df: pd.DataFrame, symbolList: list):
    ror = rate_of_return(df)
    print("Rate of eturn for hourly period\n", ror, "\n")

    # mean returns
    mean_ror = np.mean(ror, axis=0)
    print("Mean ROR\n", mean_ror, "\n")

    # Mean return of the entire portfolio per interval (hr)
    # Equally weighted cotribution to the mean
    portfolio_ror = np.mean(ror, axis=1) # or market ror
    # print("Portfolio ROR\n", portfolio_ror)

    # Covariance matrix of the assets within ror against each other
    covar_ror = np.cov(ror, rowvar=False) # rowvar = False because variables(assets) are in the cols
    print("Covariance Matrix of assets within portfolio\n", covar_ror, "\n")

    # Compute betas of assets in the portfolio
    rows, cols = ror.shape
    beta = []
    portfolio_ror_variance = np.var(portfolio_ror, ddof = 1)
    for i in range(cols):
        # covar_matrix = np.cov(portfolio_ror[:, 0], ror[:, i])
        covar_matrix = np.cov(portfolio_ror, ror[:, i])
        # print(f"Covar Matrix for asset: {symbol_list[i]} with Portfolio mean ROR\n", covar_matrix)
        covar  = covar_matrix[1, 0]
        # print("Covar Value: ", covar) 
        beta.append(covar / portfolio_ror_variance)

    print("Beta Values: ", beta, "\n")

    # weights = np.array([0.33333, 0.33333, 0.33333])

    # portfolio_return = np.matmul(np.array(mean_ror), weights.T)
    # print(portfolio_return)
    # annual_return = 365 * np.array(portfolio_return)
    # print("Portfolio Return\n", portfolio_return)
    # print("Annualized return\n", annual_return)

    # portfolio_risk = np.matmul((np.matmul(weights, covar_ror)), np.transpose(weights))
    # daily_portfolio_risk = np.sqrt(portfolio_risk)
    # annual_risk = np.sqrt(portfolio_risk*365)
    # print("Portfolio Risk\n", daily_portfolio_risk)
    # print("Annual Risk\n", annual_risk)

    max_returns = maximize_returns(mean_ror, cols)
    max_returns_weight = max_returns.x
    max_expect_portfolio_ror = np.matmul(mean_ror.T, max_returns_weight)
    print("Max expected portfolio return\nR_max_rt: ", max_expect_portfolio_ror, "\n")

    min_risk_return = minimize_risk(covar_ror, cols)
    min_risk_return_weight = min_risk_return.x
    min_risk_expected_portfolio_ror = np.matmul(mean_ror.T, min_risk_return_weight)
    print("Min risk expected portfolio return\nR_min_risk: ", min_risk_expected_portfolio_ror, "\n")

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

    print("Optimal weights array\n", x_optimal_array, "\n")
    print("Annual risk | Annual return\n", np.c_[risk_point, return_point], "\n")
    # print("risk / return\n", np.c_[min_risk_point, expected_portfolio_return_point])

    return x_optimal_array, risk_point, return_point

def eff_frontier(risk_point: np.ndarray,
                 return_point: np.ndarray,
                 save_plot: bool = False,
                 save_output: str = ""
                 ) -> None:
    no_points = risk_point.size

    colours = "blue"
    area = np.pi*3

    plt.title(f'Efficient Frontier for selected portfolio')
    plt.xlabel('Annualized Risk(%)')
    plt.ylabel('Annualized Expected Portfolio Return(%)' )
    plt.scatter(risk_point, return_point, s=area, c=colours, alpha =0.5)

    if save_plot == True:
        plt.savefig(save_output)
    
    plt.show()
    plt.close()
    
    return
