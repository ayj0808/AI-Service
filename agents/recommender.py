#개선안 제안 에이전트
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
import json

# 프롬프트 임포트
from prompts.recommendations import (
    INITIAL_RECOMMENDATIONS_PROMPT,
    PRIORITIZATION_PROMPT,
    IMPLEMENTATION_COMPLEXITY_PROMPT,
    BEST_PRACTICES_PROMPT,
    FINAL_RECOMMENDATIONS_PROMPT,
    AREA_SPECIFIC_STRATEGY_PROMPT
)

class Recommender:
    """
    AI 서비스의 윤리적 리스크를 개선하기 위한 권고안을 제시하는 에이전트
    """

    def __init__(self, model_name="gpt-4o-mini"):
        # LLM 모델 초기화
        self.llm = ChatOpenAI(model=model_name, temperature=0.2)
        # 윤리적 측면 정의
        self.ethical_aspects = ["bias", "privacy", "transparency", "accountability"]

    def generate_initial_recommendations(self, service_analysis: Dict[str, Any], 
                                      risk_assessment: Dict[str, Any], 
                                      domain_info: str, domain_focus: str) -> Dict[str, Any]:
        """
        리스크 평가 결과를 바탕으로 초기 개선 권고안 생성
        
        Args:
            service_analysis: 서비스 분석 정보
            risk_assessment: 윤리 리스크 평가 결과
            domain_info: 도메인 정보
            domain_focus: 중점 분석 요소
            
        Returns:
            초기 권고안 목록
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        risk_assessment_str = json.dumps(risk_assessment, ensure_ascii=False, indent=2)
        
        # 초기 권고안 생성 요청
        response = self.llm.invoke(
            INITIAL_RECOMMENDATIONS_PROMPT.format(
                service_analysis=service_analysis_str,
                risk_assessment=risk_assessment_str,
                domain_info=domain_info,
                domain_focus=domain_focus
            )
        )
        
        try:
            # JSON 형식 응답 추출 시도
            content = response.content
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                # 구조화되지 않은 경우 텍스트 형태로 저장
                result = {
                    "recommendations_text": content,
                    "structured": False
                }
                
            return result
            
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 텍스트 형태로 저장
            return {
                "recommendations_text": response.content,
                "structured": False
            }

    def prioritize_recommendations(self, service_analysis: Dict[str, Any], 
                                risk_assessment: Dict[str, Any], 
                                initial_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """
        생성된 권고안에 우선순위 부여
            
        Returns:
            우선순위가 부여된 권고안
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        risk_assessment_str = json.dumps(risk_assessment, ensure_ascii=False, indent=2)
        initial_recommendations_str = json.dumps(initial_recommendations, ensure_ascii=False, indent=2)
        
        # 우선순위 설정 요청
        response = self.llm.invoke(
            PRIORITIZATION_PROMPT.format(
                service_analysis=service_analysis_str,
                risk_assessment=risk_assessment_str,
                initial_recommendations=initial_recommendations_str #initial_recommendations: 초기 권고안
            )
        )
        
        try:
            # JSON 형식 응답 추출 시도
            content = response.content
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                # 구조화되지 않은 경우
                result = {
                    "high_priority": [],
                    "medium_priority": [],
                    "low_priority": [],
                    "prioritization_text": content
                }
                
            return result
            
        except json.JSONDecodeError:
            # 파싱 실패 시
            return {
                "high_priority": [],
                "medium_priority": [],
                "low_priority": [],
                "prioritization_text": response.content
            }

    def evaluate_implementation_complexity(self, service_analysis: Dict[str, Any], 
                                         prioritized_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """
        권고안의 구현 복잡도 평가
        Args:
            prioritized_recommendations: 우선순위가 부여된 권고안
        Returns:
            구현 복잡도가 평가된 권고안
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        prioritized_recommendations_str = json.dumps(prioritized_recommendations, ensure_ascii=False, indent=2)
        
        # 구현 복잡도 평가 요청
        response = self.llm.invoke(
            IMPLEMENTATION_COMPLEXITY_PROMPT.format(
                service_analysis=service_analysis_str,
                prioritized_recommendations=prioritized_recommendations_str
            )
        )
        
        try:
            # JSON 형식 응답 추출 시도
            content = response.content
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                # 구조화되지 않은 경우
                result = {
                    "implementation_complexity": {},
                    "complexity_text": content
                }
                
            return result
            
        except json.JSONDecodeError:
            # 파싱 실패 시
            return {
                "implementation_complexity": {},
                "complexity_text": response.content
            }

    def get_best_practices(self, service_analysis: Dict[str, Any], aspect: str, 
                         score: int, domain_info: str) -> Dict[str, Any]:
        """
        특정 윤리적 측면에 대한 모범 사례 제공
        
        Args:
            aspect: 윤리적 측면(bias, privacy 등)
            score: 현재 리스크 점수
            
        Returns:
            모범 사례 정보
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        
        # 윤리적 측면 한글화
        aspect_korean = {
            "bias": "편향성",
            "privacy": "프라이버시",
            "transparency": "투명성",
            "accountability": "책임성"
        }.get(aspect, aspect)
        
        # 모범 사례 요청
        response = self.llm.invoke(
            BEST_PRACTICES_PROMPT.format(
                domain_info=domain_info,
                aspect=aspect_korean,
                service_analysis=service_analysis_str,
                score=score
            )
        )
        
        # 결과 반환
        return {
            "aspect": aspect,
            "best_practices": response.content
        }

    def create_area_specific_strategy(self, service_analysis: Dict[str, Any], 
                                   aspect: str, risk_details: str, 
                                   domain_info: str) -> Dict[str, Any]:
        """
        특정 윤리적 측면에 대한 맞춤형 개선 전략 생성
        
        Args:
            risk_details: 해당 측면의 리스크 상세 설명
        Returns:
            맞춤형 개선 전략
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        
        # 윤리적 측면 한글화
        aspect_korean = {
            "bias": "편향성",
            "privacy": "프라이버시",
            "transparency": "투명성",
            "accountability": "책임성"
        }.get(aspect, aspect)
        
        # 맞춤형 전략 요청
        response = self.llm.invoke(
            AREA_SPECIFIC_STRATEGY_PROMPT.format(
                domain_info=domain_info,
                aspect=aspect_korean,
                service_analysis=service_analysis_str,
                risk_details=risk_details
            )
        )
        
        # 결과 반환
        return {
            "aspect": aspect,
            "specific_strategy": response.content
        }

    def generate_final_recommendations(self, service_analysis: Dict[str, Any], 
                                    risk_assessment: Dict[str, Any],
                                    prioritized_recommendations: Dict[str, Any],
                                    implementation_complexity: Dict[str, Any],
                                    best_practices: List[Dict[str, Any]],
                                    domain_info: str, domain_focus: str) -> Dict[str, Any]:
        """
        모든 정보를 종합하여 최종 권고안 보고서 생성          
        Returns:
            최종 권고안 보고서
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        risk_assessment_str = json.dumps(risk_assessment, ensure_ascii=False, indent=2)
        prioritized_recommendations_str = json.dumps(prioritized_recommendations, ensure_ascii=False, indent=2)
        implementation_complexity_str = json.dumps(implementation_complexity, ensure_ascii=False, indent=2)
        best_practices_str = json.dumps(best_practices, ensure_ascii=False, indent=2)
        
        # 최종 권고안 생성 요청
        response = self.llm.invoke(
            FINAL_RECOMMENDATIONS_PROMPT.format(
                service_analysis=service_analysis_str,
                risk_assessment=risk_assessment_str,
                prioritized_recommendations=prioritized_recommendations_str,
                implementation_complexity=implementation_complexity_str,
                best_practices=best_practices_str,
                domain_info=domain_info,
                domain_focus=domain_focus
            )
        )
        
        try:
            # JSON 형식 응답 추출 시도
            content = response.content
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                # 구조화되지 않은 경우
                result = {
                    "high_priority": [],
                    "medium_priority": [],
                    "low_priority": [],
                    "implementation_complexity": {},
                    "expected_impact": {},
                    "best_practices": {},
                    "recommendations_text": content
                }
                
            return result
            
        except json.JSONDecodeError:
            # 파싱 실패 시
            return {
                "high_priority": [],
                "medium_priority": [],
                "low_priority": [],
                "implementation_complexity": {},
                "expected_impact": {},
                "best_practices": {},
                "recommendations_text": response.content
            }

    def recommend(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        전체 권고안 생성 프로세스 실행
        
        Args:
            state: 현재 시스템 상태
            
        Returns:
            업데이트된 시스템 상태
        """
        # 상태에서 필요한 정보 추출
        service_analysis = state.get("service_analysis", {})
        risk_assessment = state.get("risk_assessment", {})
        service_name = service_analysis.get("service_name", state.get("service_name", ""))
        domain_info = state.get("domain_info", "일반")
        domain_focus = state.get("domain_focus", "모든 측면")
        
        # 서비스 정보와 리스크 평가 결과가 충분한지 확인
        if not service_analysis or not risk_assessment or not service_name:
            print("⚠️ 서비스 분석 또는 리스크 평가 정보가 부족합니다.")
            return state
        
        print(f"\n🔍 '{service_name}' 서비스의 윤리적 개선 권고안 생성을 시작합니다...")
        print(f"📊 도메인: {domain_info} | 중점 분석 요소: {domain_focus}")
        
        # 1. 초기 권고안 생성
        print("\n🧐 초기 개선 권고안 생성 중...")
        initial_recommendations = self.generate_initial_recommendations(
            service_analysis, risk_assessment, domain_info, domain_focus
        )
        
        # 2. 권고안 우선순위 설정
        print("\n📋 권고안 우선순위 설정 중...")
        prioritized_recommendations = self.prioritize_recommendations(
            service_analysis, risk_assessment, initial_recommendations
        )
        
        # 권고안 결과 초기 출력
        if "high_priority" in prioritized_recommendations and prioritized_recommendations["high_priority"]:
            print("\n⚠️ 높은 우선순위 권고안:")
            for i, rec in enumerate(prioritized_recommendations["high_priority"], 1):
                if isinstance(rec, dict) and "recommendation" in rec:
                    print(f"  {i}. {rec['recommendation']}")
                elif isinstance(rec, str):
                    print(f"  {i}. {rec}")
        
        # 3. 구현 복잡도 평가
        print("\n🔄 권고안 구현 복잡도 평가 중...")
        implementation_complexity = self.evaluate_implementation_complexity(
            service_analysis, prioritized_recommendations
        )
        
        # 4. 주요 리스크 영역에 대한 모범 사례 수집
        best_practices = []
        high_risk_areas = []
        
        # 높은 리스크 영역 식별 (점수 7 이상)
        risk_areas = risk_assessment.get("risk_areas", {})
        for aspect in self.ethical_aspects:
            if aspect in risk_areas and risk_areas[aspect].get("score", 0) >= 7:
                high_risk_areas.append(aspect)
        
        if high_risk_areas:
            print("\n📚 주요 리스크 영역에 대한 모범 사례 수집 중...")
            
            for aspect in high_risk_areas:
                print(f"- {aspect.capitalize()} 모범 사례 조사...")
                score = risk_areas[aspect].get("score", 0)
                best_practice = self.get_best_practices(service_analysis, aspect, score, domain_info)
                best_practices.append(best_practice)
                
                # 추가로 맞춤형 개선 전략 생성
                if aspect in risk_areas and "details" in risk_areas[aspect]:
                    risk_details = risk_areas[aspect]["details"]
                    specific_strategy = self.create_area_specific_strategy(
                        service_analysis, aspect, risk_details, domain_info
                    )
                    best_practices.append(specific_strategy)
        
        # 5. 최종 권고안 생성
        print("\n📝 최종 개선 권고안 보고서 생성 중...")
        final_recommendations = self.generate_final_recommendations(
            service_analysis, risk_assessment,
            prioritized_recommendations, implementation_complexity,
            best_practices, domain_info, domain_focus
        )
        
        # 최종 권고안 저장
        recommendations = {
            "high_priority": final_recommendations.get("high_priority", []),
            "medium_priority": final_recommendations.get("medium_priority", []),
            "low_priority": final_recommendations.get("low_priority", []),
            "implementation_complexity": final_recommendations.get("implementation_complexity", {}),
            "expected_impact": final_recommendations.get("expected_impact", {}),
            "best_practices": final_recommendations.get("best_practices", {}),
            "roadmap": final_recommendations.get("roadmap", {})
        }
        
        # 결과 로그
        print(f"\n✅ 윤리 개선 권고안 생성이 완료되었습니다.")
        print(f"📊 높은 우선순위 권고안: {len(recommendations['high_priority'])}개")
        print(f"📊 중간 우선순위 권고안: {len(recommendations['medium_priority'])}개")
        print(f"📊 낮은 우선순위 권고안: {len(recommendations['low_priority'])}개")
        
        # 상태 업데이트
        state["recommendations"] = recommendations
        
        return state


# 단독 테스트용 코드
if __name__ == "__main__":
    recommender = Recommender()
    
    # 테스트용 서비스 분석 및 리스크 평가 정보
    test_service_analysis = {
        "service_name": "의료 영상 진단 AI",
        "service_provider": "HealthTech Inc.",
        "target_functionality": ["의료 영상 분석", "병변 탐지", "진단 제안"],
        "data_types": ["환자 의료 영상", "익명화된 병력 데이터"],
        "decision_processes": ["영상 전처리", "딥러닝 모델 분석", "이상 영역 식별", "진단 제안"],
        "technical_architecture": "CNN 기반 딥러닝 모델, 클라우드 호스팅",
        "user_groups": ["방사선과 의사", "일반 의사"],
        "deployment_context": "주요 대학 병원"
    }
    
    test_risk_assessment = {
        "risk_areas": {
            "bias": {
                "score": 7,
                "evidence": ["다양성이 부족한 훈련 데이터", "특정 인구집단 데이터 누락"],
                "details": "훈련 데이터가 특정 인구통계학적 그룹에 편중되어 있어 모델이 이러한 그룹에 대해 더 정확한 결과를 제공합니다."
            },
            "privacy": {
                "score": 8,
                "evidence": ["불충분한 환자 데이터 익명화", "데이터 액세스 통제 부족"],
                "details": "환자 식별 정보가 완전히 제거되지 않아 프라이버시 침해 위험이 있습니다."
            },
            "transparency": {
                "score": 6,
                "evidence": ["의사결정 과정 설명 부족", "신뢰도 점수 부재"],
                "details": "모델이 어떻게 결론에 도달했는지 명확하게 설명하지 못합니다."
            },
            "accountability": {
                "score": 5,
                "evidence": ["책임 소재 불명확", "감사 체계 미흡"],
                "details": "시스템의 오류나 문제 발생 시 책임 소재가 명확하지 않습니다."
            }
        },
        "overall_risk_score": 6.5,
        "compliance_status": {
            "eu_ai_act": {"status": "부분 준수", "reason": "데이터 프라이버시 요구사항 불충족"},
            "oecd_ai_principles": {"status": "부분 준수", "reason": "투명성 원칙 불충족"}
        }
    }
    
    # 테스트 실행
    initial_state = {
        "service_name": "의료 영상 진단 AI",
        "domain_info": "의료",
        "domain_focus": "환자 프라이버시와 안전성",
        "service_analysis": test_service_analysis,
        "risk_assessment": test_risk_assessment
    }
    
    result_state = recommender.recommend(initial_state)
    print("\n개선 권고안 결과:")
    print(json.dumps(result_state["recommendations"], ensure_ascii=False, indent=2))
