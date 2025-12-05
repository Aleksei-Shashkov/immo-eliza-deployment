from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from predict import predict, PROPERTY_MAP

app = FastAPI(title="Real Estate Price API")

class InputModel(BaseModel):
    province: str = Field(..., example="Antwerp")
    postalcode: int = Field(..., example=2000)
    TypeOfProperty: str = Field(..., example="apartment")
    SubTypeOfProperty: str = Field(..., example="Apartment")
    Bedrooms: int = Field(..., example=2)
    living_area: int = Field(..., example=75)
    equiped_kitchen: Optional[bool] = False
    furnished: Optional[bool] = False
    terrace: Optional[bool] = False
    garden: Optional[bool] = False
    swimming_pool: Optional[bool] = False

@app.post("/predict")
def predict_endpoint(payload: InputModel):
    data = payload.dict()
    # quick validation for subtype
    t = data["TypeOfProperty"]
    s = data["SubTypeOfProperty"]
    if s not in PROPERTY_MAP.get(t, []):
        raise HTTPException(status_code=400, detail=f"Invalid subtype '{s}' for type '{t}'")
    out = predict(data)
    if out.get("status_code") != 200:
        raise HTTPException(status_code=500, detail=out.get("error", "prediction failed"))
    return out