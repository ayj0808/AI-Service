#메인 실행 파일
# 메인 실행 파일
from langgraph.graph import StateGraph
from typing import TypedDict, Dict, Any, Optional, List
from langchain_core.messages import AIMessage, HumanMessage

from agents.service_analyzer import ServiceAnalyzer
from agents.risk_assessor import RiskAssessor
from agents.recommender import Recommender
from agents.report_generator import ReportGenerator
from tools.domain_adapter import DomainAdapter
from dotenv import load_dotenv
load_dotenv()

# 상태 타입 정의
class StateType(TypedDict):
    service_name: str
    domain_info: str
    domain_focus: str
    service_analysis: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    recommendations: Dict[str, Any]
    report_generation: Dict[str, Any]
    feedback_required: Optional[bool]

def main():
    """
    AI 윤리성 리스크 진단 시스템의 메인 함수
    """
    print("=== AI 윤리성 리스크 진단 시스템 ===")
    
    # 사용자 입력 받기
    service_name = input("분석할 AI 서비스 이름을 입력하세요: ")
    domain_info = input("해당 서비스의 도메인 정보를 입력하세요 (예: '의료', '금융', '교육' 등): ")
    domain_focus = input("해당 도메인에서 중점적으로 봐야 할 윤리적 측면이 있다면 알려주세요\n ('편향성','프라이버시','투명성','책임성'): ")
    
    # 초기 상태 설정
    initial_state = {
        "service_name": service_name,
        "domain_info": domain_info,
        "domain_focus": domain_focus,
        "service_analysis": {},
        "risk_assessment": {},
        "recommendations": {},
        "report_generation": {}
    }
    
    # 에이전트 초기화
    service_analyzer = ServiceAnalyzer()
    domain_adapter = DomainAdapter()
    risk_assessor = RiskAssessor()
    recommender = Recommender()
    report_generator = ReportGenerator()
    
    # 에이전트 그래프 구성 - TypedDict 사용
    graph = StateGraph(StateType)
    
    # 노드 추가
    graph.add_node("service_analyzer", service_analyzer.run)
    graph.add_node("domain_adapter", domain_adapter.adapt)
    graph.add_node("risk_assessor", risk_assessor.assess)
    graph.add_node("recommender", recommender.recommend)
    graph.add_node("report_generator", report_generator.generate)
    
    # 시작점 설정 (entry point)
    graph.set_entry_point("service_analyzer")
    
    # 엣지 추가 (순차적 흐름)
    graph.add_edge("service_analyzer", "domain_adapter")
    graph.add_edge("domain_adapter", "risk_assessor")
    graph.add_edge("risk_assessor", "recommender")
    graph.add_edge("recommender", "report_generator")
    
    # 피드백 루프 추가
    graph.add_conditional_edges(
    "risk_assessor",
    lambda x: "service_analyzer" if x.get("feedback_required") else "recommender")
    
    # 그래프 컴파일
    workflow = graph.compile()
    
    # 실행
    print(f"\n'{service_name}' 서비스에 대한 분석을 시작합니다...")
    result = workflow.invoke(initial_state)
    
    print("\n분석이 완료되었습니다. 결과 보고서는 outputs/reports/ 디렉토리에 저장되었습니다.")
    return result

if __name__ == "__main__":
    main()
