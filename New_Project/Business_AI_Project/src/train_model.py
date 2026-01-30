# Date: 2026-01-28
# Script Name: train_model.py
# Author: omegazyph
# Updated: 2026-01-28
# Description: This script performs incremental machine learning using 
#              SGDRegressor to analyze business expenses and provide insights.
#              Refined to remove unused imports and optimize for 8GB RAM.

import pandas as pd
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
import joblib # Used for saving and loading the model "brain"
import os

def run_training():
    # Define file paths within the Project folder structure
    # Project folder: Business_AI_Project
    data_path = os.path.join('data', 'settlement_data.csv')
    model_path = os.path.join('models', 'business_model.pkl')
    scaler_path = os.path.join('models', 'scaler.pkl')

    # Ensure the model directory exists to avoid save errors
    if not os.path.exists('models'):
        os.makedirs('models')

    # Check if data exists before trying to learn
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please add your settlement data.")
        return

    # 1. Load data
    # We load the CSV into a DataFrame. For 8GB RAM, this is fine for standard 
    # settlement files. If the file grows to several GBs, we can use chunking.
    data_chunk = pd.read_csv(data_path)

    # Example Feature Selection:
    # Adjust 'Miles' and 'Fuel_Cost' to match your actual CSV column names.
    features = ['Miles', 'Fuel_Cost']
    target = 'Profit'

    X = data_chunk[features]
    y = data_chunk[target]

    # 2. Initialize or Load the Model/Scaler
    # SGDRegressor is perfect for your Legion laptop because it updates
    # weights incrementally rather than loading everything into RAM.
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        print("Existing model loaded. AI is continuing its education...")
    else:
        model = SGDRegressor()
        scaler = StandardScaler()
        print("New model initialized. Starting from scratch.")

    # 3. Scaling the data 
    # Scalers must also be updated incrementally using partial_fit.
    scaler.partial_fit(X)
    X_scaled = scaler.transform(X)

    # 4. The "Learning" step
    # partial_fit allows the AI to learn from these new rows without 
    # forgetting what it learned in previous sessions.
    model.partial_fit(X_scaled, y)

    # 5. Save the updated state to your 200GB free space
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)

    print("AI training complete. The model has been updated and saved.")

if __name__ == "__main__":
    run_training()