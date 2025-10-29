# ==========================================================
# 📊 Auto EDA Pro — Automated Exploratory Data Analysis App
# Author: Saurabh Srivastva
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import sweetviz as sv
import tempfile
import os

# -----------------------------------
# ⚙️ Page Configuration
# -----------------------------------
st.set_page_config(page_title="Auto EDA Pro", layout="wide", page_icon="🤖")

# -----------------------------------
# 🎨 Theme Toggle
# -----------------------------------
st.sidebar.title("⚙️ Settings")
theme = st.sidebar.radio("Choose Theme:", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
        <style>
        body, .stApp { background-color: #0E1117; color: #FFFFFF; }
        .dataframe { background-color: #1E222A; color: #FFFFFF; }
        .stButton>button {
            background-color: #262730; 
            color: white; 
            border-radius: 8px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #4CAF50; 
            color: white;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body, .stApp { background-color: #FFFFFF; color: #000000; }
        .stButton>button {
            background-color: #f0f0f0; 
            color: black; 
            border-radius: 8px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #4CAF50; 
            color: white;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)

# -----------------------------------
# 🧭 Header
# -----------------------------------
st.title("🤖 Auto EDA Pro")
st.write("Welcome! Upload your dataset and get instant **data insights, visualizations, and reports** — all in one click.")

# -----------------------------------
# 📁 File Upload
# -----------------------------------
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df = df.convert_dtypes()
        st.success("✅ File uploaded successfully!")

        # --- Clean dataframe for Streamlit display ---
        for col in df.columns:
            dtype_str = str(df[col].dtype)
            if dtype_str in ["Int64", "Float64"]:
                df[col] = df[col].astype("float64")
            elif pd.api.types.is_object_dtype(df[col]):
                df[col] = df[col].astype(str)

        # Show cleaned data preview
        st.dataframe(df.head())

    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
    else:
        # -----------------------------------
        # 📘 Basic Info Section
        # -----------------------------------
        st.header("📘 Basic Information")
        st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")
        st.write("**Column Names:**", list(df.columns))
        st.write("**Missing Values:**")
        st.dataframe(df.isnull().sum().to_frame("Missing Count"))
        st.write("**Data Types:**")
        st.dataframe(df.dtypes)

        # -----------------------------------
        # 💡 Smart Insights
        # -----------------------------------
        st.header("💡 Smart Insights")

        # Missing value alert
        missing = df.isnull().sum().sum()
        if missing > 0:
            st.warning(f"⚠️ Missing Values detected: {missing} cells are empty.")
        else:
            st.success("✅ No Missing Values found.")

        # Correlation Analysis
        st.subheader("📈 Correlation Heatmap")
        num_df = df.select_dtypes(include=np.number)

        if not num_df.empty and num_df.shape[1] > 1:
            corr = num_df.corr(numeric_only=True)
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax, fmt=".2f")
            st.pyplot(fig)
        else:
            st.info("No numeric columns found or insufficient numeric data for correlation heatmap.")

        # Descriptive Statistics
        st.subheader("✨ Key Descriptive Statistics")
        st.dataframe(df.describe())

        # -----------------------------------
        # 📊 Interactive Visualization
        # -----------------------------------
        st.header("📊 Interactive Visualizations")

        cols = df.columns.tolist()
        x_axis = st.selectbox("Select X-axis:", options=cols)
        y_axis = st.selectbox("Select Y-axis (for numeric plots):", options=cols)
        chart_type = st.selectbox("Choose Chart Type:", ["Scatter", "Line", "Histogram", "Boxplot", "Bar"])

        if st.button("Generate Chart"):
            try:
                if chart_type == "Scatter":
                    fig = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot", template="plotly_dark" if theme == "Dark" else "plotly_white")
                elif chart_type == "Line":
                    fig = px.line(df, x=x_axis, y=y_axis, title="Line Plot", template="plotly_dark" if theme == "Dark" else "plotly_white")
                elif chart_type == "Histogram":
                    fig = px.histogram(df, x=x_axis, title="Histogram", template="plotly_dark" if theme == "Dark" else "plotly_white")
                elif chart_type == "Boxplot":
                    fig = px.box(df, x=x_axis, y=y_axis, title="Boxplot", template="plotly_dark" if theme == "Dark" else "plotly_white")
                else:
                    fig = px.bar(df, x=x_axis, y=y_axis, title="Bar Chart", template="plotly_dark" if theme == "Dark" else "plotly_white")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Chart error: {e}")

        # -----------------------------------
        # 📄 Automated EDA Report (Sweetviz)
        # -----------------------------------
        st.header("📄 Automated EDA Report (Sweetviz)")

        if st.button("Generate Full Report"):
            st.info("Generating Sweetviz report... please wait ⏳")
            report = sv.analyze(df)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
                report.show_html(tmpfile.name)
                st.success("✅ Report generated successfully!")

                with open(tmpfile.name, "rb") as f:
                    st.download_button(
                        label="📥 Download Full HTML Report",
                        data=f,
                        file_name="AutoEDA_Report.html",
                        mime="text/html"
                    )

        # -----------------------------------
        # ✅ Completion Message
        # -----------------------------------
        st.success("✅ All tasks completed. Explore your data above!")

else:
    st.info("👆 Please upload a dataset to begin.")

# -----------------------------------
# 🧠 Help & Usage Sidebar
# -----------------------------------
with st.sidebar.expander("❓ Help & Usage"):
    st.markdown("""
    **How to Use Auto EDA Pro:**
    1. Upload a CSV file using the uploader.
    2. View the preview, insights, and correlations.
    3. Generate and explore interactive charts.
    4. Click "Generate Full Report" to create a Sweetviz EDA summary.
    5. Download the full report in HTML format.
    6. Use the Theme toggle above to switch Light/Dark mode.

    **Note:**  
    Some warnings (like from `pkg_resources`) are harmless and can be ignored.
    """)

# -----------------------------------
# 🧾 Footer
# -----------------------------------
st.markdown("""
---
👨‍💻 **Developed by:** *Saurabh Srivastva*  
📅 **Version:** 1.0  
🧩 **Tech Stack:** Python, Streamlit, Pandas, Sweetviz, Plotly, Seaborn  
💬 *Built with ❤️ for data enthusiasts.*
""")
