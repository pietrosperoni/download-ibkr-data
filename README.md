# download-ibkr-data

# Interactive Brokers Option Data Fetcher

This Python script connects to the Interactive Brokers Trader Workstation (TWS) API to fetch option contract details for a specific ticker symbol and expiration date, and then saves the data to a CSV file.

## Features

- Retrieve option contract details (call and put) for a specified ticker symbol and expiration date
- Save the fetched data to a CSV file

## Requirements

- Python 3.6 or higher
- Interactive Brokers account and TWS software installed
- TWS API enabled with proper IP and port settings
- `ibapi` package installed (use `pip install ibapi` to install)

## Usage

1. Update the script with the desired ticker symbol and expiration date in the `main()` function:

contract.symbol = "AMZN"
contract.lastTradeDateOrContractMonth = "20240119"


2. Ensure that the TWS software is running and the API is enabled with the correct IP and port settings.

3. Run the script:

python fetch_option_data.py


4. The option contract details will be saved in a CSV file named `options_data.csv`.

## License

This project is licensed under the GNU Lesser General Public License (LGPL) v2.1. See the [LICENSE](LICENSE) file for details.
