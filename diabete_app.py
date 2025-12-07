import streamlit as st
import numpy as np
import pickle
@st.cache_resource
def load_model():
    with open("model_final.pkl", "rb") as f:
        model = pickle.load(f)
    return model
model = load_model()
st.title("Diabetes Prediction App")
st.write("Enter patient information below to estimate the probability of diabetes.")
age = st.number_input("Age", min_value=1, max_value=120, value=40)
bmi = st.number_input("BMI (kg/m²)", 
                      min_value=10.0, 
                      max_value=100.0,    
                      value=25.0)
hba1c = st.number_input("HbA1c (%)", 
                        min_value=3.0, 
                        max_value=25.0,    
                        value=5.4)

glucose = st.number_input("Blood Glucose (mg/dL)", 
                          min_value=30, 
                          max_value=1000,   
                          value=100)
if hba1c >= 6.5:
    st.warning(" HbA1c above 6.5% suggests diabetes according to medical guidelines.")
elif hba1c >= 5.7:
    st.info(" HbA1c between 5.7% and 6.4% indicates prediabetes.")
if glucose >= 126:
    st.warning(" Fasting glucose ≥ 126 mg/dL suggests diabetes.")
elif glucose >= 100:
    st.info(" Fasting glucose between 100 and 125 mg/dL suggests prediabetes.")
if bmi >= 30:
    st.warning(" BMI above 30 indicates obesity, a major risk factor for diabetes.")
elif bmi >= 25:
    st.info(" BMI between 25 and 29.9 indicates overweight.")
gender = st.selectbox("Gender", ["Female", "Male"])
hypertension = st.selectbox("Hypertension", ["No", "Yes"])
heart = st.selectbox("Heart Disease", ["No", "Yes"])
smoking = st.selectbox("Smoking History", ["never", "former", "current", "ever", "not current"])
gender_Male = 1 if gender == "Male" else 0
gender_Other = 1 if gender == "Other" else 0
hypertension_val = 1 if hypertension == "Yes" else 0
heart_val = 1 if heart == "Yes" else 0
smoking_current = 1 if smoking == "current" else 0
smoking_ever = 1 if smoking == "ever" else 0
smoking_former = 1 if smoking == "former" else 0
smoking_never = 1 if smoking == "never" else 0
smoking_not_current = 1 if smoking == "not current" else 0
input_array = np.array([[
    age,
    hypertension_val,
    heart_val,
    bmi,
    hba1c,
    glucose,
    gender_Male,
    gender_Other,
    smoking_current,
    smoking_ever,
    smoking_former,
    smoking_never,
    smoking_not_current
]])
if st.button(" Predict"):
    proba = model.predict_proba(input_array)[0][1]
    pred = model.predict(input_array)[0]

    if pred == 1:
        st.error(f"High risk of diabetes.\nPredicted probability: {proba:.2f}")
    else:
        st.success(f" Low risk of diabetes.\nPredicted probability: {proba:.2f}")
