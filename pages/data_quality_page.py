import streamlit as st
import polars as pl
from utils import DataQuality

st.set_page_config(page_title="Data Quality Report", layout="wide")
st.title("📌 Data Quality Assessment")

if "uploaded_file" not in st.session_state:
    st.warning("📂 먼저 메인 페이지에서 파일을 업로드해주세요.")
else:
    df = pl.read_csv(st.session_state["uploaded_file"], infer_schema_length=10000)
    dq = DataQuality(df)

    st.subheader("📋 Assessing Data Quality Metrics...")
    quality_metrics = dq.assess_data_quality()
    dq.plot_quality_metrics(quality_metrics)
