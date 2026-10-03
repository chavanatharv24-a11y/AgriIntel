import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import numpy as np

def train_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(current_dir, 'yield_dataset.csv')
    model_path = os.path.join(current_dir, 'yield_model.pkl')
    
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return
        
    print("Loading dataset...")
    df = pd.read_csv(dataset_path)
    
    print("\n--- Exploratory Data Analysis (EDA) ---")
    print("\nDataset Describe:")
    print(df.describe().to_string())
    
    print("\nCorrelation with Target (yield_kg_per_acre):")
    corr = df.corr()['yield_kg_per_acre'].sort_values(ascending=False)
    print(corr.to_string())
    print("-" * 39 + "\n")
    
    # Split data
    X = df.drop(columns=['yield_kg_per_acre'])
    y = df['yield_kg_per_acre']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training RandomForestRegressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    
    print("\n--- Evaluation Metrics ---")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"R-squared (R2): {r2:.4f}")
    
    # Save model
    joblib.dump(model, model_path)
    print(f"\nModel saved successfully to {model_path}")

if __name__ == "__main__":
    train_model()
