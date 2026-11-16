"""주간 비교 페이지."""

from pathlib import Path

import pandas as pd
import streamlit as st

import calc


st.title("주간 비교")
st.caption("교육용 가상 데이터")

project_dir = Path(__file__).resolve().parent.parent
previous_week = calc.load_readiness(project_dir / "data" / "readiness_W44.csv")
current_week = calc.load_readiness(project_dir / "data" / "readiness_W45.csv")
comparison = calc.compare_weeks(previous_week, current_week)

st.subheader("가동률 상승 상위 3")
st.dataframe(comparison.head(3), hide_index=True, use_container_width=True)

st.subheader("가동률 하락 상위 3")
st.dataframe(
    comparison.tail(3).iloc[::-1].reset_index(drop=True),
    hide_index=True,
    use_container_width=True,
)

st.subheader("전체 장비 주간 비교")
st.dataframe(comparison, hide_index=True, use_container_width=True)

previous_notes = previous_week.loc[
    previous_week["비고"].notna() & previous_week["비고"].str.strip().ne("")
].assign(주차="W44 · 지난주")
current_notes = current_week.loc[
    current_week["비고"].notna() & current_week["비고"].str.strip().ne("")
].assign(주차="W45 · 이번 주")
notes = pd.concat([previous_notes, current_notes], ignore_index=True)

st.subheader("비고가 있는 행")
if notes.empty:
    st.info("비고가 입력된 행이 없습니다.")
else:
    st.dataframe(
        notes[["주차", "일자", "장비코드", "장비명", "비고"]],
        hide_index=True,
        use_container_width=True,
    )
