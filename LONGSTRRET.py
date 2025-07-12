import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="수학 정답 번호 분석기", layout="wide")
st.title("📊 수학 시험 선택지 번호 분석기 (1~30번 문항)")
st.markdown("CSV 파일을 업로드하면 각 문항별 정답 번호의 분포를 분석하고, 어떤 번호를 찍는 게 유리한지 알려드립니다.")

# 실제 기출 통계 예시
real_world_stats = {
    "20": {"번호": 5, "횟수": 8, "출처": "2010~2020년 수능 및 모의고사"},
    "21": {"번호": 3, "횟수": 7, "출처": "2010~2020년 수능 및 모의고사"},
    "22": {"번호": 4, "횟수": 6, "출처": "2010~2020년 수능 및 모의고사"},
}

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (정답 번호만 포함된 30문항)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # 열 구조 확인 및 변환
        if df.shape[1] == 30:
            df.columns = [str(i) for i in range(1, 31)]
            df_long = df.melt(var_name="문항", value_name="정답번호")
        elif df.shape[1] == 2 and {"문항 번호", "정답"}.issubset(df.columns):
            df_long = df.rename(columns={"문항 번호": "문항", "정답": "정답번호"})
        else:
            st.error("지원되는 CSV 형식이 아닙니다. 1~30번 문항이 열로 존재하거나, '문항 번호', '정답' 열이 있어야 합니다.")
            st.stop()

        # 문항별 정답 번호 카운트
        counts = df_long.groupby(["문항", "정답번호"]).size().unstack(fill_value=0).sort_index(axis=1)

        # 표 출력
        st.subheader(

