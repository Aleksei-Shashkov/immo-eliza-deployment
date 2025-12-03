import pytest
from predict import preprocess, predict, PROPERTY_MAP
import numpy as np

# sample valid input
VALID_INPUT = {
    "province": "Antwerp",
    "postalcode": 2000,
    "TypeOfProperty": "apartment",
    "SubTypeOfProperty": "Apartment",
    "Bedrooms": 2,
    "living_area": 75,
    "equiped_kitchen": True,
    "furnished": False,
    "terrace": True,
    "garden": False,
    "swimming_pool": False
}

def test_property_map_valid():
    assert "Apartment" in PROPERTY_MAP["apartment"]

def test_predict_returns_structure():
    out = predict(VALID_INPUT)
    assert "prediction" in out
    assert "status_code" in out
    assert out["status_code"] == 200
    assert isinstance(out["prediction"], float)

def test_preprocess_shape():
    X = preprocess(VALID_INPUT)
    # should be 2D array
    assert len(X.shape) == 2