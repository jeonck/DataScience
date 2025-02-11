import streamlit as st
import requests
import json
 
# Streamlit 페이지 제목
st.title("Apache Pinot Schema 추가하기")
 
# 사용자 입력을 위한 폼 생성
with st.form(key='schema_form'):
    schema_name = st.text_input("스키마 이름", "mySchema")
     
    # 차원 필드 입력
    dimension_fields = st.text_area("차원 필드 (JSON 형식)",
                                      '[{"name": "playerName", "dataType": "STRING"}, {"name": "team", "dataType": "STRING"}]')
     
    # 메트릭 필드 입력
    metric_fields = st.text_area("메트릭 필드 (JSON 형식)",
                                   '[{"name": "gamesPlayed", "dataType": "INT"}]')
     
    submit_button = st.form_submit_button("스키마 추가")
 
# 스키마 추가 요청 처리
if submit_button:
    # 스키마 JSON 구성
    schema = {
        "schemaName": schema_name,
        "dimensionFieldSpecs": json.loads(dimension_fields),
        "metricFieldSpecs": json.loads(metric_fields)
    }
     
    # Pinot API 호출
    response = requests.post("http://localhost:9000/schemas", json=schema)
     
    # 결과 출력
    if response.status_code == 200:
        st.success("스키마가 성공적으로 추가되었습니다!")
    else:
        st.error(f"스키마 추가 실패: {response.text}")
