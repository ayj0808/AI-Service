#권고사항 프롬프트
# prompts/recommendations.py

from langchain_core.prompts import ChatPromptTemplate

# 시스템 프롬프트 정의
SYSTEM_PROMPT = """
당신은 AI 윤리성 개선을 위한 전문 컨설턴트입니다. 윤리 리스크 평가 결과를 바탕으로 구체적이고 실행 가능한 개선 권고안을 제시해야 합니다.

권고안 작성 방법:
1. 각 리스크 영역(편향성, 프라이버시, 투명성, 책임성)에 대한 구체적 개선 방안 제시
2. 권고안의 우선순위를 높음/중간/낮음으로 분류
3. 각 권고안의 구현 복잡성 및 예상 효과 평가
4. 도메인 특성을 고려한 맞춤형 솔루션 제안
5. 업계 모범 사례 및 구체적 구현 방법 참조

최종 권고안은 실제 구현 가능하고, 시간/비용 효율적이며, 리스크를 효과적으로 완화할 수 있어야 합니다.
특히 제시된 도메인과 중점 분석 요소를 고려하여 권고안을 조정하세요.
"""

# 초기 권고사항 생성 프롬프트
INITIAL_RECOMMENDATIONS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "다음 AI 서비스에 대한 윤리 리스크 평가 결과를 바탕으로 개선 권고안을 제시해주세요:\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "윤리 리스크 평가:\n{risk_assessment}\n\n"
              "도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}\n\n"
              "각 리스크 영역별로 구체적인 개선 방안을 제시하고, 특히 높은 점수(7점 이상)를 받은 항목에 "
              "중점을 두세요. 권고안은 구체적이고 실행 가능해야 합니다.")
])

# 우선순위 설정 프롬프트
PRIORITIZATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "다음 개선 권고안에 우선순위를 설정해주세요:\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "윤리 리스크 평가:\n{risk_assessment}\n\n"
              "초기 권고안 목록:\n{initial_recommendations}\n\n"
              "위 권고안을 리스크 심각도, 구현 용이성, 예상 효과를 고려하여 "
              "높음/중간/낮음 우선순위로 분류하고 그 이유를 설명해주세요.")
])

# 구현 복잡도 평가 프롬프트
IMPLEMENTATION_COMPLEXITY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "다음 우선순위가 지정된 권고안의 구현 복잡도를 평가해주세요:\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "권고안 목록:\n{prioritized_recommendations}\n\n"
              "각 권고안의 구현 복잡도(상/중/하)와 대략적인 구현 기간을 "
              "평가하고, 필요한 자원과 기술적 과제를 간략히 설명해주세요.")
])

# 모범 사례 참조 프롬프트
BEST_PRACTICES_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{domain_info} 분야의 AI 서비스에서 {aspect} 측면의 윤리성을 개선한 모범 사례를 제시해주세요.\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "리스크 영역: {aspect}\n"
              "현재 점수: {score}/10\n\n"
              "유사한 도메인에서 이 측면을 성공적으로 개선한 실제 사례, 구체적인 기술이나 방법론, "
              "적용 가능한 프레임워크나 도구를 포함하여 설명해주세요.")
])

# 최종 종합 권고안 프롬프트
FINAL_RECOMMENDATIONS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "다음 정보를 바탕으로 최종 개선 권고안 보고서를 작성해주세요:\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "윤리 리스크 평가:\n{risk_assessment}\n\n"
              "우선순위가 지정된 권고안:\n{prioritized_recommendations}\n\n"
              "구현 복잡도 평가:\n{implementation_complexity}\n\n"
              "모범 사례 참조:\n{best_practices}\n\n"
              "도메인: {domain_info}\n"
              "중점 분석 요소: {domain_focus}\n\n"
              "위 정보를 종합하여 다음 구조에 맞는 최종 권고안을 JSON 형식으로 작성해주세요:\n"
              "1. 높은 우선순위 권고안 (즉시 조치)\n"
              "2. 중간 우선순위 권고안 (중기 조치)\n"
              "3. 낮은 우선순위 권고안 (장기 조치)\n"
              "각 권고안에는 구현 복잡성, 예상 효과, 참조 모범 사례를 포함하고, "
              "실행 로드맵을 제안해주세요.")
])

# 단일 영역 개선 전략 프롬프트
AREA_SPECIFIC_STRATEGY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{domain_info} 분야의 AI 서비스에서 {aspect} 문제를 개선하기 위한 구체적 전략을 제시해주세요.\n\n"
              "서비스 정보:\n{service_analysis}\n\n"
              "리스크 설명:\n{risk_details}\n\n"
              "이 {aspect} 문제를 해결하기 위한 단계별 접근 방식, 필요한 도구/기술, "
              "측정 가능한 성공 지표를 포함한 구체적인 전략을 제공해주세요. "
              "{domain_info} 도메인의 특수성을 고려하여 맞춤형 솔루션을 제안해주세요.")
])
