import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Preset root directory
ROOT_DIRECTORY = "" #This folder is the folder where you have stored the emotion log csv data. 
OUTPUT_DIRECTORY = "" #Create a folder for your output. 

def select_folder():
    """Opens a file dialog allowing the user to select a folder containing CSV files."""
    root = tk.Tk()
    root.withdraw()  # Hide main window

    # Ask user to select a folder, opening at the preset directory
    selected_folder = filedialog.askdirectory(initialdir=ROOT_DIRECTORY, title="Select Folder with CSV Files")
    
    if selected_folder:
        process_files(selected_folder)

def process_files(directory):
    """Processes CSV files in the selected folder and merges them into a single file."""
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)  # Ensure output directory exists

    # Get CSV files
    csv_files = sorted([f for f in os.listdir(directory) if f.endswith(".csv")])

    if not csv_files:
        print("No CSV files found in the selected folder.")
        return

    # Extract the number before the dot from the first filename
    file_number = csv_files[0].split(".")[0]  # Extracts number before ".csv"

    # Merge CSV files
    df_list = []
    for file in csv_files:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)
        df.insert(1, "Trial ID", file)  # Rename "Filename" column to "Trial ID"
        df_list.append(df)

    merged_df = pd.concat(df_list, ignore_index=True)

    # Define output file name and path
    output_filename = f"Merged_{file_number}.csv"
    output_path = os.path.join(OUTPUT_DIRECTORY, output_filename)

    # Save merged file
    merged_df.to_csv(output_path, index=False)

    print(f"Merged file saved as: {output_path}")

# Run the folder selection function
select_folder()
