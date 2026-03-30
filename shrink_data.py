import pandas as pd
import os
file_path = "data/paysim_data.csv"
df = pd.read_csv(file_path)
df_small = df.head(100000)
df_small.to_csv(file_path, index=False)
new_size = os.path.getsize(file_path) / (1024 * 1024)
print(f"{new_size:.2f} MB")