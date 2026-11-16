"""전체 가동률 요약 페이지."""

from pathlib import Path

import streamlit as st

import calc


st.title("장비 가동률 요약")
st.caption("교육용 가상 데이터")

project_dir = Path(__file__).resolve().parent.parent
previous_week = calc.load_readiness(project_dir / "data" / "readiness_W44.csv")
current_week = calc.load_readiness(project_dir / "data" / "readiness_W45.csv")

previous_rate = calc.total_rate(previous_week)
current_rate = calc.total_rate(current_week)
week_change = round(current_rate - previous_rate, 1)
goal_difference = round(current_rate - 90.0, 1)

current_col, previous_col, goal_col = st.columns(3)
current_col.metric(
    "이번 주 전체 가동률",
    f"{current_rate:.1f}%",
    delta=f"{week_change:+.1f}%p 전주 대비",
)
previous_col.metric("지난주 전체 가동률", f"{previous_rate:.1f}%")
goal_col.metric("90% 목표 대비", f"{goal_difference:+.1f}%p")

st.subheader("장비별 이번 주 가동률")
equipment_rates = calc.rate_by_equipment(current_week)
st.bar_chart(equipment_rates, x="장비명", y="가동률", y_label="가동률 (%)")
