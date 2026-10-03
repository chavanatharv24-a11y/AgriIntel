import pandas as pd
import numpy as np
import os

def generate_data(num_samples=500):
    np.random.seed(42)
    
    # Generate features
    soil_moisture = np.random.uniform(20, 80, num_samples)
    temperature = np.random.uniform(15, 40, num_samples)
    humidity = np.random.uniform(30, 90, num_samples)
    land_size = np.random.uniform(0.5, 20, num_samples)
    rain_detected = np.random.randint(0, 2, num_samples)
    
    # Calculate yield per acre (base value)
    # 1. Soil moisture: peaks around 60
    moisture_effect = 1 - 0.0015 * (soil_moisture - 60)**2
    
    # 2. Temperature: peaks around 27
    temp_effect = 1 - 0.004 * (temperature - 27)**2
    
    # 3. Rainfall: binary effect
    rain_effect = np.where(rain_detected == 1, 1.1, 0.85)
    
    # 4. Humidity: slight positive effect
    humidity_effect = 0.8 + 0.002 * humidity
    
    # Base yield per acre (let's say average is around 2000 kg/acre)
    base_yield_per_acre = 2000 * np.clip(moisture_effect, 0.35, 1.2) * \
                          np.clip(temp_effect, 0.35, 1.2) * \
                          np.clip(rain_effect, 0.4, 1.1) * \
                          humidity_effect
                          
    # Total yield = yield per acre * land size
    yield_kg = base_yield_per_acre * land_size
    
    # Add ~10% random noise
    noise = np.random.normal(0, 0.1 * yield_kg)
    yield_kg = np.clip(yield_kg + noise, 0, None)
    
    # Construct DataFrame
    df = pd.DataFrame({
        'soilMoisture': soil_moisture,
        'temperature': temperature,
        'humidity': humidity,
        'landSize': land_size,
        'rainDetected': rain_detected,
        'yield_kg_per_acre': yield_kg / land_size  # Target is yield per acre
    })
    
    # Save to CSV
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'yield_dataset.csv')
    df.to_csv(output_path, index=False)
    print(f"Dataset with {num_samples} rows generated and saved to {output_path}")

if __name__ == "__main__":
    generate_data()
