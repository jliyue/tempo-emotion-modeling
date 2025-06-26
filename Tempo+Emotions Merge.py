import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog

def load_file(title, filetypes):
    """Open a file dialog and return the selected file path."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    return file_path

def merge_audio_data():
    # Load datasets using file dialog
    excel_file = load_file("Select Tempo Analysis File", [("Excel files", "*.xlsx")])
    csv_file = load_file("Select Merged CSV File", [("CSV files", "*.csv")])
    
    # Load datasets
    df1 = pd.read_excel(excel_file)
    df2 = pd.read_csv(csv_file)
    
    # Standardize timestamp format in df1 (Excel file)
    df1["Duration (hh:mm:ss.ms)"] = df1["Duration (hh:mm:ss.ms)"].str.replace(".", ":", regex=False, n=2)
    df1["Duration (hh:mm:ss.ms)"] = df1["Duration (hh:mm:ss.ms)"].apply(
        lambda x: f"{x[:2]}:{x[3:5]}:{x[6:8]}.{x[9:]}" if len(x) > 8 else x
    )
    
    # Convert timestamps to timedelta
    df1["Duration (hh:mm:ss.ms)"] = pd.to_timedelta(df1["Duration (hh:mm:ss.ms)"])
    df2["Duration (hh:mm:ss.ms)"] = pd.to_timedelta(df2["Duration (hh:mm:ss.ms)"])
    
    # Merge using nearest timestamp match
    merged_df = pd.merge_asof(
        df2.sort_values("Duration (hh:mm:ss.ms)"), 
        df1.sort_values("Duration (hh:mm:ss.ms)"), 
        on="Duration (hh:mm:ss.ms)", 
        direction='nearest'
    )
    
    # Calculate additional metrics
    window_size = 3  # Adjust this based on preference
    merged_df["Tempo Std Dev"] = merged_df["Tempo (bpm)"].rolling(window=window_size).std()
    merged_df["Mean BPM"] = merged_df["Tempo (bpm)"].rolling(window=window_size).mean()
    merged_df["Coefficient of Variation"] = merged_df["Tempo (bpm)"].pct_change()
    merged_df["Rolling Coefficient of Variation"] = (merged_df["Tempo Std Dev"] / merged_df["Mean BPM"]).rolling(window=window_size).mean()
    merged_df["Instantaneous Rate of Tempo Change"] = merged_df["Tempo (bpm)"].diff() / merged_df["Duration (hh:mm:ss.ms)"].diff().dt.total_seconds()
    
    # Define output path based on input filename number after the underscore
    output_dir = "/Users/joyceliyue/Downloads/thesis files/Data Analysis/MERGE/Merged w Tempo and Calculations"
    os.makedirs(output_dir, exist_ok=True)
    csv_filename_number = os.path.basename(csv_file).split('_')[-1].split('.')[0]  # Extract the number after the underscore
    output_file = os.path.join(output_dir, f"Merged w Tempo ({csv_filename_number}).csv")
    
    # Save the result
    merged_df.to_csv(output_file, index=False)
    print(f"Processed file saved as: {output_file}")

# Run the merge function
merge_audio_data()
