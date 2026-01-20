import os
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from dotenv import load_dotenv

load_dotenv()

start_time = time.time()

# Configuration
MY_CSV_FILE = os.getenv("MY_CSV_FILE", "test_data_10000000.csv")
MY_FEATURES = ["feature_col1", "feature_col2", "feature_col3"]
MY_RESPONSE = "target_col"

# ---- READ DATA ----
if not os.path.exists(MY_CSV_FILE):
    print(f"Error: File {MY_CSV_FILE} not found.")
    exit(1)

print(f"Loading data from {MY_CSV_FILE}...")
df = pd.read_csv(MY_CSV_FILE)
print(f"Initial rows: {len(df)}")

# ---- PREPARE FEATURES ----
X = df[MY_FEATURES].astype(float)
y = df[MY_RESPONSE].astype(float)

# ---- TRAIN/TEST SPLIT ----
# We use 80% for training and 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set: {len(X_train)} rows | Testing set: {len(X_test)} rows")

# ---- MODEL TRAINING ----
print("Training Random Forest model...")
# Lowering n_estimators slightly for speed in local Docker; increase back to 500 for final runs
model = RandomForestRegressor(n_estimators=100, max_depth=20, n_jobs=-1)
model.fit(X_train, y_train)

# ---- PREDICTIONS ----
print("Making predictions on test set...")
y_pred = model.predict(X_test)

# Print first 5 predictions vs actuals
print("\nFirst 5 Predictions vs Actuals:")
for pred, actual in zip(y_pred[:5], y_test.iloc[:5]):
    print(f"Predicted: {pred:.4f} | Actual: {actual:.4f}")

# ---- METRICS ----
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\n--- Model Performance Metrics ---")
print(f"R-squared (R2): {r2:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print("---------------------------------\n")

end_time = time.time()
print(f"Total time taken: {end_time - start_time:.2f} seconds")