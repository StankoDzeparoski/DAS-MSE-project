from flask import Flask, jsonify
from flask_cors import CORS
import filterOne
import filterTwo
import filterThree
import sqlite3
import time

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

DATABASE = "mse_data.db"

def initialize_database():
    """Initialize the database and create the required table if it doesn't exist."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mse_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker_code TEXT NOT NULL,
            date TEXT NOT NULL,
            last_price REAL,
            max_price REAL,
            min_price REAL,
            volume REAL,
            UNIQUE (ticker_code, date) ON CONFLICT REPLACE
        )
    """)
    connection.commit()
    connection.close()

@app.route('/getDataBase', methods=['GET'])
def get_database():
    """Execute the entire pipeline and return the database."""
    try:
        start_time = time.time()

        # Step 1: Initialize the database
        initialize_database()

        # Step 2: Fetch issuer codes and save to the database
        tickers = filterOne.getTickers()
        filterOne.save_tickers_to_db(tickers, DATABASE)

        # Step 3: Process data for each issuer
        filterTwo.process_data_with_threads(tickers)

        # Step 4: Finalize and verify the data
        filterThree.update_data()

        end_time = time.time()

        return jsonify({
            "message": "Pipeline executed successfully",
            "execution_time": f"{end_time - start_time:.2f} seconds",
            "database": DATABASE
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
