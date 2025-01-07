import pandas as pd
import matplotlib.pyplot as plt

# Load the FAOSTAT dataset
file_path = "FAOSTAT_data_en_1-8-2025.csv"  # Update with the correct path if needed
data = pd.read_csv(file_path)

# Inspect the first few rows to understand the dataset structure
print("Dataset preview:")
print(data.head())

# Check the column names
print("Column names:", data.columns)

# Filter the relevant data (check for the correct columns)
# Assuming 'Year' and 'Value' are the relevant columns
if 'Year' in data.columns and 'Value' in data.columns:
    data['Year'] = pd.to_numeric(data['Year'], errors='coerce')  # Ensure 'Year' is numeric
    data['Value'] = pd.to_numeric(data['Value'], errors='coerce')  # Ensure 'Value' is numeric

    # Drop rows with missing or invalid values
    data = data.dropna(subset=['Year', 'Value'])

    # Aggregate production values by year
    production_by_year = data.groupby('Year')['Value'].sum()

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(production_by_year.index, production_by_year.values, marker='o', color='green')
    plt.title("Global Tea Production Over Time")
    plt.xlabel("Year")
    plt.ylabel("Production (tons)")
    plt.grid(True)
    plt.show()
else:
    print("Error: 'Year' or 'Value' column not found in the dataset.")


# Risk analysis
# Group by 'Year' and 'Item' to observe trends in the tea data
tea_trends = data.groupby(['Year', 'Item'])['Value'].sum().reset_index()

# Plot trends by item
for item in tea_trends['Item'].unique():
    item_data = tea_trends[tea_trends['Item'] == item]
    plt.plot(item_data['Year'], item_data['Value'], label=item)

plt.title('Trends in Tea Production/Value by Item')
plt.xlabel('Year')
plt.ylabel('Value')
plt.legend()
plt.show()
