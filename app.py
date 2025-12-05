import streamlit as st
from predict import predict, PROPERTY_MAP
from typing import Dict

st.set_page_config(page_title="Immo Eliza Price Predictor", layout="centered")

st.title("🏠 Immo Eliza Price Predictor")

# Дизайн кнопки
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        border-radius: #8px;
        height: #3em;
        width: #12em;
        font-size: #16px
    }
    div.stButton > button:first-child:hover {
        background-color: #45a049;
        color: white;
    }
    </style>
""", unsafe_allow_html=True
    )

with st.form("predict_form"):

    province = st.selectbox(
        "Province",
        [
            "Antwerp", "Brabant-Wallon", "Brussels", "East-Flanders", "Flemish-Brabant",
            "Hainaut", "Limburg", "Luik", "Luxembourg", "Namur", "West-Flanders"
        ]
    )

    postalcode = st.number_input(
        "Postal Code",
        min_value=1000,
        max_value=9999,
        value=1000,
        step=1
    )

    # Type → SubType
    col1, col2 = st.columns(2)
    with col1:
        ptype = st.radio("Type of Property",options=list(PROPERTY_MAP.keys()),horizontal=True)
    with col2:
        subtype = st.selectbox("Subtype",options=PROPERTY_MAP[ptype])
    
    col1, col2 = st.columns(2)
    with col1:
        bedrooms = st.slider("Bedrooms", min_value=0,max_value=10,value=1,step=1)
    with col2:
        living_area = st.slider("Living area (m²)",min_value=10,max_value=500,value=50,step=1)

    st.markdown("### Optional features")

    col1, col2 = st.columns(2)

    with col1:
        equiped_kitchen = st.checkbox("Equipped kitchen", value=False)
        furnished = st.checkbox("Furnished", value=False)
        terrace = st.checkbox("Terrace", value=False)

    with col2:
        garden = st.checkbox("Garden", value=False)
        swimming_pool = st.checkbox("Swimming pool", value=False)

    submit = st.form_submit_button("Predict price")

########################################################################################################
# https://docs.streamlit.io/deploy

    add_selectbox = st.sidebar.selectbox("I want to sell:",("within a month","within 6 months", "within 1 year", "no urgency"))
    with st.sidebar:
        add_radio = st.radio("Choose a payment method",("By credit card", "By cash"))

########################################################################################################
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