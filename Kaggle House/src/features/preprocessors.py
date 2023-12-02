import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler

class DataPreprocessor:
  def __init__(self):
    self.one_hot_encoder = OneHotEncoder(handle_unknown='ignore')
    self.label_encoder = LabelEncoder()
    self.scaler = StandardScaler()

  def fit(self, df, one_hot_cols, label_cols):
    pass
