"""Streamlit 앱 진입점과 페이지 내비게이션."""

import streamlit as st

import db


db.init_db()

pages = st.navigation(
    [
        st.Page("pages/summary.py", title="요약", default=True),
        st.Page("pages/equipment.py", title="장비별 상세"),
        st.Page("pages/weekly_compare.py", title="주간 비교"),
        st.Page("pages/maintenance.py", title="정비 요청"),
    ]
)
pages.run()
