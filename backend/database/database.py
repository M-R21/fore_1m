from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime

DATABASE_URL = 'sqlite:///crypto_data.db'  # Use PostgreSQL or MySQL in production

# Setup database connection
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def save_data_to_db(data):
    # Convert data to DataFrame and save it to DB
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    df.to_sql('crypto_data', con=engine, if_exists='append', index=False)

def get_data_from_db():
    # Retrieve last X entries from the database
    query = "SELECT * FROM crypto_data ORDER BY timestamp DESC LIMIT 1000"
    df = pd.read_sql(query, con=engine)
    return df
