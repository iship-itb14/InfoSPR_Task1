import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import lightgbm as lgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
import smtplib
from email.mime.text import MIMEText
import requests

# Function to send email alerts
def send_email_alerts(low_stock_items, recipient_email):
    sender_email = input("Enter your Gmail address: ")
    sender_password = input("Enter your Gmail password (or app-specific password): ")

    subject = "Low Stock Alert"
    body = "\n".join([
        f"Domain: {row['Domain']}, Region: {row['Region']}, Item: {row['Item']}, "
        f"Simulated Stock Level: {row['Simulated_Stock_Level']:.2f}"
        for _, row in low_stock_items.iterrows()
    ])

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email alerts sent successfully!")
    except Exception as e:
        print(f"Failed to send email alerts: {e}")

# Function to send Slack alerts
def send_slack_alerts(low_stock_items, webhook_url):
    messages = [
        f"Domain: {row['Domain']}, Region: {row['Region']}, Item: {row['Item']}, "
        f"Simulated Stock Level: {row['Simulated_Stock_Level']:.2f}"
        for _, row in low_stock_items.iterrows()
    ]
    for message in messages:
        payload = {"text": message}
        try:
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 200:
                print(f"Slack alert sent: {message}")
            else:
                print(f"Failed to send Slack alert: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Failed to send Slack alert: {e}")

# Load the dataset
data = pd.read_csv('combined_supply_chain_risk_data.csv')

# Convert categorical columns to strings (ensure uniform data types)
categorical_cols = ['Domain', 'Region', 'Item', 'Flag', 'Flag Description', 'category']

for col in categorical_cols:
    data[col] = data[col].astype(str)

# Handling missing values
# Separate numeric and categorical columns
numeric_cols = data.select_dtypes(include=[np.number]).columns
categorical_cols = data.select_dtypes(exclude=[np.number]).columns

# Fill missing values in numeric columns with the mean
data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

# Fill missing values in categorical columns with the most frequent value (mode)
data[categorical_cols] = data[categorical_cols].fillna(data[categorical_cols].mode().iloc[0])

# Encoding categorical columns using LabelEncoder
label_encoders = {}
for col in categorical_cols:
    # Ensure column is treated as string before encoding
    data[col] = data[col].astype(str)

    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Selecting features and target variable
X = data.drop(columns=["Risk_Index"])  # Features
y = data["Risk_Index"]  # Target variable

# Split the dataset into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Set up LightGBM model
model = lgb.LGBMRegressor(objective='regression', metric='rmse')

# Train the model
model.fit(X_train, y_train)

# Predict the target on test set
y_pred = model.predict(X_test)

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# Hyperparameter Tuning using GridSearchCV
param_grid = {
    'num_leaves': [31, 50, 100],
    'max_depth': [-1, 5, 10],
    'learning_rate': [0.01, 0.1, 0.2],
    'n_estimators': [20, 50, 100]
}

# Create GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error')

# Fit grid search
grid_search.fit(X_train, y_train)

# Get best parameters and model
best_params = grid_search.best_params_
best_model = grid_search.best_estimator_

# Evaluate the best model
y_pred_best = best_model.predict(X_test)
rmse_best = np.sqrt(mean_squared_error(y_test, y_pred_best))

# Output Results
print("Risk Analysis Report:\n")
print(f"1. Initial RMSE (before tuning): {rmse:.2f}")
print(f"2. Optimized RMSE (after hyperparameter tuning): {rmse_best:.2f}")
print(f"3. Best Hyperparameters:\n{best_params}")

# Define a proxy for stock levels based on Production_Value or quantity
data['Simulated_Stock_Level'] = data['Production_Value']

# Define a low stock threshold
low_stock_threshold = data['Simulated_Stock_Level'].mean() * 0.01

# Identify items with low simulated stock
low_stock_items = data[data['Simulated_Stock_Level'] < low_stock_threshold]

# Remove duplicate entries based on specific columns (Domain, Region, Item) for stock level 0

low_stock_items = low_stock_items[low_stock_items['Simulated_Stock_Level'] > 0]
low_stock_items = low_stock_items.drop_duplicates(subset=['Domain', 'Region', 'Item'])

# Print low stock alerts
print("\nLow Stock Alerts:")
if not low_stock_items.empty:
    for _, row in low_stock_items.iterrows():
        print(f"Domain: {row['Domain']}, Region: {row['Region']}, Item: {row['Item']}, "
              f"Simulated Stock Level: {row['Simulated_Stock_Level']:.2f}")
else:
    print("No low stock items detected.")


# Prompt user for notification method
notify_method = input("Choose notification method (email/slack/none): ").lower()
if notify_method == "email":
    recipient_email = input("Enter recipient email address: ")
    send_email_alerts(low_stock_items, recipient_email)
elif notify_method == "slack":
    slack_webhook_url = input("Enter Slack webhook URL: ")
    send_slack_alerts(low_stock_items, slack_webhook_url)
else:
    print("No alerts sent.")

# Optional: Save the alerts to a CSV file
low_stock_items.to_csv('low_stock_alerts.csv', index=False)
print("\nLow stock alerts saved to 'low_stock_alerts.csv'.")
