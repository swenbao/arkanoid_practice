import re
import pandas as pd

# Initialize an empty dictionary to store the win rates
win_rates = {}

# Pattern to extract level and win rate
pattern = r"Level: (\d+)\nTotal: \d+ rounds\nWin: \d+ rounds\nWin Rate: ([\d.]+)%"

# Loop through each model
for i in range(1, 11):
    model_name = f"new_big{i}nn_model_win_rate.txt"
    with open(model_name, 'r') as file:
        content = file.read()
        matches = re.findall(pattern, content)
        for level, win_rate in matches:
            win_rates.setdefault(level, []).append(float(win_rate))

# Convert the dictionary to a pandas DataFrame for better visualization
df = pd.DataFrame(win_rates)
df.index = [f"big{i+1}nn" for i in range(10)]  # Naming rows as big1nn, big2nn, ...

# Transpose the DataFrame to get levels as columns and models as rows
df = df.T

# Write the DataFrame to a CSV file
output_file_name = 'win_rates_summary.csv'
df.to_csv(output_file_name)

print(f"Win rates summary has been written to {output_file_name}")
