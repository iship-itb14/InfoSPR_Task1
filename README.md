# Milestone 1: 
## Supply Chain Management Project Documentation
### 1. Introduction

This project integrates real-time supply chain data using various APIs and employs GPT-4 for predictions and analysis in supply chain management.

Task 1: Integrate data APIs with Python to retrieve and process real-time supply chain data.
Task 2: Research GPT-4 (LLM) for applications in supply chain management, such as demand forecasting and trend analysis.
### 2. Task 1: Integrating Data APIs with Python
What are APIs?
APIs (Application Programming Interfaces) enable communication between different software systems. This project uses APIs to gather real-time data on shipping, inventory, global trade, and financials.

### APIs Used:

Event Registry: Real-time news data for market trends.
Freightos: Shipping rates and freight quotes.
MarineTraffic: Ship movement and port traffic.
UN Comtrade: Global trade statistics.
World Bank LPI: Logistics performance indices.
IMF: Global economic data.
NASDAQ Data: Financial data and trends.
Kaggle: Datasets for machine learning.
Dun & Bradstreet: Business and supplier data.
Python Code Example:
import requests

api_key = "your_api_key"
url = "https://api.eventregistry.org/api/v1/article/getArticles"
params = {"query": "supply chain", "apiKey": api_key}
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Data fetched successfully:", data)
else:
    print("Error fetching data:", response.status_code)
### Key Learnings:

Authentication: Use API keys securely.
Rate Limiting: Be aware of request limits.
Response Formats: Typically JSON or XML.
Error Handling: Handle timeouts and errors gracefully.
### 3. Task 2: Researching and Using GPT-4 for Supply Chain Management
What is GPT-4?
GPT-4 is an advanced language model by OpenAI that performs tasks like content generation, summarization, and prediction. It can be fine-tuned for specific tasks like supply chain management.
Applications in Supply Chain Management:
Demand Forecasting: Predict future demand using historical data.
Supply Chain Optimization: Optimize logistics and inventory.
Trend Analysis: Analyze market trends and disruptions.
Text Mining: Extract insights from unstructured data.
Integrating GPT-4 in Python:
import openai

openai.api_key = 'your_openai_api_key'

response = openai.Completion.create(
    model="gpt-4",
    prompt="Given the latest shipping data, what are the best strategies to optimize our supply chain for Q1?",
    max_tokens=150
)

print(response.choices[0].text.strip())
Key Learnings:

API Access: Obtain an OpenAI API key.
Token Limit: GPT-4 processes a limited amount of text per request.
Fine-Tuning: Tailor GPT-4 for specific tasks like supply chain management.
### 4. Conclusion
This project combines APIs for real-time data retrieval and GPT-4's capabilities for data analysis and predictions to optimize supply chain operations.




# MILESTONE 2:



## Tea Production, Risk, and Supply Chain Analysis
This project analyzes various aspects of tea production, trade, and supply chain risks using data from multiple sources. The project includes the following components:
1.	Global Tea Production Over Time
2.	Tea Production Risk Analysis (e.g., Argentina)
3.	Tea Import/Export Analysis
4.	Tea Leaf Disease Identification
5.	Supply Chain Risk Prediction
The code is organized into multiple Python scripts, each focusing on a specific aspect of the analysis.

## Project Structure
•	main.py: Analyzes global tea production trends and plots them over time.

•	risks.py: Focuses on analyzing tea production, yield, and harvested area trends, along with data flag distribution and comparisons between official and estimated data.

•	importexport.py: Analyzes tea import/export trends based on trade data and plots quantity and trade value trends.

•	tea_diseases.py: Downloads a dataset for identifying diseases in tea leaves and visualizes sample images from different disease categories.

•	combined.py: Predicts the risk index of supply chain data using LightGBM, with hyperparameter tuning.

## Requirements
•	Python 3.x

•	pandas for data manipulation

•	matplotlib for data visualization

•	sklearn for machine learning

•	lightgbm for LightGBM model

•	kagglehub for downloading datasets

•	PIL for image handling

You can install the necessary libraries using pip:
pip install pandas matplotlib scikit-learn lightgbm kagglehub Pillow

## How to Use

1.	Global Tea Production:
Run the main.py script to analyze and visualize the global tea production over time. Make sure to update the dataset path if needed.
```python main.py```

2.	Risk Analysis:
Run the risks.py script to analyze tea production, yield, and harvested area trends for Argentina, as well as compare official vs. estimated production values.
```python risks.py```

3.	Import/Export Analysis:
Run the importexport.py script to analyze tea import/export trends and visualize quantity and trade value trends.
```python importexport.py```

4.	Tea Diseases:
The tea_diseases.py script downloads the latest dataset for identifying diseases in tea leaves and displays sample images for different categories.
```python tea_diseases.py```

5.	Supply Chain Risk Prediction:
Run the combined.py script to predict the supply chain risk index based on historical data, with a LightGBM model and hyperparameter tuning.
```python combined.py```

## Code Overview

1. main.py
   
•	Functionality: Analyzes and plots global tea production trends over time.

•	Key Steps:

o	Loads and preprocesses the dataset.

o	Aggregates production data by year.

o	Plots the global tea production over time.

2. risks.py
   
•	Functionality: Analyzes tea production, yield, and harvested area trends, and compares official vs. estimated data.

•	Key Steps:

o	Filters production, yield, and area harvested data.

o	Plots the trends for Argentina.

o	Analyzes data flags for reliability.

3. importexport.py
   
•	Functionality: Analyzes tea import/export data and visualizes trends.

•	Key Steps:

o	Filters data for tea-related commodities.

o	Analyzes import/export flow data.

o	Plots trends for quantity and trade value.

4. tea_diseases.py

•	Functionality: Downloads a dataset to identify diseases in tea leaves and displays sample images.

•	Key Steps:

o	Downloads the dataset using kagglehub.

o	Displays sample images of tea diseases.

5. combined.py
•	Functionality: Predicts supply chain risks using LightGBM with hyperparameter tuning.

•	Key Steps:

o	Preprocesses the dataset (fills missing values and encodes categorical variables).

o	Trains a LightGBM model.

o	Performs hyperparameter tuning using GridSearchCV.

o	Evaluates and compares model performance before and after tuning.

## Conclusion
This project provides insights into the global tea production trends, risks, and supply chain management. The models built can be used to predict and mitigate risks in tea production and trade, and also help in disease identification in tea leaves for better quality control.

# Milestone 3

## Low Stock Alert System

This project provides a framework for identifying low stock items within a supply chain dataset by simulating stock levels based on available features such as Production_Value, quantity, or other relevant metrics. The solution generates alerts for items with stock levels below a defined threshold and optionally saves these alerts to a CSV file.

### Features

Simulates stock levels using the Production_Value column.

Dynamically calculates a low stock threshold based on the average stock levels in the dataset.

Identifies and lists items with simulated stock levels below the threshold.

Saves the low stock alerts to a CSV file for further analysis.

Requirements

Ensure the following Python libraries are installed before running the script:

pandas

numpy

Install missing packages using:

pip install pandas numpy

Columns in the Dataset

The dataset is expected to have the following columns:

Domain Code: Code representing the domain.

Domain: Description of the domain.

Area Code (M49): Region code based on M49 classification.

Region: Geographic region.

Element Code: Code for the element.

Element: Description of the element.

Item Code (CPC): Item classification code.

Item: Name of the item.

Year Code: Numeric representation of the year.

Year: Year of the record.

Unit: Unit of measurement.

Production_Value: Production metric used as a proxy for stock level.

Flag, Flag Description, Note: Additional metadata.

year: Alternate year field.

comm_code: Commodity code.

commodity: Name of the commodity.

flow: Trade flow description.

Trade_Value: Value of trade.

weight_kg: Weight in kilograms.

quantity_name: Name of the quantity.

quantity: Quantity value.

category: Category of the item.

Risk_Index: Risk metric.

How It Works

Simulating Stock Levels:

A new column, Simulated_Stock_Level, is derived from the Production_Value column.

Defining the Threshold:

The threshold for low stock is dynamically set to 30% of the average simulated stock level. This value can be adjusted in the code.

Generating Alerts:

Items with stock levels below the threshold are flagged.

Alerts include the Domain, Region, Item, and Simulated_Stock_Level for easy identification.

Saving Results:

Low stock alerts are saved to a CSV file named low_stock_alerts.csv.

Usage

Place the dataset file in the same directory as the script. The file should be named combined_supply_chain_risk_data.csv.

Run the script in Python:

``python low_stock_alerts.py``

Check the console for low stock alerts.

Review the saved alerts in the low_stock_alerts.csv file.

Example Output

Console Alerts:

Low Stock Alerts:
Domain: Chemicals, Region: Europe, Item: Plastics, Simulated Stock Level: 40.00
Domain: Textiles, Region: Africa, Item: Fabrics, Simulated Stock Level: 60.00

Low stock alerts saved to 'low_stock_alerts.csv'.

Customization

Adjust Threshold: Modify the low_stock_threshold value to change the sensitivity of low stock detection.

Alternative Metrics: Replace Production_Value with other columns like quantity or weight_kg if more suitable for stock level estimation.





