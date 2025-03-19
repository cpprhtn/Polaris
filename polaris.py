import polars as pl
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

class PolarisEDA:
    def __init__(self, file_path):
        self.df = pl.read_csv(file_path, infer_schema_length=10000)

    def generate_eda_report(self):
        st.title("📊 Polaris EDA Report")
        
        self.dataset_overview()
        self.detect_anomalies()
        self.visualize_numeric_data()
        self.correlation_matrix()
        self.categorical_data_analysis()
        self.timeseries_analysis()

    def dataset_overview(self):
        st.subheader("📌 Dataset Overview")
        st.write(f"🔹 Total Rows: {self.df.height}")
        st.write(f"🔹 Total Columns: {self.df.width}")
        st.write("🔹 Data Types:")
        st.dataframe(self.df.schema)
        
        st.subheader("⚠️ Missing Data Percentage")
        missing_data = self.df.null_count() / self.df.height * 100
        st.dataframe(missing_data.to_pandas())

    def detect_anomalies(self):
        st.subheader("🚨 Anomaly Detection")
        
        common_invalid_values = ["?", "unknown", "N/A", "null", "missing", "-"]
        text_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype == pl.Utf8]
        anomalies = []
        
        for col in text_cols:
            invalid_counts = self.df[col].is_in(common_invalid_values).sum()
            if invalid_counts > 0:
                detected_values = self.df[col].filter(self.df[col].is_in(common_invalid_values)).unique().to_list()
                anomalies.append({
                    "Column": col,
                    "Invalid Values Count": invalid_counts,
                    "Detected Values": ", ".join(map(str, detected_values))
                })
        
        if anomalies:
            st.subheader("🔍 Invalid String Values Detected")
            st.table(anomalies)
        else:
            st.write("✅ No invalid string values detected.")
        
        st.subheader("📌 Numeric Outliers")
        numeric_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype in [pl.Float64, pl.Int64]]
        outlier_summary = []
        
        for col in numeric_cols:
            q1 = self.df[col].quantile(0.25)
            q3 = self.df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outliers = self.df.filter((self.df[col] < lower_bound) | (self.df[col] > upper_bound))
            if len(outliers) > 0:
                outlier_values = outliers[col].unique().to_list()
                outlier_summary.append({
                    "Column": col,
                    "Outlier Count": len(outliers),
                    "Lower Bound": round(lower_bound, 2),
                    "Upper Bound": round(upper_bound, 2),
                    "Detected Outliers": ", ".join(map(str, outlier_values[:5])) + ("..." if len(outlier_values) > 5 else "")
                })
        
        if outlier_summary:
            st.subheader("📌 Numeric Outliers Detected")
            st.table(outlier_summary)
        else:
            st.write("✅ No numeric outliers detected.")

    def visualize_numeric_data(self):
        st.subheader("📊 Numeric Data Distribution")
        numeric_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype in [pl.Float64, pl.Int64]]
        
        for col in numeric_cols:
            st.write(f"🔹 **{col}**")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(self.df[col].to_pandas(), bins=20, kde=True, ax=ax)
            st.pyplot(fig)

    def correlation_matrix(self):
        st.subheader("📈 Correlation Matrix")
        numeric_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype in [pl.Float64, pl.Int64]]
        
        if len(numeric_cols) < 2:
            st.write("⚠️ Not enough numeric columns for correlation matrix.")
            return

        corr_matrix = self.df.select(numeric_cols).to_pandas().corr()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig)

    def categorical_data_analysis(self):
        st.subheader("🔢 Categorical Data Analysis")
        cat_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype == pl.Utf8]
        
        for col in cat_cols:
            st.write(f"🔹 **{col}**")
            value_counts = self.df[col].value_counts().head(10).to_pandas()
            st.bar_chart(value_counts.set_index(col))

    def timeseries_analysis(self):
        st.subheader("📅 Time-Series Analysis")
        date_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype == pl.Date]
        
        if not date_cols:
            st.write("⚠️ No date columns detected.")
            return
        
        for col in date_cols:
            st.write(f"🔹 **{col}**")
            self.df = self.df.with_columns(self.df[col].cast(pl.Date))
            time_series = self.df.groupby(col).count()
            st.line_chart(time_series.to_pandas().set_index(col))
    