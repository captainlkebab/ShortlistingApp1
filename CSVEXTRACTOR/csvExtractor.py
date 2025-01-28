import pandas as pd
import os

# Read the CSV file into a DataFrame
try:
    df = pd.read_csv('resumesamples.csv')
except FileNotFoundError:
    print("The file 'resumesamples.csv' was not found.")
    exit()

# Print the first few rows of the DataFrame
print("First few rows of the DataFrame:")
print(df.head())

# Check if the 'Category' column exists
if 'Category' not in df.columns:
    print("The column 'Category' does not exist in the CSV file.")
    exit()

# Define the directory for the new CSV files
output_dir = r'C:\Users\samil\Documents\Python Project Folder\SemesterProject2\CSV'
os.makedirs(output_dir, exist_ok=True)

# Get unique categories
unique_categories = df['Category'].unique()

# Iterate over unique categories and save to CSV if more than 20 entries
for category in unique_categories:
    df_filtered = df[df['Category'] == category]
    if len(df_filtered) > 10:
        output_file = os.path.join(output_dir, f'{category}.csv')
        df_filtered.to_csv(output_file, index=False)
        print(f'Saved {category} category with {len(df_filtered)} entries to {output_file}')