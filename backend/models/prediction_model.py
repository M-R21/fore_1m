import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from database import get_data_from_db

def prepare_data():
    df = get_data_from_db()
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[['close']])
    X, y = [], []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i-60:i, 0])
        y.append(scaled_data[i, 0])
    X = np.array(X)
    y = np.array(y)
    return X, y, scaler

def build_model(input_shape):
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(units=50, return_sequences=True, input_shape=input_shape),
        tf.keras.layers.LSTM(units=50, return_sequences=False),
        tf.keras.layers.Dense(units=25),
        tf.keras.layers.Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model():
    X, y, scaler = prepare_data()
    X_train = np.reshape(X, (X.shape[0], X.shape[1], 1))
    model = build_model((X_train.shape[1], 1))
    model.fit(X_train, y, batch_size=1, epochs=1)
    model.save("crypto_predictor_model.h5")

def predict_next_hour():
    model = tf.keras.models.load_model("crypto_predictor_model.h5")
    X, _, scaler = prepare_data()
    last_60_data = np.reshape(X[-1], (1, X.shape[1], 1))
    prediction = model.predict(last_60_data)
    predicted_price = scaler.inverse_transform(prediction)
    return "Buy" if predicted_price > X[-1][-1] else "Sell"
