import os
import pandas as pd

# Set your input folder path
input_folder = ''  # Replace with your folder containing CSV files
output_file = 'combined_output.csv'  # Output filename

# List to hold data from each CSV
combined_data = []

# Loop through each CSV file in the folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder, filename)
        try:
            df = pd.read_csv(file_path)
            df['Source_File'] = filename  # Optional: Add a column to keep track of source file
            combined_data.append(df)
            print(f"Added: {filename}")
        except Exception as e:
            print(f"Skipped {filename}: {e}")

# Concatenate all DataFrames
if combined_data:
    combined_df = pd.concat(combined_data, ignore_index=True)
    combined_df.to_csv(output_file, index=False)
    print(f"\n✅ All files combined and saved to: {output_file}")
else:
    print("⚠️ No CSV files found or processed.")
