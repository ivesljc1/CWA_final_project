import pandas as pd


def process_currency_data(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path, index_col=0)

    # Transpose data to have dates as rows for filling purposes
    data = data.transpose()

    # Fill missing values with the average of neighboring available data
    data_filled = data.interpolate(method='linear', axis=0, limit_direction='both')

    # Transpose data back to have dates as columns and currency pairs as rows
    data_processed = data_filled.transpose()

    # Save the processed data into a new CSV file
    processed_file_path = file_path.replace('_unfilled.csv', '_filled.csv')
    data_processed.to_csv(processed_file_path)

    return processed_file_path


# Specify the path to your CSV file
file_path = 'currencies_unfilled.csv'  # Update to the path where your file is located

# Process the currency data and fill missing values
processed_file_path = process_currency_data(file_path)

# Output the path to the processed file
print(f"Processed data saved to: {processed_file_path}")
