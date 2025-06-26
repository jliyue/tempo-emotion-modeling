import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Set your folder paths
input_folder = ''    # Replace with your input folder of merged files 
output_folder = ''  # Replace with your output folder, make sure to label correctly for Normalized. 

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each CSV in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder, filename)
        df = pd.read_csv(file_path)

        # Convert non-numeric to NaN
        df['Rate_of_Tempo_Change'] = pd.to_numeric(df['Rate_of_Tempo_Change'], errors='coerce')
        df['Tempo_Change_Percentage'] = pd.to_numeric(df['Tempo_Change_Percentage'], errors='coerce')

        # Drop rows with NaNs in relevant columns
        df_clean = df.dropna(subset=['Rate_of_Tempo_Change', 'Tempo_Change_Percentage'])

        # Normalize
        scaler = MinMaxScaler()
        df_clean[['Normalized_Rate_of_Tempo_Change', 'Normalized_Tempo_Change_Percentage']] = scaler.fit_transform(
            df_clean[['Rate_of_Tempo_Change', 'Tempo_Change_Percentage']]
        )

        # Save to output folder
        output_path = os.path.join(output_folder, filename)
        df_clean.to_csv(output_path, index=False)
        print(f"Processed and saved: {output_path}")

print("✅ All files processed and saved.")
