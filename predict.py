import joblib
import numpy as np
import pandas as pd

# 1. Загрузка артефактов (модель + скейлер)
MODEL_PATH = "xgb_model_final.pkl"
SCALER_PATH = "scaler_final.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# 2. Маппинг подтипов недвижимости
PROPERTY_MAP = {
    "apartment": ["Apartment", "Duplex", "Ground floor", "Loft", "Penthouse", "Studio", "Triplex"],
    "house": ["Bungalow", "Chalet", "Cottage", "Mansion", "Master house", "Mixed building", "Residence", "Villa"]
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
        df[col] = df[col].astype(bool).astype(int)

    # One-hot кодирование категорий
    df = pd.get_dummies(df)

    # Чтобы избежать проблемы с отсутствующими колонками:
    # 1. Загружаем список признаков, использованных при обучении модели (модель XGBoost сохраняет feature_names_)
    model_features = model.get_booster().feature_names

    # 2. Добавляем отсутствующие признаки
    for col in model_features:
        if col not in df.columns:
            df[col] = 0

    # 3. Выравниваем порядок колонок
    df = df[model_features]

    # 4. Масштабирование
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