import numpy as np


def compute_gradient_matrix(X, y, w, b):
    """
    Computes the gradient  for linear regression

    Args:
    X (ndarrey (m, n)): Data, m examples, n features
    y (ndarray (m, 1)): Labels or target values
    w (ndarray (n, 1)): Weights, model parameters
    b (scalar): Bias, model parameter
  Returns
    dj_dw (ndarray (n, 1)): Gradient of cost function w.r.t w
    dj_db (scalar): Gradient of ccost w.r.t the paramater b
    """

    m, n = X.shape
    f_wb = X @ w + b
    e = f_wb - y
    dj_dw = (1/m) * (X.T @ e)
    dj_db = (1/m) * np.sum(e)

    return dj_dw, dj_db
