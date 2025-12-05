import joblib
import numpy as np
import pandas as pd
import streamlit as st
import json

# 1. Загрузка артефактов (модель + скейлер)
MODEL_PATH = "xgb_model_final.pkl"
SCALER_PATH = "scaler_final.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# 2. Маппинг подтипов недвижимости
PROPERTY_MAP = {
    "Apartment": ["Apartment", "Duplex", "Ground floor", "Loft", "Penthouse", "Studio", "Triplex"],
    "House": ["Bungalow", "Chalet", "Cottage", "Mansion", "Master house", "Mixed building", "Residence", "Villa"]
    }

# 3. Предобработка входных данных в формат DataFrame для модели
def preprocess(data: dict) -> pd.DataFrame:
    # Проверка соответствия подтипа
    type_ = data["TypeOfProperty"]
    subtype = data["SubTypeOfProperty"]

    if subtype not in PROPERTY_MAP[type_]:
        raise ValueError(f"Subtype '{subtype}' is not valid for TypeOfProperty '{type_}'")

    # Преобразуем в DataFrame
    df = pd.DataFrame([data])

    # Преобразуем булевые значения (None → 0)
    bool_cols = ["equiped_kitchen", "furnished", "terrace", "garden", "swimming_pool"]
    for col in bool_cols:
        df[col] = df[col].fillna(False).astype(bool).astype(int)

    # 🔥 Создаём категорию property_type как при обучении
    df["property_type"] = df["TypeOfProperty"] + "_" + df["SubTypeOfProperty"]

    # Удаляем исходные поля (если они НЕ участвовали в обучении)
    df = df.drop(columns=["TypeOfProperty", "SubTypeOfProperty"])

    # One-hot кодирование
    df = pd.get_dummies(df)

    # Выравнивание признаков
    # model_features = model.get_booster().feature_names
    model_features = json.load(open("features.json"))   

    for col in model_features:
        if col not in df.columns:
            df[col] = 0

    df = df[model_features]

    # Масштабирование
    df_scaled = scaler.transform(df)

    return df_scaled

# 4. Функция предсказания: возвращает прогноз цены в формате {"prediction": float,"status_code": int}
def predict(data: dict) -> dict:
    try:
        X = preprocess(data)
        prediction = model.predict(X)[0]

        return {
            "prediction": float(prediction),
            "status_code": 200
        }

    except Exception as e:
        return {
            "prediction": None,
            "status_code": 500,
            "error": str(e)
        }