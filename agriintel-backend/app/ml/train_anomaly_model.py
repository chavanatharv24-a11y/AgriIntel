import pandas as pd
import os
from sklearn.ensemble import IsolationForest
import joblib

def train_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(current_dir, 'anomaly_dataset.csv')
    model_path = os.path.join(current_dir, 'anomaly_model.pkl')
    
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return
        
    print("Loading anomaly dataset...")
    df = pd.read_csv(dataset_path)
    
    print("Training IsolationForest model...")
    # contamination=0.05 specifies the proportion of outliers in the data set
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(df)
    
    # Predict anomalies on the training set as a sanity check
    # Returns 1 for inliers, -1 for outliers
    predictions = model.predict(df)
    
    num_anomalies = (predictions == -1).sum()
    num_normal = (predictions == 1).sum()
    
    print(f"\n--- Sanity Check on Training Data ---")
    print(f"Total points: {len(df)}")
    print(f"Normal points (1): {num_normal}")
    print(f"Anomalous points (-1): {num_anomalies}")
    
    # Save model
    joblib.dump(model, model_path)
    print(f"\nModel saved successfully to {model_path}")

if __name__ == "__main__":
    train_model()
