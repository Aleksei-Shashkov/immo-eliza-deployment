import streamlit as st
from predict import predict, PROPERTY_MAP
from typing import Dict

st.set_page_config(page_title="Immo Eliza Price Predictor", layout="centered")

st.title("🏠 Immo Eliza Price Predictor")

st.markdown("""
<style>

.result-wrapper {
    margin-top: 25px;
}

.result-card {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 25px;

    padding: 25px 30px;
    border-radius: 18px;
    background: #ffffff;
    border: 1px solid #e7e7e7;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);

    animation: fadeInUp 0.6s ease-out;
}

/* Левая колонка: параметры */
.params {
    width: 45%;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.param-title {
    font-size: 18px;
    font-weight: 600;
    color: #444;
    margin-bottom: 6px;
}

.param-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    font-size: 16px;
    color: #333;
}

.param-icon {
    font-size: 22px;
}

/* Правая колонка: результат */
.result-block {
    width: 55%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: right;
}

.result-title {
    font-size: 18px;
    color: #444;
    font-weight: 600;
}

.result-value {
    font-size: 42px;
    font-weight: 700;
    color: #2b7cff;
}

.result-sub {
    font-size: 15px;
    color: #777;
    margin-top: 4px;
}

/* Анимация */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)


# ===== ФОРМА ==============================================================
with st.form("form"):
    area = st.number_input("Area (m²)", min_value=10, max_value=300)
    rooms = st.number_input("Rooms", min_value=1, max_value=10)
    location = st.text_input("Location")
    submit = st.form_submit_button("Predict")


# ===== КАРТОЧКА РЕЗУЛЬТАТА ================================================
if submit:
    predicted_price = area * 1200 + rooms * 15000

    st.markdown(
        f"""
        <div class="result-wrapper">
            <div class="result-card">

                <!-- Левая колонка -->
                <div class="params">
                    <div class="param-title">Property parameters</div>

                    <div class="param-item">
                        <div class="param-icon">🏠</div>
                        Area: <b>{area} m²</b>
                    </div>

                    <div class="param-item">
                        <div class="param-icon">🛏️</div>
                        Rooms: <b>{rooms}</b>
                    </div>

                    <div class="param-item">
                        <div class="param-icon">📍</div>
                        Location: <b>{location if location else "—"}</b>
                    </div>
                </div>

                <!-- Правая колонка -->
                <div class="result-block">
                    <div class="result-title">Predicted price</div>
                    <div class="result-value">{predicted_price:,.0f} €</div>
                    <div class="result-sub">Based on your inputs</div>
                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True
    )