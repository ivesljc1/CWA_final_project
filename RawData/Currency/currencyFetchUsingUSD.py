import yfinance as yf
import pandas as pd
from datetime import datetime
from tqdm import tqdm

# Define the currency pairs and date range
currency_pairs = ['USDNPR=X', 'USDINR=X', 'USDCNY=X']
start_date = '2013-06-16'
end_date = '2021-05-13'

# Initialize a DataFrame to store the data
exchange_rates = pd.DataFrame()

# Progress bar setup
pbar = tqdm(total=len(currency_pairs), desc="Fetching Data", unit="pair")

# Fetch data for each currency pair
for pair in currency_pairs:
    data = yf.download(pair, start=start_date, end=end_date)
    #data['Average'] = (data['High'] + data['Low']) / 2
    exchange_rates[pair] = data['Close']
    pbar.update(1)

pbar.close()

# Calculate NPR to INR and NPR to CNY using USD as base
exchange_rates['NPRINR'] = exchange_rates['USDINR=X'] / exchange_rates['USDNPR=X']
exchange_rates['NPRCNY'] = exchange_rates['USDCNY=X'] / exchange_rates['USDNPR=X']

# Transpose the DataFrame
exchange_rates = exchange_rates.transpose()

# Check for missing data
missing_data = exchange_rates.isnull().sum(axis=1)
total_days = len(exchange_rates.columns)
missing_percentage = (missing_data / total_days) * 100

# Print fetch summary
print("\nFetch Summary:")
for pair, missing in missing_data.items():
    print(f"{pair} - Missing data: {missing} days ({missing_percentage[pair]:.2f}% missing)")
    if missing > 0:
        missing_dates = exchange_rates.columns[exchange_rates.loc[pair].isnull()]
        print(f"Missing Dates for {pair}: {list(missing_dates)}")

# Save the DataFrame to a CSV file
exchange_rates.to_csv('currency_exchange_rates_USD.csv')
print("\nData fetched and saved to currency_exchange_rates.csv")
