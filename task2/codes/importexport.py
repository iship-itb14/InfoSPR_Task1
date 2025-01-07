import pandas as pd
import matplotlib.pyplot as plt


path = 'commodity_trade_statistics_data.csv'

# Load the dataset
data = pd.read_csv(path, low_memory=False)

# Check the first few rows and the column names to understand the structure
print("Dataset Preview:")
print(data.head())

# Check column names
print("\nDataset Columns:")
print(data.columns)

# Filter data for tea-related commodities
tea_data = data[data['commodity'].str.contains('Tea', case=False, na=False)]

# Filter for import/export flow and select relevant columns
tea_import_export = tea_data[tea_data['flow'].isin(['Export', 'Import'])]

# Group by year and flow to calculate total quantity and trade value
tea_trends = tea_import_export.groupby(['year', 'flow'])[['trade_usd', 'quantity']].sum().reset_index()

# Plot tea import/export trends over the years
plt.figure(figsize=(14, 7))

# Plot quantity trends
plt.subplot(1, 2, 1)
for flow in tea_trends['flow'].unique():
    flow_data = tea_trends[tea_trends['flow'] == flow]
    plt.plot(flow_data['year'], flow_data['quantity'], label=f'{flow} Quantity')
plt.xlabel('Year')
plt.ylabel('Quantity (kg or other unit)')
plt.title('Tea Import/Export Quantity Trends')
plt.legend()

# Plot trade value trends
plt.subplot(1, 2, 2)
for flow in tea_trends['flow'].unique():
    flow_data = tea_trends[tea_trends['flow'] == flow]
    plt.plot(flow_data['year'], flow_data['trade_usd'], label=f'{flow} Trade Value')
plt.xlabel('Year')
plt.ylabel('Trade Value (USD)')
plt.title('Tea Import/Export Trade Value Trends')
plt.legend()

plt.tight_layout()
plt.show()
