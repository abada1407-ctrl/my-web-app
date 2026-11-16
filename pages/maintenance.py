"""정비 요청 접수와 관리 페이지."""

from pathlib import Path

import streamlit as st

import calc
import db


st.title("정비 요청")
st.caption("교육용 가상 데이터")
st.caption(f"현재 저장소: {db.backend_name()}")

project_dir = Path(__file__).resolve().parent.parent
current_week = calc.load_readiness(project_dir / "data" / "readiness_W45.csv")
equipment_options = list(
    dict.fromkeys(zip(current_week["장비코드"], current_week["장비명"]))
)
equipment_names = {code: name for code, name in equipment_options}

st.subheader("정비 요청 등록")
with st.form("maintenance_request_form", clear_on_submit=True):
    equipment_code = st.selectbox(
        "장비",
        [code for code, _ in equipment_options],
        format_func=lambda code: f"{code} · {equipment_names[code]}",
    )
    request_title = st.text_area("요청 내용")
    priority = st.selectbox("우선순위", db.PRIORITIES)
    requester_role = st.text_input("요청자 역할명")
    submitted = st.form_submit_button("요청 등록")

if submitted:
    request_id = db.add_request(
        equipment_code=equipment_code,
        title=request_title,
        priority=priority,
        requester_role=requester_role,
    )
    st.success(f"정비 요청 {request_id}번을 등록했습니다.")
    st.rerun()

st.subheader("정비 요청 목록")
selected_status = st.selectbox("상태 필터", ["전체", *db.STATUSES])
requests = db.list_requests(status=None if selected_status == "전체" else selected_status)

if requests.empty:
    st.info("해당하는 정비 요청이 없습니다.")
else:
    st.dataframe(requests, hide_index=True, use_container_width=True)

    st.subheader("요청 상태 변경")
    request_ids = requests["id"].tolist()
    with st.form("maintenance_status_form"):
        request_id = st.selectbox("요청 번호", request_ids)
        new_status = st.selectbox("변경할 상태", db.STATUSES)
        update_submitted = st.form_submit_button("상태 변경")

    if update_submitted:
        db.update_status(int(request_id), new_status)
        st.success(f"{request_id}번 요청 상태를 '{new_status}'(으)로 변경했습니다.")
        st.rerun()
