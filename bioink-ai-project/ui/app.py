import streamlit as st
import joblib
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load trained model safely
# -----------------------------
model_path = os.path.join(os.path.dirname(__file__), "..", "model", "bioink_model.pkl")
model = joblib.load(model_path)

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Bio-Ink Printability Predictor",
    page_icon="🧬",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("🧬 AI Bio-Ink Printability Predictor")

st.write(
"""
This AI system predicts whether a **bio-ink formulation** can be successfully printed in a **3D bioprinter**.
The prediction is based on important printing parameters such as viscosity, pressure, temperature,
polymer concentration, and cell density.
"""
)

st.markdown("---")

# -----------------------------
# Input section
# -----------------------------
st.header("⚙️ Enter Bio-Ink Parameters")

col1, col2 = st.columns(2)

with col1:
    viscosity = st.slider("Viscosity", 5.0, 50.0, 25.0)
    temperature = st.slider("Temperature (°C)", 20.0, 37.0, 25.0)
    pressure = st.slider("Pressure", 10.0, 60.0, 30.0)

with col2:
    nozzle = st.selectbox("Nozzle Diameter", [0.2, 0.3, 0.4])
    polymer = st.slider("Polymer Concentration (%)", 1.0, 5.0, 3.0)
    cell_density = st.slider("Cell Density", 0.5, 2.0, 1.0)

st.markdown("---")

# -----------------------------
# Prediction button
# -----------------------------
if st.button("🔍 Predict Printability"):

    input_data = np.array([[viscosity, temperature, pressure, nozzle, polymer, cell_density]])

    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.success("✅ Printable Bio-Ink")
    else:
        st.error("❌ Not Printable")

    # -----------------------------
    # Show input summary
    # -----------------------------
    st.subheader("📋 Input Summary")

    input_df = pd.DataFrame({
        "Parameter": [
            "Viscosity",
            "Temperature",
            "Pressure",
            "Nozzle Diameter",
            "Polymer Concentration",
            "Cell Density"
        ],
        "Value": [
            viscosity,
            temperature,
            pressure,
            nozzle,
            polymer,
            cell_density
        ]
    })

    st.table(input_df)

    st.markdown("---")

    # -----------------------------
    # Feature Importance
    # -----------------------------
    st.subheader("📊 Feature Importance")

    importance = model.feature_importances_

    features = [
        "Viscosity",
        "Temperature",
        "Pressure",
        "Nozzle Diameter",
        "Polymer Concentration",
        "Cell Density"
    ]

    importance_df = pd.DataFrame({
        "Feature": features,
        "Importance": importance
    }).sort_values(by="Importance", ascending=False)

    fig, ax = plt.subplots()

    ax.barh(importance_df["Feature"], importance_df["Importance"])

    ax.set_xlabel("Importance Score")
    ax.set_title("Feature Importance in Prediction")

    st.pyplot(fig)

st.markdown("---")

st.caption("AI Model for Bio-Ink Printability Prediction | Machine Learning + Bioprinting")