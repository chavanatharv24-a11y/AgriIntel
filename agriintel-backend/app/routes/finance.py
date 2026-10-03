from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.routes.auth import get_current_user
from app.routes.predictions import predict_yield

router = APIRouter(prefix="/finance", tags=["finance"])

class FinanceRequest(BaseModel):
    seedCost: float = 0.0
    fertilizerCost: float = 0.0
    laborCost: float = 0.0
    otherCosts: float = 0.0
    sellingPricePerKg: float

@router.post("/calculate")
async def calculate_finance(request: FinanceRequest, current_user: dict = Depends(get_current_user)):
    # Fetch yield using existing logic
    # predict_yield raises HTTPException on failures (e.g., no sensors, missing model)
    yield_data = await predict_yield(current_user)
    
    predictedYieldPerAcre = yield_data["predictedYieldKgPerAcre"]
    landSize = current_user.get("landSize")
    
    if landSize is None:
        raise HTTPException(status_code=400, detail="User profile is missing landSize.")
        
    totalYieldKg = predictedYieldPerAcre * landSize
    totalCost = request.seedCost + request.fertilizerCost + request.laborCost + request.otherCosts
    revenue = totalYieldKg * request.sellingPricePerKg
    profit = revenue - totalCost
    profitMarginPercent = (profit / revenue * 100) if revenue > 0 else 0
    breakEvenPricePerKg = totalCost / totalYieldKg if totalYieldKg > 0 else 0
    
    return {
        "totalYieldKg": round(totalYieldKg, 2),
        "totalCost": round(totalCost, 2),
        "revenue": round(revenue, 2),
        "profit": round(profit, 2),
        "profitMarginPercent": round(profitMarginPercent, 2),
        "breakEvenPricePerKg": round(breakEvenPricePerKg, 2)
    }
