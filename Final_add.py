import pandas as pd

# Paths to the main CSV file and the additional CSV files
main_csv_path = r'C:\Users\rsun2\OneDrive\ChatData.csv'
type_csv_path = r'C:\Users\rsun2\OneDrive\Type.csv'
description_csv_path = r'C:\Users\rsun2\OneDrive\Description.csv'
affected_data_csv_path = r'C:\Users\rsun2\OneDrive\Affected_data.csv'
reported_csv_path = r'C:\Users\rsun2\OneDrive\Reported.csv'

# Read the main CSV file into a DataFrame
main_df = pd.read_csv(main_csv_path)

# Read the additional CSV files into DataFrames
type_df = pd.read_csv(type_csv_path)
description_df = pd.read_csv(description_csv_path)
affected_data_df = pd.read_csv(affected_data_csv_path)
reported_df = pd.read_csv(reported_csv_path)

# Ensure each additional data column has the correct number of rows
def extend_or_truncate(df, length):
    if len(df) < length:
        return df.reindex(range(length), fill_value=pd.NA)
    else:
        return df.iloc[:length]

# Extend or truncate the additional data columns to match the length of main_df
type_df = extend_or_truncate(type_df, len(main_df))
description_df = extend_or_truncate(description_df, len(main_df))
affected_data_df = extend_or_truncate(affected_data_df, len(main_df))
reported_df = extend_or_truncate(reported_df, len(main_df))

# Add the additional columns to the main DataFrame
main_df['Detected Date'] = reported_df['Detected Date']
main_df['Affected individuals'] = affected_data_df['Affected individuals']
main_df['Description'] = description_df['Description']
main_df['Type'] = type_df['Type']

# Path to save the updated data
updated_csv_path = r'C:\Users\rsun2\OneDrive\ChatData_With_All.csv'

# Save the updated DataFrame to a new CSV file
main_df.to_csv(updated_csv_path, index=False)

print(f"All columns successfully added and data saved to {updated_csv_path}")
