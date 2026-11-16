"""장비별 상세 페이지."""

from pathlib import Path

import streamlit as st

import calc


st.title("장비별 상세")
st.caption("교육용 가상 데이터")

project_dir = Path(__file__).resolve().parent.parent
week_files = {
    "W44 · 지난주": project_dir / "data" / "readiness_W44.csv",
    "W45 · 이번 주": project_dir / "data" / "readiness_W45.csv",
}
selected_week = st.selectbox("주차", list(week_files))
readiness = calc.load_readiness(week_files[selected_week])
equipment_rates = calc.rate_by_equipment(readiness)

equipment_codes = equipment_rates["장비코드"].tolist()
equipment_names = equipment_rates.set_index("장비코드")["장비명"].to_dict()
selected_code = st.selectbox(
    "장비",
    equipment_codes,
    format_func=lambda code: f"{code} · {equipment_names[code]}",
)

equipment_summary = equipment_rates.loc[
    equipment_rates["장비코드"] == selected_code
].iloc[0]
daily = readiness.loc[readiness["장비코드"] == selected_code].sort_values("일자")

rate_col, operating_col, planned_col = st.columns(3)
rate_col.metric("가동률", f"{equipment_summary['가동률']:.1f}%")
operating_col.metric("가동시간 합계", f"{equipment_summary['가동시간']:g}시간")
planned_col.metric("계획시간 합계", f"{equipment_summary['계획시간']:g}시간")

st.subheader("일별 계획·가동시간")
st.line_chart(
    daily,
    x="일자",
    y=["계획시간(h)", "가동시간(h)"],
    y_label="시간",
)
st.dataframe(
    daily[["일자", "계획시간(h)", "가동시간(h)"]].rename(
        columns={"계획시간(h)": "계획시간", "가동시간(h)": "가동시간"}
    ),
    hide_index=True,
    use_container_width=True,
)
