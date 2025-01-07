import pandas as pd
import matplotlib.pyplot as plt

# Example of loading the snippet into a dataframe (assuming data is already loaded)
data = pd.read_csv("FAOSTAT_data_en_1-8-2025.csv")

# Filter for production-related data
production_data = data[data['Element'] == 'Production']

# Group by Year and Area, and sum the production values
production_trends = production_data.groupby(['Year', 'Area'])['Value'].sum().reset_index()

# Plot production trends by area (e.g., Argentina)
plt.plot(production_trends['Year'], production_trends['Value'], label='Production in Argentina')

plt.title('Tea Production Trend in Argentina')
plt.xlabel('Year')
plt.ylabel('Production (tons)')
plt.legend()
plt.show()
# Filter for yield-related data
yield_data = data[data['Element'] == 'Yield']

# Group by Year and Area, and sum the yield values
yield_trends = yield_data.groupby(['Year', 'Area'])['Value'].sum().reset_index()

# Plot yield trends
plt.plot(yield_trends['Year'], yield_trends['Value'], label='Yield in Argentina')

plt.title('Tea Yield Trend in Argentina')
plt.xlabel('Year')
plt.ylabel('Yield (kg/ha)')
plt.legend()
plt.show()
# Filter for area harvested data
area_data = data[data['Element'] == 'Area harvested']

# Group by Year and Area, and sum the area harvested values
area_trends = area_data.groupby(['Year', 'Area'])['Value'].sum().reset_index()

# Plot harvested area trends
plt.plot(area_trends['Year'], area_trends['Value'], label='Area Harvested in Argentina')

plt.title('Tea Harvested Area Trend in Argentina')
plt.xlabel('Year')
plt.ylabel('Area harvested (ha)')
plt.legend()
plt.show()
# Analyze flag distribution
flag_counts = data['Flag'].value_counts()

# Plot flag counts to check for reliability of data
flag_counts.plot(kind='bar')
plt.title('Distribution of Data Flags')
plt.xlabel('Flag')
plt.ylabel('Count')
plt.show()
# Filter official and estimated data
official_data = data[data['Flag'] == 'A']
estimated_data = data[data['Flag'] == 'E']

# Compare production values between official and estimated data
plt.plot(official_data['Year'], official_data['Value'], label='Official Production', marker='o')
plt.plot(estimated_data['Year'], estimated_data['Value'], label='Estimated Production', marker='x')

plt.title('Official vs Estimated Tea Production in Argentina')
plt.xlabel('Year')
plt.ylabel('Production (tons)')
plt.legend()
plt.show()
