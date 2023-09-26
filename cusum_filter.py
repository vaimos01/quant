import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def cusum_filter(data, baseline_window=30, h_plus=2.0, h_minus=-2.0):
    """
    Apply CUSUM filter to a DataFrame.

    Parameters:
    - data: DataFrame with 'Timestamp' and 'Price' columns.
    - baseline_window: Number of data points to use for baseline estimation.
    - h_plus: Positive threshold.
    - h_minus: Negative threshold.

    Returns:
    - cusum_values: A list of CUSUM values.
    """
    baseline = data['Price'].iloc[:baseline_window].mean()
    cusum_pos = 0
    cusum_neg = 0
    cusum_values = []

    for _, row in data.iterrows():
        deviation = row['Price'] - baseline
        cusum_pos = max(0, cusum_pos + deviation - h_plus)
        cusum_neg = max(0, cusum_neg - deviation - h_minus)
        cusum_values.append(cusum_pos - cusum_neg)

    return cusum_values


# Apply CUSUM filter to the DataFrame
cusum_values = cusum_filter(data)

# Plot CUSUM values
plt.figure(figsize=(10, 6))
plt.plot(data['Timestamp'], cusum_values, label='CUSUM Values', color='c')
plt.axhline(y=2.0, color='r', linestyle='--', label='Positive Threshold')
plt.axhline(y=-2.0, color='g', linestyle='--', label='Negative Threshold')
plt.title('CUSUM Filter')
plt.xlabel('Timestamp')
plt.ylabel('CUSUM Value')

plt.tight_layout()
plt.legend()
plt.grid(True)
plt.show()
