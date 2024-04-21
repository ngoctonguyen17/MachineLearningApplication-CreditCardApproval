import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM,Dropout
from tensorflow.keras.callbacks import ModelCheckpoint,EarlyStopping


from Connectors.Connector import Connector


import warnings
warnings.filterwarnings("ignore")

import os

class StockPricePrediction:
    def __init__(self):
        super().__init__()

    def connectDatabase(self):
        self.connector.server = "localhost"
        self.connector.port = 3306
        self.connector.database = "stockdatabase"
        self.connector.username = "root"
        self.connector.password = "123456"
        self.connector.connect()

    def
