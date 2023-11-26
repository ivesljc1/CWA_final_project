import pandas as pd

# Load the CSV file into a DataFrame
file_path = '../../RawData/vegePrice.csv'
data = pd.read_csv(file_path)

# Grouping the data by the 'Commodity' column
grouped_data = data.groupby('Commodity')

# Returning the number of unique groups (commodities) formed
print(f"Total Group: {len(grouped_data)}")

# Initialize an empty DataFrame to hold the concatenated data
concatenated_data = pd.DataFrame()

# Concatenate the groups
for name, group in grouped_data:
    concatenated_data = pd.concat([concatenated_data, group])

#Find the max and min dates
min_date = concatenated_data['Date'].min()
max_date = concatenated_data['Date'].max()

# Create a date range
date_range = pd.date_range(start=min_date, end=max_date)

# Pivoting the data
# 'Commodity' and 'Unit' will be the leading columns, followed by dates in the date range as columns
# Each cell under the dates will contain the 'Average' price for the commodity on that date
pivoted_data = concatenated_data.pivot_table(
    index=['Commodity', 'Unit'],
    columns='Date',
    values='Average',
    aggfunc='mean'
)

# Resetting the index to turn multi-index into columns
pivoted_data.reset_index(inplace=True)

pivoted_data = pivoted_data.fillna('NA')




###########
# Load the category data
category_data_path = '../../RawData/category.csv'
category_data = pd.read_csv(category_data_path, header=None)
category_data.columns = ['Commodity', 'Category']

# Standardizing 'Commodity' names in both dataframes for accurate merging
pivoted_data['Commodity'] = pivoted_data['Commodity'].str.lower()
category_data['Commodity'] = category_data['Commodity'].str.lower().str.strip()

# Merging the category data with the pivoted data
merged_data = pd.merge(pivoted_data, category_data, on='Commodity', how='left')

# Reorder the columns to place 'Category' as the third column
cols = merged_data.columns.tolist()
cols.insert(2, cols.pop(cols.index('Category')))
merged_data = merged_data[cols]

# Replace NaN with 'NA' in 'Category' if any
merged_data['Category'].fillna(0, inplace=True)

# Save the merged and reordered data to a CSV file
final_data_path = '../../ProcessedData/final_vegePrice0.csv'
merged_data.to_csv(final_data_path, index=False)