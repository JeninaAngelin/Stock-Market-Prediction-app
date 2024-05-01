import numpy as np
from tensorflow.keras.models import load_model
from datetime import datetime
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the pre-trained Bi-LSTM model
model = load_model('models/BILSTM_model.h5')

# Load the scaler used for training
scaler = MinMaxScaler(feature_range=(0,1))

def preprocess_input(datetime_str, stock_name, scaler):
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d')
    stock_code = hash(stock_name) % 1000
    datetime_features = [datetime_obj.year, datetime_obj.month, datetime_obj.day]
    input_data = np.array([datetime_features + [stock_code] * 97])
    return input_data

def predict_closing_price(datetime_str, stock_name):
    data_training = pd.read_csv(f"data/anomalies_{stock_name}.csv")
    data_training = data_training[['Close Price']]
    scaler.fit(data_training)
    input_data = preprocess_input(datetime_str, stock_name, scaler)
    predicted_price_scaled = model.predict(input_data)
    predicted_price = scaler.inverse_transform(predicted_price_scaled.reshape(-1, 1))
    return predicted_price[0][0]
