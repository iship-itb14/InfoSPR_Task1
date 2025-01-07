import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import lightgbm as lgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV

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

# Conclusion
print("\nConclusion:")
if rmse_best < rmse:
    print(
        "The model performance improved after hyperparameter tuning. The optimized model is better at predicting the risk index.")
else:
    print(
        "The hyperparameter tuning did not significantly improve the model performance. Further tuning or model adjustments may be needed.")

# Supply Chain Management Insights
print("\nSupply Chain Management Insights:")
if rmse_best < rmse:
    print(
        "With improved risk predictions, this model can help optimize supply chain risk management by identifying key risk factors and mitigating potential disruptions.")
else:
    print(
        "The model provides a baseline for understanding supply chain risks, but further enhancements are necessary for more accurate predictions.")
