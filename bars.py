import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Function to create volume bars
def create_volume_bars(data, volume_threshold=1000):
    volume_cumsum = data['Volume'].cumsum()
    volume_bars = data.iloc[np.where(volume_cumsum.diff() >= volume_threshold)[0] + 1]
    return volume_bars

# Function to create dollar bars
def create_dollar_bars(data, dollar_threshold=1000):
    dollar_cumsum = (data['Volume'] * data['Price']).cumsum()
    dollar_bars = data.iloc[np.where(dollar_cumsum.diff() >= dollar_threshold)[0] + 1]
    return dollar_bars



# Function to create volume imbalance bars
def create_volume_imbalance_bars(data, imbalance_threshold=1000):
    bars = []
    current_bar = []
    # Calculate order flow imbalance
    data['Imbalance'] = data['BuyVolume'] - data['SellVolume']
    for _, row in data.iterrows():
        current_bar.append(row)
        if abs(sum(current_bar)['Imbalance']) >= imbalance_threshold:
            bars.append(pd.concat(current_bar, axis=1).T)
            current_bar = []
    if current_bar:
        bars.append(pd.concat(current_bar, axis=1).T)
    return pd.concat(bars).reset_index(drop=True)


# Create different bars
bars = {
    'Time Bars': data,
    'Volume Bars': create_volume_bars(data),
    'Dollar Bars': create_dollar_bars(data),
    'Imbalance Bars': create_volume_imbalance_bars(data),
}

# Plotting
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.subplots_adjust(hspace=0.4)

for i, (bar_type, bar_data) in enumerate(bars.items()):
    row, col = divmod(i, 3)
    ax = axes[row, col]
    ax.plot(bar_data['Timestamp'], bar_data['Price'], label=bar_type)
    ax.set_title(bar_type)
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Price')

plt.tight_layout()
plt.show()
