from fastapi import APIRouter, Depends, HTTPException
import joblib
import os
import pandas as pd
from app.routes.auth import get_current_user
from app.database import db

router = APIRouter(prefix="/predict", tags=["predictions"])

# Define model path based on the current file location
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml", "yield_model.pkl")
ANOMALY_MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml", "anomaly_model.pkl")

@router.get("/yield")
async def predict_yield(current_user: dict = Depends(get_current_user)):
    # Fetch most recent sensor reading
    sensor_reading = await db.db["sensor_readings"].find_one(
        {"userId": str(current_user["_id"])},
        sort=[("timestamp", -1)]
    )
    
    if not sensor_reading:
        raise HTTPException(status_code=404, detail="No sensor readings found for the user.")
        
    land_size = current_user.get("landSize")
    if land_size is None:
        raise HTTPException(status_code=400, detail="User profile is missing landSize.")
        
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=500, detail="Model file not found. Please train the model first.")
        
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {e}")
        
    # Extract features
    soil_moisture = sensor_reading.get("soilMoisture", 0)
    temperature = sensor_reading.get("temperature", 0)
    humidity = sensor_reading.get("humidity", 0)
    rain_detected_raw = sensor_reading.get("rainDetected", False)
    rain_detected = 1 if rain_detected_raw else 0
    
    # Feature array must match the exact order: [soilMoisture, temperature, humidity, landSize, rainDetected]
    features_df = pd.DataFrame([{
        "soilMoisture": soil_moisture,
        "temperature": temperature,
        "humidity": humidity,
        "landSize": land_size,
        "rainDetected": rain_detected
    }])
    
    try:
        predicted_yield = model.predict(features_df)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
        
    return {
        "predictedYieldKgPerAcre": round(float(predicted_yield), 1),
        "inputs": {
            "soilMoisture": soil_moisture,
            "temperature": temperature,
            "humidity": humidity,
            "landSize": land_size,
            "rainDetected": rain_detected
        }
    }

@router.get("/anomaly-check")
async def check_anomaly(current_user: dict = Depends(get_current_user)):
    sensor_reading = await db.db["sensor_readings"].find_one(
        {"userId": str(current_user["_id"])},
        sort=[("timestamp", -1)]
    )
    
    if not sensor_reading:
        raise HTTPException(status_code=404, detail="No sensor readings found for the user.")
        
    if not os.path.exists(ANOMALY_MODEL_PATH):
        raise HTTPException(status_code=500, detail="Anomaly model file not found.")
        
    try:
        model = joblib.load(ANOMALY_MODEL_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load anomaly model: {e}")
        
    soil_moisture = sensor_reading.get("soilMoisture", 0)
    temperature = sensor_reading.get("temperature", 0)
    humidity = sensor_reading.get("humidity", 0)
    
    features_df = pd.DataFrame([{
        "soilMoisture": soil_moisture,
        "temperature": temperature,
        "humidity": humidity
    }])
    
    try:
        prediction = model.predict(features_df)[0]
        score = model.decision_function(features_df)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anomaly prediction failed: {e}")
        
    status = "Normal" if prediction == 1 else "Anomalous"
    
    return {
        "status": status,
        "anomalyScore": round(float(score), 3),
        "inputs": {
            "soilMoisture": soil_moisture,
            "temperature": temperature,
            "humidity": humidity
        }
    }
