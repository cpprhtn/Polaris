import streamlit as st
from polaris import PolarisEDA

def run_eda_app():
    # 파일 업로드
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        # Polaris 클래스 인스턴스화
        eda = PolarisEDA(uploaded_file)

        # EDA 보고서 생성
        report = eda.generate_eda_report()

        # HTML 리포트 출력
        st.markdown(report, unsafe_allow_html=True)

if __name__ == "__main__":
    run_eda_app()
