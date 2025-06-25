import os
import pandas as pd
import statsmodels.formula.api as smf

# === Set your input CSV file and output folder ===
input_file = ''
output_folder = ''

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Extract filename from path
filename = os.path.basename(input_file)

print(f"📂 Processing: {filename}")

try:
    # Load CSV
    df = pd.read_csv(input_file)

    # Convert relevant columns to numeric, forcing non-numeric values to NaN
    cols_to_convert = ['Rate_of_Tempo_Change', 'Tempo_Change_Percentage', 'Arousal_Change']
    for col in cols_to_convert:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with any NaNs in key columns
    df_clean = df.dropna(subset=cols_to_convert)

    # Define and fit model
    formula = 'Arousal_Change ~ Rate_of_Tempo_Change + Tempo_Change_Percentage'
    model = smf.ols(formula=formula, data=df_clean).fit()

    # Build output text
    output_text = f"File: {filename}\n\nArousal Change Regression Results:\n"
    output_text += model.summary().as_text()

    # Save results
    output_filename = f"OLS_Regression_Report(Arousal Change)_{filename.replace('.csv', '')}.txt"
    output_path = os.path.join(output_folder, output_filename)

    with open(output_path, 'w') as f:
        f.write(output_text)

    print(f"✅ Saved: {output_filename}")

except Exception as e:
    print(f"⚠️ Error processing {filename}: {e}")
