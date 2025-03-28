import streamlit as st
from utils import PolarisEDA

st.set_page_config(page_title="EDA Report", layout="wide")
st.title("📊 Exploratory Data Analysis (EDA)")

if "uploaded_file" not in st.session_state:
    st.warning("📂 먼저 메인 페이지에서 파일을 업로드해주세요.")
else:
    eda = PolarisEDA(st.session_state["uploaded_file"])
    eda.generate_eda_report()
