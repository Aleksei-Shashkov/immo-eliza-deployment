import streamlit as st
from predict import predict, PROPERTY_MAP
from typing import Dict

st.set_page_config(page_title="Real Estate Price Predictor", layout="centered")

st.title("🏠 Real Estate Price Predictor")

with st.form("predict_form"):
    province = st.selectbox("Province", [
        "Antwerp", "Brabant-Wallon", "Brussels", "East-Flanders", "Flemish-Brabant",
        "Hainaut", "Limburg", "Luik", "Luxembourg", "Namur", "West-Flanders"
    ])

    postalcode = st.number_input("Postal Code", min_value=1000, max_value=9999, value=1000, step=1)
    ptype = st.selectbox("Type of Property", ["apartment", "house"])
    subtype = st.selectbox("Subtype", PROPERTY_MAP[ptype])

    col1, col2 = st.columns(2)
    with col1:
        bedrooms = st.number_input("Bedrooms", min_value=0, value=1)
    with col2:
        living_area = st.number_input("Living area (m²)", min_value=10, value=50)

    st.markdown("Optional features")
    equiped_kitchen = st.checkbox("Equipped kitchen", value=False)
    furnished = st.checkbox("Furnished", value=False)
    terrace = st.checkbox("Terrace", value=False)
    garden = st.checkbox("Garden", value=False)
    swimming_pool = st.checkbox("Swimming pool", value=False)

    submit = st.form_submit_button("Predict price")

if submit:
    data = {
        # "province": province,
        "postalcode": int(postalcode),
        "TypeOfProperty": ptype,
        "SubTypeOfProperty": subtype,
        "Bedrooms": int(bedrooms),
        "living_area": int(living_area),
        "equiped_kitchen": bool(equiped_kitchen),
        "furnished": bool(furnished),
        "terrace": bool(terrace),
        "garden": bool(garden),
        "swimming_pool": bool(swimming_pool)
    }

    with st.spinner("Predicting..."):
        out = predict(data)

    if out.get("status_code") == 200:
        price = out["prediction"]
        st.success(f"Predicted price: €{price:,.2f}")
    else:
        st.error(f"Prediction failed: {out.get('error', 'unknown error')}")