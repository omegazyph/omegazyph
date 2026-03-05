# Date: 2026-01-28
# Script Name: predict_profit.py
# Author: omegazyph
# Updated: 2026-01-28
# Description: Improved prediction script with better path handling 
#              to ensure the model files are found correctly.

import pandas as pd
import joblib
import os

def predict_outcome():
    # This looks for the 'models' folder in the directory above 'src'
    # which is the standard Project folder structure we set up.
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'models', 'business_model.pkl')
    scaler_path = os.path.join(base_dir, 'models', 'scaler.pkl')

    # Check if the files exist at the calculated paths
    if not os.path.exists(model_path):
        print(f"Error: Could not find model at {model_path}")
        print("Make sure you ran train_model.py successfully.")
        return

    # 1. Load the saved model and scaler
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    print("--- Business AI Assistant (Ready) ---")
    
    try:
        # 2. Get input from Wayne
        user_miles = float(input("Enter expected miles for the trip: "))
        user_fuel = float(input("Enter estimated fuel cost: "))

        # 3. Format data
        input_data = pd.DataFrame([[user_miles, user_fuel]], columns=['Miles', 'Fuel_Cost'])

        # 4. Scale and Predict
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)

        print("-" * 30)
        print(f"Predicted Profit: ${prediction[0]:.2f}")
        
    except ValueError:
        print("Please enter valid numbers.")

if __name__ == "__main__":
    predict_outcome()