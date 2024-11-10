import filterOne
import filterTwo
import filterThree
import time


if __name__ == '__main__':
    startTime = time.time()
    # Filter One Execute
    filterOne.processTickerTagData("ticker_codes.csv")
    # # Filter Two Execute with threads test
    ticker_codes = filterTwo.fetch_issuer_codes()
    filterTwo.process_data_with_threading(ticker_codes)
    # Filter Three Execute
    filterThree.update_data_with_formatting()
    endTime = time.time()
    print(f'Execution time: {endTime - startTime}')