import numpy as np


def compute_cost_matrix(X, y, w, b, verbose=False):
    """
    Computes the gradient  for linear regression
    Args:
    X (ndarrey (m, n)): Data, m examples, n features
    y (ndarray (m, 1)): Labels or target values
    w (ndarray (n, 1)): Weights, model parameters
    b (scalar): Bias, model parameter
    verbose (bool): If true, prints tntermediate values f_wb
  Returns
    cost (scalar): Cost function for linear regression
    """
    m = X.shape[0]

    # calculate f_wb for all data
    f_wb = X @ w + b

    # calculate cost
    total_cost = (1/m) * np.sum((f_wb - y)**2)

    return total_cost
