#서비스 분석 에이전트
#service_analyzer.py
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from tools.web_search import WebSearchTool
import json

# 프롬프트 파일에서 상수 임포트
from prompts.service_analysis import (
    INFO_COLLECTION_PROMPT, 
    FOLLOW_UP_PROMPT, 
    FINAL_ANALYSIS_PROMPT
)

class ServiceAnalyzer:
    """AI 서비스의 기본 정보를 수집하고 분석하는 에이전트"""

    def __init__(self, model_name="gpt-4o-mini"):
        # LLM 모델 초기화
        self.llm = ChatOpenAI(model=model_name, temperature=0.2)
        self.web_search = WebSearchTool()  # 웹 검색 도구 추가
    
    def auto_analyze_service (self, service_name: str, domain_info: str, domain_focus: str) -> Dict[str, Any]:
        """웹 검색 결과를 활용한 서비스 분석"""
        
        # 웹 검색 수행
        print(f"🔎 '{service_name}'에 대한 정보 검색 중...")
        search_results = self.web_search.search_service_info(service_name, domain_info)
        
        # 검색 결과를 포함한 프롬프트 작성
        prompt = f"""
        다음은 {service_name}에 관한 검색 결과입니다:
        
        {search_results}
        
        위 정보를 바탕으로 {domain_info} 도메인의 {service_name}에 대해 분석하고,
        서비스 제공업체, 주요 기능, 사용 데이터, 의사결정 과정 등에 대한 정보를 JSON 형식으로 제공해주세요.
        특히 {domain_focus} 측면에 주목해주세요.
        """
        
        # 검색 결과를 활용한 분석 수행
        response = self.llm.invoke(prompt)
        
        # 정보 수집 (검색 결과 포함)
        collected_info = {
            "web_search_results": search_results,
            "initial_analysis": response.content
        }
        
        # 최종 분석 수행
        final_response = self.llm.invoke(
            FINAL_ANALYSIS_PROMPT.format(
                service_name=service_name,
                collected_info=json.dumps(collected_info, ensure_ascii=False),
                domain_info=domain_info,
                domain_focus=domain_focus
            )
        )
        
        # JSON 응답 추출
        try:
            content = final_response.content
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                result = json.loads(json_str)
                result["service_name"] = service_name
                return result
            else:
                return self._create_default_analysis(service_name)
        except:
            return self._create_default_analysis(service_name)
    
    def _create_default_analysis(self, service_name: str) -> Dict[str, Any]:
        """기본 서비스 분석 정보 생성"""
        return {
            "service_name": service_name,
            "service_provider": "알 수 없음",
            "target_functionality": ["주요 기능 알 수 없음"],
            "data_types": ["알 수 없음"],
            "decision_processes": ["알 수 없음"],
            "technical_architecture": "알 수 없음",
            "user_groups": ["알 수 없음"],
            "deployment_context": "알 수 없음"
        }

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """전체 서비스 분석 프로세스 실행"""
        
        # 필요 정보 추출
        service_name = state.get("service_name", "")
        domain_info = state.get("domain_info", "일반")
        domain_focus = state.get("domain_focus", "모든 측면")
        
        # 자동 분석 수행
        analysis_result = self.auto_analyze_service(service_name, domain_info, domain_focus)
        
        # 상태 업데이트
        state["service_analysis"] = analysis_result
        
        return state

