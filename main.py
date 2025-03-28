import streamlit as st

def run_app():
    st.title("📊 데이터 분석 대시보드")
    st.write("👈 왼쪽 사이드바에서 분석 페이지를 선택하세요.")

    uploaded_file = st.file_uploader("📂 CSV 파일 업로드", type=["csv"])
    
    if uploaded_file:
        # 세션에 저장
        st.session_state["uploaded_file"] = uploaded_file
    elif "uploaded_file" in st.session_state:
        # 이미 저장된 파일이 있다면 유지
        uploaded_file = st.session_state["uploaded_file"]

if __name__ == "__main__":
    run_app()
