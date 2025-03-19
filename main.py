import streamlit as st
import polars as pl
from polaris import PolarisEDA, DataQuality

def run_app():
    st.title("📊 Data Analysis Dashboard")
    
    analysis_type = st.radio("Select Analysis Type:", ["Exploratory Data Analysis (EDA)", "Data Quality Assessment"])
    
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        if analysis_type == "Exploratory Data Analysis (EDA)":
            st.subheader("🔍 Running EDA Report...")
            eda = PolarisEDA(uploaded_file)
            report = eda.generate_eda_report()
            st.markdown(report, unsafe_allow_html=True)
        
        elif analysis_type == "Data Quality Assessment":
            st.subheader("📌 Running Data Quality Report...")
            df = pl.read_csv(uploaded_file, infer_schema_length=10000)
            quality_report = DataQuality(df)
            quality_metrics = quality_report.assess_data_quality()
            quality_report.plot_quality_metrics(quality_metrics)

if __name__ == "__main__":
    run_app()
