#보고서 생성 프롬프트
# prompts/report_generation.py

from langchain_core.prompts import ChatPromptTemplate

# 시스템 프롬프트 정의
SYSTEM_PROMPT = """
당신은 AI 윤리성 리스크 진단 보고서를 작성하는 전문가입니다. 서비스 분석, 리스크 진단, 개선 권고안 정보를 바탕으로 체계적이고 전문적인 최종 보고서를 작성해야 합니다.

보고서 작성 원칙:
1. 명확하고 간결한 전문적 문체 사용
2. 핵심 정보를 눈에 띄게 강조
3. 논리적이고 체계적인 흐름 유지
4. 발견사항과 권고사항 간의 명확한 연결성 제시
5. 전문가도 이해할 수 있는 깊이와 비전문가도 파악할 수 있는 명확성 균형

도메인 특성과 중점 분석 요소를 충분히 고려하여 맞춤형 보고서를 작성하세요.
"""

# 보고서 구조 정의 프롬프트
REPORT_STRUCTURE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "다음 AI 서비스에 대한 윤리 리스크 진단 보고서의 구조를 설계해주세요:\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "리스크 평가:\n{risk_assessment}\n\n"
              "개선 권고안:\n{recommendations}\n\n"
              "도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}\n\n"
              "체계적이고 논리적인 보고서 목차와 각 섹션에 포함될 주요 내용을 제안해주세요. "
              "특히 {domain_info} 도메인의 특성과 {domain_focus}에 중점을 두세요.")
])

# 요약(SUMMARY) 작성 프롬프트
EXECUTIVE_SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{service_name}에 대한 윤리 리스크 진단 보고서의 요약(Executive Summary)을 작성해주세요.\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "리스크 평가:\n{risk_assessment}\n\n"
              "개선 권고안:\n{recommendations}\n\n"
              "도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}\n\n"
              "200-300단어 내외로 다음을 포함하는 명확하고 간결한 요약을 작성하세요:\n"
              "1. 주요 발견사항\n"
              "2. 핵심 리스크 영역\n"
              "3. 우선적 권고사항\n"
              "4. 전반적 평가 결론")
])

# 서론 섹션 작성 프롬프트
INTRODUCTION_SECTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{service_name}에 대한 윤리 리스크 진단 보고서의 서론 섹션을 작성해주세요.\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}\n\n"
              "다음 내용을 포함하는 서론을 작성하세요:\n"
              "1. 진단 목적 및 범위\n"
              "2. 적용된 윤리 가이드라인\n"
              "3. 진단 방법론 개요\n"
              "4. {domain_info} 도메인에서 AI 윤리의 중요성")
])

# 서비스 개요 섹션 작성 프롬프트
SERVICE_OVERVIEW_SECTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{service_name}에 대한 윤리 리스크 진단 보고서의 서비스 개요 섹션을 작성해주세요.\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}\n\n"
              "다음 내용을 포함하는 서비스 개요를 작성하세요:\n"
              "1. 서비스 목적 및 기능\n"
              "2. 주요 특징 및 기술 아키텍처\n"
              "3. 사용자 그룹 및 사용 사례\n"
              "4. {domain_info} 도메인에서 해당 서비스의 의미")
])

# 리스크 평가 섹션 작성 프롬프트
RISK_ASSESSMENT_SECTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{service_name}에 대한 윤리 리스크 진단 보고서의 리스크 평가 섹션을 작성해주세요.\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "리스크 평가:\n{risk_assessment}\n\n"
              "도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}\n\n"
              "다음 윤리적 측면에 대한 상세한 리스크 평가를 작성하세요:\n"
              "1. 편향성 및 공정성 (점수: {bias_score}/10)\n"
              "2. 프라이버시 및 데이터 보호 (점수: {privacy_score}/10)\n"
              "3. 투명성 및 설명가능성 (점수: {transparency_score}/10)\n"
              "4. 책임성 및 거버넌스 (점수: {accountability_score}/10)\n\n"
              "각 영역에 대해 주요 발견사항, 증거, 잠재적 영향을 설명하고, "
              "{domain_info} 도메인에서 특히 중요한 {domain_focus}에 관련된 측면을 강조하세요.")
])

# 규정 준수 섹션 작성 프롬프트
COMPLIANCE_SECTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{service_name}에 대한 주요 AI 윤리 가이드라인 준수 상태를 설명하는 섹션을 작성해주세요.\n\n"
              "리스크 평가:\n{risk_assessment}\n\n"
              "가이드라인 준수 상태:\n{compliance_status}\n\n"
              "도메인: {domain_info}\n\n"
              "다음 가이드라인에 대한 준수 상태를 상세히 설명하세요:\n"
              "1. EU AI Act\n"
              "2. OECD AI 원칙\n"
              "3. UNESCO AI 윤리 권고\n\n"
              "각 가이드라인별로 준수 상태(준수/부분 준수/미준수)와 그 이유, "
              "그리고 {domain_info} 도메인에서 특히 중요한 규제적 측면을 설명하세요.")
])

# 권고사항 섹션 작성 프롬프트
RECOMMENDATIONS_SECTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{service_name}에 대한 윤리 리스크 진단 보고서의 개선 권고안 섹션을 작성해주세요.\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "리스크 평가:\n{risk_assessment}\n\n"
              "개선 권고안:\n{recommendations}\n\n"
              "도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}\n\n"
              "우선순위별로 구분하여 권고안을 상세히 설명하세요:\n"
              "1. 단기 개선 사항 (0-3개월): 높은 우선순위 권고안\n"
              "2. 중기 개선 사항 (3-6개월): 중간 우선순위 권고안\n"
              "3. 장기 개선 사항 (6-12개월): 낮은 우선순위 권고안\n\n"
              "각 권고안에 대해 구현 방법, 예상 효과, 필요한 자원을 설명하고, "
              "특히 {domain_info} 도메인에서 {domain_focus}와 관련된 측면에 중점을 두세요.")
])

# 결론 섹션 작성 프롬프트
CONCLUSION_SECTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{service_name}에 대한 윤리 리스크 진단 보고서의 결론 섹션을 작성해주세요.\n\n"
              "리스크 평가:\n{risk_assessment}\n\n"
              "개선 권고안:\n{recommendations}\n\n"
              "도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}\n\n"
              "다음 내용을 포함하는 결론을 작성하세요:\n"
              "1. 전반적 윤리적 성숙도 평가\n"
              "2. 개선을 위한 다음 단계\n"
              "3. 장기적 윤리 전략 방향\n"
              "4. {domain_info} 도메인에서 AI 윤리의 미래 전망")
])

# 시각화 제안 프롬프트
VISUALIZATION_SUGGESTIONS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{service_name}에 대한 윤리 리스크 진단 보고서에 포함할 시각화 요소를 제안해주세요.\n\n"
              "리스크 평가:\n{risk_assessment}\n\n"
              "개선 권고안:\n{recommendations}\n\n"
              "도메인: {domain_info}\n\n"
              "다음과 같은 시각화 요소를 제안하세요:\n"
              "1. 리스크 점수를 보여주는 레이더 차트 또는 막대 그래프\n"
              "2. 우선순위-영향력 매트릭스\n"
              "3. 개선 로드맵 타임라인\n"
              "4. {domain_info} 도메인에 특화된 시각화 요소\n\n"
              "각 시각화에 대한 목적, 포함할 데이터, 디자인 제안을 설명하세요.")
])

# 최종 보고서 생성 프롬프트
FINAL_REPORT_ASSEMBLY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{service_name}에 대한 최종 윤리 리스크 진단 보고서를 조립해주세요.\n\n"
              "다음 섹션들이 제공됩니다:\n\n"
              "---요약---\n{executive_summary}\n\n"
              "---서론---\n{introduction}\n\n"
              "---서비스 개요---\n{service_overview}\n\n"
              "---리스크 평가---\n{risk_assessment_section}\n\n"
              "---규정 준수 상태---\n{compliance_section}\n\n"
              "---개선 권고안---\n{recommendations_section}\n\n"
              "---결론---\n{conclusion}\n\n"
              "---시각화 제안---\n{visualization_suggestions}\n\n"
              "각 리스크 평가에 대한 평균 점수를 결론 옆에 표시해주세요"
              "이 내용을 바탕으로 일관성 있고 전문적인 완전한 보고서를 생성하세요. "
              "필요한 경우 연결 문구를 추가하거나 내용을 조정하여 보고서 전체가 "
              "논리적 흐름을 갖도록 해주세요.")
])
