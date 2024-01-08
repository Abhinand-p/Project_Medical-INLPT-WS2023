import pandas as pd

input_csv_file = '../Data Analysis/All_Articles_PreProcessed.csv'


df = pd.read_csv(input_csv_file)
print("Column names:")
print(df.columns)
print("\nFirst few rows of the CSV file:")
print(df.head())
print("\nNumber of rows:")
print(len(df))

# Read the original CSV file
original_file_path = '../Data Analysis/All_Articles_PreProcessed.csv'
df = pd.read_csv(original_file_path)

# Extract the first 10 rows
first_10_rows = df.head(10)

# Specify the path for the new CSV file
new_file_path = 'First_10_Rows.csv'

# Save the first 10 rows to the new CSV file
first_10_rows.to_csv(new_file_path, index=False)

print(f"The new file '{new_file_path}' has been created with the first 10 rows.")
