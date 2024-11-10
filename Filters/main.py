from datetime import datetime

import filterOne
import filterTwo
import filterThree
import time


if __name__ == '__main__':
    startTime = time.time()
    # Filter One Execute
    filterOne.processTickerTagData("ticker_codes.csv")
    # Filter Two Execute
    issuer_codes = filterTwo.fetch_issuer_codes()
    for ticker_code in issuer_codes:
        filterTwo.process_data(ticker_code)
    # Filter Three Execute
    filterThree.update_data_with_formatting()
    endTime = time.time()
    print(f'Execution time: {endTime - startTime}')