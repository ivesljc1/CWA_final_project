import pandas as pd


def refactor_and_check(filename):
    # Read the CSV file
    data = pd.read_csv(filename)

    # Convert 'Date' to datetime and remove the time part
    data['Date'] = pd.to_datetime(data['Date']).dt.date

    # Create a date range that covers all dates in the dataset
    date_range = pd.date_range(start=data['Date'].min(), end=data['Date'].max(), freq='D')

    # Initialize a DataFrame to hold refactored data
    refactored_data = pd.DataFrame(index=date_range)

    # Rename 'Close' column to currency pair name extracted from the filename
    currency_pair = filename.replace('.csv', '')
    data.rename(columns={'Close': currency_pair}, inplace=True)

    # Set 'Date' as the index
    data.set_index('Date', inplace=True)

    # Join the data to the date range DataFrame
    refactored_data = refactored_data.join(data)

    # Find missing dates
    missing_dates = refactored_data[refactored_data[currency_pair].isnull()].index

    # Print out missing dates
    if not missing_dates.empty:
        print(f"Missing dates for {currency_pair}:")
        print(missing_dates.strftime('%Y-%m-%d').tolist())

    # Transpose the DataFrame for the desired output format
    refactored_data = refactored_data.transpose()

    # Return the refactored DataFrame
    return refactored_data


# List of filenames to be processed
filenames = ['NPRCNY.csv', 'NPRINR.csv', 'NPRUSD.csv']

# Process each file and store the refactored DataFrames in a dictionary
refactored_data_dict = {}
for filename in filenames:
    refactored_data = refactor_and_check(filename)
    refactored_data_dict[filename.replace('.csv', '')] = refactored_data

# Since we don't want to combine the data, we can now save each refactored DataFrame separately
for currency_pair, df in refactored_data_dict.items():
    output_filename = f'refactoredV1_{currency_pair}.csv'
    df.to_csv(output_filename)
    print(f'Refactored data saved to {output_filename}')
