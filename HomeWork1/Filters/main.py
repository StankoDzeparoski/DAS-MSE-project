import filterOne
import filterTwo
import filterThree
import time
import sqlite3


if __name__ == '__main__':
    start_time = time.time()

    connection = sqlite3.connect("mse_data.db")
    cursor = connection.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS "mse_data.db" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker_code TEXT NOT NULL,
                date TEXT NOT NULL,
                lastPrice REAL,
                maxPrice REAL,
                minPrice REAL,
                volume REAL,
                UNIQUE (ticker_code, date) ON CONFLICT REPLACE
            )
        """)
    connection.commit()
    connection.close()

    # Fetch issuer codes using Filter One and save them to the database
    print("Fetching issuer codes...")
    tickers = filterOne.getTickers()
    filterOne.save_tickers_to_db(tickers, "mse_tickers.db")
    print(f"Saved {len(tickers)} issuer codes to the database.")

    # Process each issuer using Filter Two
    print("Processing data for each issuer...")
    filterTwo.process_data_with_threads(tickers)

    # Format and verify the data using Filter Three
    print("Finalizing and verifying data...")
    filterThree.fetch_all_data_from_db("mse_data.db")

    end_time = time.time()
    print(f"Execution completed in {end_time - start_time:.2f} seconds.")