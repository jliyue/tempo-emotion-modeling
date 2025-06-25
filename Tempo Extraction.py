import librosa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from io import BytesIO
from openpyxl.utils.dataframe import dataframe_to_rows
import os

input_folder = ""  # Check the exact folder name of your files with audio files


output_folder = output_folder = "" # Update with your output folder path

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Get all .mp3 files in the input folder
audio_files = [f for f in os.listdir(input_folder) if f.endswith(".mp3")]

for audio_file in audio_files:
    file_path = os.path.join(input_folder, audio_file)
    file_name = os.path.basename(audio_file).replace('.mp3', '')  # Extract file name without extension

    try:
        # Load audio file
        y, sr = librosa.load(file_path)

        # Tempo extraction parameters
        hop_length = 512
        frame_length = 2048
        segment_length = 1  # In seconds
        n_segments = int(librosa.get_duration(y=y, sr=sr) / segment_length)

        tempos = []
        timestamps = []
        file_names = []

        # Extract tempo per segment
        for i in range(n_segments):
            start_sample = i * segment_length * sr
            end_sample = (i + 1) * segment_length * sr
            segment = y[start_sample:end_sample]

            onset_env_segment = librosa.onset.onset_strength(y=segment, sr=sr)

            if len(onset_env_segment) > 0:
                tempo_segment = librosa.beat.tempo(onset_envelope=onset_env_segment, sr=sr)
                tempos.append(tempo_segment[0])
            else:
                tempos.append(0)  # Assign 0 BPM if no tempo detected

            # Calculate timestamp (hh:mm:ss:ms format)
            total_milliseconds = int(i * segment_length * 1000)  # Convert seconds to ms
            hours = total_milliseconds // (3600 * 1000)
            minutes = (total_milliseconds % (3600 * 1000)) // (60 * 1000)
            seconds = (total_milliseconds % (60 * 1000)) // 1000
            milliseconds = total_milliseconds % 1000

            timestamp = f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
            timestamps.append(timestamp)
            file_names.append(file_name)  # Store the file name for each row

        # Create DataFrame for segment-wise tempo analysis
        df = pd.DataFrame({
            'Song': file_names,
            'Duration (hh:mm:ss.ms)': timestamps,
            'Tempo (bpm)': tempos
        })

        # Calculate statistics
        mean_tempo = np.mean(tempos)
        std_tempo = np.std(tempos)
        cv_tempo = (std_tempo / mean_tempo) * 100 if mean_tempo != 0 else 0

        # Create DataFrame for statistical summary
        df_stats = pd.DataFrame({
            'Metric': ['Mean', 'Standard Deviation', 'Coefficient of Variation (CV)'],
            'Value': [mean_tempo, std_tempo, cv_tempo]
        })

        # Plot tempo variations
        plt.figure(figsize=(10, 6))
        plt.plot(df['Tempo (bpm)'], marker='o', linestyle='-')
        plt.xlabel('Time (Segments)')
        plt.ylabel('Tempo (bpm)')
        plt.title(f'Tempo Variations Over Time - {file_name}')
        plt.grid(True)

        # Save plot to image
        img_data = BytesIO()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        plt.close()

        # Save to Excel
        wb = Workbook()

        # Create first sheet for tempo analysis
        ws1 = wb.active
        ws1.title = 'Tempo Analysis'
        for r in dataframe_to_rows(df, index=False, header=True):
            ws1.append(r)

        # Create second sheet for statistics and graph
        ws2 = wb.create_sheet(title='Statistics & Graph')
        for r in dataframe_to_rows(df_stats, index=False, header=True):
            ws2.append(r)

        # Insert image dynamically in the second sheet
        img = Image(img_data)
        ws2.add_image(img, 'C5')  # Adjust cell for better placement

        # Define the output file path
        excel_filename = os.path.join(output_folder, f"{file_name}_Tempo_Analysis.xlsx")
        wb.save(excel_filename)

        print(f"Tempo analysis saved to {excel_filename}")

    except Exception as e:
        print(f"Error processing {audio_file}: {e}")

print("Processing complete. All files have been saved in the output folder.")
