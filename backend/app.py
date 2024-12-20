from flask import Flask, jsonify
from database import get_data_from_db, save_data_to_db
from models.prediction_model import predict_next_hour, train_model
import requests

app = Flask(__name__)

# Fetch live data from Binance API
BINANCE_API_URL = 'https://api.binance.com/api/v3/klines'

def get_live_data():
    params = {
        'symbol': 'BABYDOGEUSDT',
        'interval': '1m',
        'limit': 1000  # Get the last 1000 1-minute candles
    }
    response = requests.get(BINANCE_API_URL, params=params)
    data = response.json()
    return data

@app.route('/update_data', methods=['GET'])
def update_data():
    # Get live data from Binance API
    data = get_live_data()

    # Save the data to DB
    save_data_to_db(data)

    # Retrain models periodically (every 10 minutes or based on your choice)
    train_model()

    return jsonify({"status": "success", "data": data}), 200

@app.route('/predict', methods=['GET'])
def predict():
    prediction = predict_next_hour()  # Use the trained model to make predictions
    return jsonify({"prediction": prediction}), 200

@app.route('/api/crypto_data', methods=['GET'])
def get_crypto_data():
    data = get_data_from_db()
    return jsonify(data.to_dict(orient='records')), 200

if __name__ == '__main__':
    app.run(debug=True)
