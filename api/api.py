from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from predict import predict, PROPERTY_MAP

app = FastAPI(title="Real Estate Price API")

class InputModel(BaseModel):
    province: str = Field(..., json_schema_extra={"example": "Antwerp"})
    postalcode: int = Field(..., json_schema_extra={"example": 1000})
    TypeOfProperty: str = Field(..., json_schema_extra={"example": "apartment"})
    SubTypeOfProperty: str = Field(..., json_schema_extra={"example": "Apartment"})
    Bedrooms: int = Field(..., json_schema_extra={"example": 2})
    living_area: int = Field(..., json_schema_extra={"example": 75})
    equiped_kitchen: Optional[bool] = Field(default=False)
    furnished: Optional[bool] = Field(default=False)
    terrace: Optional[bool] = Field(default=False)
    garden: Optional[bool] = Field(default=False)
    swimming_pool: Optional[bool] = Field(default=False)

@app.post("/predict")
def predict_endpoint(payload: InputModel):
    data = payload.model_dump()  # Pydantic 2
    # validate subtype
    t = data["TypeOfProperty"]
    s = data["SubTypeOfProperty"]
    if s not in PROPERTY_MAP.get(t, []):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid subtype '{s}' for type '{t}'"
        )
    out = predict(data)
    if out.get("status_code") != 200:
        raise HTTPException(status_code=500, detail=out.get("error", "prediction failed"))
    return out