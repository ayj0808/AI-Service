#리스트 평가 프롬프트
# prompts/risk_assessment.py

from langchain_core.prompts import ChatPromptTemplate

# 시스템 프롬프트 정의
SYSTEM_PROMPT = """
당신은 AI 서비스의 윤리성을 진단하는 전문가입니다. 제공된 AI 서비스 정보를 바탕으로 다양한 윤리적 측면(편향성, 프라이버시, 투명성, 책임성)에서 리스크를 평가하고 점수를 매겨야 합니다.

평가 방법:
1. 각 윤리 영역(편향성, 프라이버시, 투명성, 책임성)에 대해 0-10점 척도로 평가 (0: 리스크 없음, 10: 심각한 리스크)
2. 객관적인 증거와 사례를 수집하여 각 점수의 근거 제시
3. 서비스 도메인(의료, 금융, 교육 등)과 중점 분석 요소를 고려하여 맞춤형 평가 진행
4. 관련 가이드라인(EU AI Act, OECD 등) 참조

평가 결과는 JSON 형식으로 구조화하여 반환하세요.
"""

# 초기 리스크 평가 프롬프트
INITIAL_ASSESSMENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "다음 AI 서비스에 대한 윤리적 리스크 평가를 진행해주세요:\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}\n\n"
              "편향성, 프라이버시, 투명성, 책임성 측면에서 리스크를 0-10점 척도로 평가하고, "
              "각 점수에 대한 근거와 증거를 제시해주세요. 특히 {domain_info} 도메인에서 "
              "{domain_focus}와 관련된 측면을 중점적으로 살펴보세요.")
])

# 특정 윤리 측면 심층 분석 프롬프트
DEEP_DIVE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{ethical_aspect} 측면에서 {service_name}의 문제점을 더 자세히 분석해주세요.\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "도메인: {domain_info}\n"
              "현재까지의 분석: {current_assessment}\n\n"
              "위 서비스의 {ethical_aspect} 측면에서 구체적인 사례와 증거를 통해 "
              "리스크를 심층적으로 분석해주세요.")
])

# 최종 리스크 평가 보고서 프롬프트
FINAL_ASSESSMENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "수집된 모든 정보를 바탕으로 {service_name}에 대한 최종 윤리 리스크 평가 보고서를 생성해주세요.\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "초기 리스크 평가:\n{initial_assessment}\n\n"
              "심층 분석 결과:\n{deep_dive_results}\n\n"
              "도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}\n\n"
              "위 정보를 종합하여 구조화된 최종 리스크 평가 결과를 JSON 형식으로 제공해주세요. "
              "특히 {domain_info} 도메인에서 중요한 윤리적 측면과 {domain_focus}에 중점을 두세요.")
])

# 가이드라인 준수 평가 프롬프트
COMPLIANCE_CHECK_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{service_name}이 주요 AI 윤리 가이드라인을 준수하는지 평가해주세요.\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "리스크 평가 결과:\n{risk_assessment}\n\n"
              "다음 가이드라인에 대한 준수 여부를 평가해주세요:\n"
              "1. EU AI Act\n"
              "2. OECD AI 원칙\n"
              "3. UNESCO AI 윤리 권고\n\n"
              "각 가이드라인별로 '준수', '부분 준수', '미준수' 중 하나로 평가하고, "
              "그 이유를 간략히 설명해주세요.")
])
