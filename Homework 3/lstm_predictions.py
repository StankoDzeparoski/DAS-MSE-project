from keras.src.models import Sequential
from keras.src.layers import LSTM, Dense, Dropout
import sqlite3
import pandas as pd
import numpy as np
from keras.src.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def extract_data(database_path, query):
    """Extract data from the SQLite database."""
    conn = sqlite3.connect(database_path)
    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()
    return df

def preprocess_data(df):
    """Preprocess the stock data."""
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    scaler = MinMaxScaler(feature_range=(0, 1))
    df['last_price_scaled'] = scaler.fit_transform(df[['last_price']])
    return df, scaler

def create_sequences(data, target_col, sequence_length=10):
    """Create sequences and targets for LSTM."""
    sequences = []
    targets = []
    for i in range(len(data) - sequence_length):
        seq = data.iloc[i:i + sequence_length][target_col].values
        target = data.iloc[i + sequence_length][target_col]
        sequences.append(seq)
        targets.append(target)
    return np.array(sequences), np.array(targets)

def build_lstm_model(input_shape):
    """Build and compile the LSTM model."""
    model = Sequential([
        LSTM(50, activation='relu', return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(50, activation='relu'),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return model

def plot_predictions(y_test_actual, predicted_prices):
    """Plot actual vs predicted stock prices."""
    plt.plot(y_test_actual, color='blue', label='Actual Prices')
    plt.plot(predicted_prices, color='red', label='Predicted Prices')
    plt.title('Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

def main():
    # Step 1: Extract Data
    database_path = "mse_data.db"
    query = "SELECT ticker_code, date, last_price, max_price, min_price, volume FROM mse_data"
    df = extract_data(database_path, query)

    # Step 2: Preprocess Data
    df, scaler = preprocess_data(df)
    target_col = 'last_price_scaled'
    sequence_length = 10

    # Step 3: Create Sequences
    X, y = create_sequences(df, target_col, sequence_length=sequence_length)

    # Reshape X for LSTM (samples, time steps, features)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)

    # Step 4: Build and Train Model
    model = build_lstm_model(input_shape=(X_train.shape[1], 1))
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

    # Step 5: Make Predictions
    predicted_prices = model.predict(X_test)
    y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))
    predicted_prices = scaler.inverse_transform(predicted_prices)

    # Step 6: Evaluate Model
    mse = mean_squared_error(y_test_actual, predicted_prices)
    print(f"Mean Squared Error (MSE): {mse:.2f}")

    # Step 7: Plot Results
    plot_predictions(y_test_actual, predicted_prices)

    # Step 8: Predict Future Prices
    def predict_future(steps):
        future_predictions = []
        last_sequence = X_test[-1]  # Start from the last test sequence
        for _ in range(steps):
            next_prediction = model.predict(last_sequence[np.newaxis, :, :])[0, 0]
            future_predictions.append(next_prediction)
            last_sequence = np.append(last_sequence[1:], [[next_prediction]], axis=0)
        return scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

    future_predictions = predict_future(1)
    print(f"Predicted next day stock price: {future_predictions[0][0]:.2f}")

if __name__ == "__main__":
    main()
