# Import all the necessary libraries
import pandas as pd
import joblib
import streamlit as st

# Add dynamic background and custom styles
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
        background-attachment: fixed;
    }
    .stApp {
        background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
        background-attachment: fixed;
    }
    .stTitle { color: #003366; }
    /* Dark table styling */
    table {
        background: #222831 !important;
        color: #f1f1f1 !important;
        border-radius: 8px;
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        font-size: 1.1em;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    th, td {
        background: #222831 !important;
        color: #f1f1f1 !important;
        padding: 10px 16px !important;
        border-bottom: 1px solid #393e46 !important;
    }
    th {
        background: #393e46 !important;
        color: #00adb5 !important;
        font-weight: bold;
    }
    tr:last-child td {
        border-bottom: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the model and structure
model = joblib.load("pollution_model.pkl")
model_cols = joblib.load("model_columns.pkl")

# Let's create an User interface
st.title("Water Pollutants Predictor")
st.write("Predict the water pollutants based on Year and Station ID")

# User inputs
year_input = st.number_input("Enter Year", min_value=2000, max_value=2100, value=2022)
station_id = st.text_input("Enter Station ID", value='1')

# To encode and then predict
if st.button('Predict'):
    if not station_id:
        st.warning('Please enter the station ID')
    else:
        # Prepare the input
        input_df = pd.DataFrame({'year': [year_input], 'id':[station_id]})
        input_encoded = pd.get_dummies(input_df, columns=['id'])

        # Align with model cols
        for col in model_cols:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[model_cols]

        # Predict
        predicted_pollutants = model.predict(input_encoded)[0]
        pollutants = ['O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']

        st.subheader(f"Predicted pollutant levels for the station '{station_id}' in {year_input}:")
        # Create a DataFrame for the results
        results_df = pd.DataFrame({
            'Pollutant': pollutants,
            'Predicted Value': [f"{val:.2f}" for val in predicted_pollutants]
        })
        st.table(results_df)