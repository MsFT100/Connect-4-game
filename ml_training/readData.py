import pandas as pd

# Load the dataset from local file
file_path = "connect-4.data"  # Update this with the correct path
column_names = [f"col_{i}" for i in range(42)] + ["outcome"]

df = pd.read_csv(file_path, names=column_names)

# Show first few rows
print(df.head())
