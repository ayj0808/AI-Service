#서비스 분석 프롬프트
# prompts/service_analysis.py

from langchain_core.prompts import ChatPromptTemplate

# 시스템 프롬프트 정의
SYSTEM_PROMPT = """
당신은 AI 윤리성 리스크 진단을 위해 AI 서비스를 분석하는 전문가입니다.
사용자가 제공하는 AI 서비스에 대해 필요한 정보를 수집하고 체계적으로 분석하세요.

당신의 역할은:
1. 서비스의 기본 정보 수집 (이름, 제공업체, 주요 기능 등)
2. 사용되는 데이터 유형 파악
3. 의사결정 프로세스 이해
4. 기술적 아키텍처 정보 수집
5. 대상 사용자 및 배포 컨텍스트 파악

중요: 사용자가 언급한 도메인(예: 의료, 금융, 교육)과 중점 분석 요소를 특별히 고려하세요.
필요한 정보가 부족할 경우 사용자에게 추가 질문을 해야 합니다.
모든 수집된 정보는 체계적으로 정리하여 JSON 형식으로 반환하세요.
"""

# 초기 정보 수집 프롬프트
INFO_COLLECTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "분석할 AI 서비스: {service_name}\n"
              "서비스 도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}")
])

# 후속 질문 프롬프트
FOLLOW_UP_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "지금까지 수집된 {service_name}에 대한 정보는 다음과 같습니다:\n{current_info}\n\n"
              "도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}\n\n"
              "아직 필요한 정보가 부족합니다. 어떤 추가 질문을 해야 할까요? "
              "특히 {domain_info} 도메인에서 중요한 {domain_focus}와 관련된 정보를 얻기 위한 "
              "가장 중요한 3가지 질문을 제시해주세요.")
])

# 최종 분석 프롬프트
FINAL_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "지금까지 수집된 {service_name}에 대한 정보는 다음과 같습니다:\n{collected_info}\n\n"
              "도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}\n\n"
              "이 정보를 바탕으로 체계적인 서비스 분석 결과를 JSON 형식으로 제공해주세요.")
])

# 추가 정보 요청 프롬프트
MISSING_INFO_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "현재 {service_name}에 대해 다음 정보가 수집되었습니다:\n"
             "{existing_analysis}\n\n"
             "윤리 리스크 평가를 위해 추가로 필요한 정보가 있다면 질문해주세요.")
])
