# -*- coding: utf-8 -*-
"""BIA FINAL COPY.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1u-O7olItpu4RoLwj5VomktYKwhiXLvfh
"""

!pip install streamlit pandas numpy scikit-learn matplotlib seaborn plotly

import os
import time
import logging
import warnings
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.getLogger("streamlit").setLevel(logging.ERROR)

st.set_page_config(page_title="Automated Data Analysis & ML Pipeline", layout="wide")

st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to:", ["Upload Data", "EDA", "ML Training"])

st.title("🚀 Automated Data Analysis & ML Pipeline")

# Upload Dataset
if page == "Upload Data":
    st.header("📂 Upload Your Dataset")
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.session_state.df = df
        st.write("### 📌 Data Preview:")
        st.dataframe(df.head())

# Exploratory Data Analysis (EDA)
elif page == "EDA":
    if "df" in st.session_state:
        df = st.session_state.df
        st.header("📊 Exploratory Data Analysis")

        # Missing Values
        st.subheader("🔍 Missing Values")
        missing_values = df.isnull().sum()
        st.write(missing_values[missing_values > 0])

        handle_missing = st.selectbox("Handle Missing Values:", ["Mean Imputation", "Median Imputation", "Drop Rows", "Do Nothing"])
        if handle_missing == "Mean Imputation":
            df.fillna(df.mean(), inplace=True)
        elif handle_missing == "Median Imputation":
            df.fillna(df.median(), inplace=True)
        elif handle_missing == "Drop Rows":
            df.dropna(inplace=True)

        # Duplicate Removal
        if st.checkbox("Remove Duplicates"):
            df.drop_duplicates(inplace=True)

        # Data Distribution
        st.subheader("📊 Data Visualization")
        selected_column = st.selectbox("Select Column for Visualization", df.columns)
        fig = px.histogram(df, x=selected_column, title=f"Distribution of {selected_column}", color_discrete_sequence=['blue'])
        st.plotly_chart(fig)

        # Correlation Heatmap
        st.subheader("📊 Correlation Heatmap")
        plt.figure(figsize=(10, 5))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
        st.pyplot(plt)

# Machine Learning Model Training
elif page == "ML Training":
    if "df" in st.session_state:
        df = st.session_state.df
        st.header("🤖 Machine Learning Model Training")
,
        # Target Selection
        target = st.selectbox("🎯 Select Target Variable", df.columns)
        features = [col for col in df.columns if col != target]

        # Convert categorical variables
        for col in df.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])

        X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

        # Feature Scaling
        if st.checkbox("Apply Feature Scaling"):
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

        # Model Selection
        st.subheader("⚙️ Select Machine Learning Model")
        model_type = st.radio("Task Type", ["Classification", "Regression"])
        model_choice = st.selectbox("Choose Model", ["Random Forest", "Logistic Regression", "SVM"])

        if model_choice == "Random Forest":
            model = RandomForestClassifier() if model_type == "Classification" else RandomForestRegressor()
        elif model_choice == "Logistic Regression":
            model = LogisticRegression() if model_type == "Classification" else LinearRegression()
        else:
            model = SVC() if model_type == "Classification" else SVR()

        # Train Model
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Model Evaluation
        st.header("📉 Model Evaluation")
        if model_type == "Classification":
            acc = accuracy_score(y_test, y_pred)
            st.write(f"### ✅ Accuracy: {acc:.2f}")
            st.text(classification_report(y_test, y_pred))
        else:
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            st.write(f"### 📉 Mean Squared Error: {mse:.2f}")
            st.write(f"### 📊 R-Squared: {r2:.2f}")

            # Prediction Visualization
            fig = px.scatter(x=y_test, y=y_pred, labels={'x': 'Actual', 'y': 'Predicted'}, title='Actual vs. Predicted')
            st.plotly_chart(fig)

with open("requirements.txt", "w") as f:
    f.write("streamlit\npandas\nnumpy\nscikit-learn\nplotly")
from google.colab import files
files.download("requirements.txt")
