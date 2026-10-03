import pandas as pd
import numpy as np
import os

def generate_anomaly_data(num_samples=500):
    np.random.seed(42)
    
    # Generate "normal" features using np.random.normal
    # soilMoisture: centered ~50, range roughly 30-70 => std_dev ~ 6.67
    soil_moisture = np.random.normal(loc=50.0, scale=6.67, size=num_samples)
    
    # temperature: centered ~27, range roughly 20-35 => std_dev ~ 2.5
    temperature = np.random.normal(loc=27.0, scale=2.5, size=num_samples)
    
    # humidity: centered ~60, range roughly 40-80 => std_dev ~ 6.67
    humidity = np.random.normal(loc=60.0, scale=6.67, size=num_samples)
    
    # Construct DataFrame
    df = pd.DataFrame({
        'soilMoisture': soil_moisture,
        'temperature': temperature,
        'humidity': humidity
    })
    
    # Save to CSV
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'anomaly_dataset.csv')
    df.to_csv(output_path, index=False)
    print(f"Anomaly dataset with {num_samples} rows generated and saved to {output_path}")

if __name__ == "__main__":
    generate_anomaly_data()
