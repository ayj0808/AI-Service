#윤리 리스크 진단 에이전트
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
import json

# 프롬프트 임포트
from prompts.risk_assessment import (
    INITIAL_ASSESSMENT_PROMPT,
    DEEP_DIVE_PROMPT,
    FINAL_ASSESSMENT_PROMPT, 
    COMPLIANCE_CHECK_PROMPT
)

class RiskAssessor:
    """
    AI 서비스의 윤리적 리스크를 평가하는 에이전트
    """

    def __init__(self, model_name="gpt-4o-mini"):
        # LLM 모델 초기화 - 온도를 낮게 설정하여 객관적인 평가 유도
        self.llm = ChatOpenAI(model=model_name, temperature=0.1)
        # 평가할 윤리적 측면들
        self.ethical_aspects = ["bias", "privacy", "transparency", "accountability"]
        
    def initial_risk_assessment(self, service_analysis: Dict[str, Any], domain_info: str, domain_focus: str) -> Dict[str, Any]:
        """
        서비스 정보를 바탕으로 초기 윤리 리스크 평가 수행
        
        Args:
            service_analysis: 서비스 분석 정보
            domain_info: 서비스 도메인 정보
            domain_focus: 중점 분석 요소
            
        Returns:
            초기 리스크 평가 결과
        """
        # 서비스 분석 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        
        # 초기 리스크 평가 요청
        response = self.llm.invoke(
            INITIAL_ASSESSMENT_PROMPT.format(
                service_analysis=service_analysis_str,
                domain_info=domain_info,
                domain_focus=domain_focus
            )
        )
        
        try:
            # JSON 형식 응답 추출
            content = response.content
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                # 구조화되지 않은 경우 수동 파싱 시도
                result = self._parse_unstructured_assessment(content)
                
            return result
            
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 수동 파싱 시도
            return self._parse_unstructured_assessment(response.content)

    def deep_dive_analysis(self, service_name: str, ethical_aspect: str, 
                         service_analysis: Dict[str, Any], domain_info: str,
                         current_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        특정 윤리적 측면에 대해 심층 분석 수행
        
        Args:
            current_assessment: 현재까지의 평가 정보
            
        Returns:
            심층 분석 결과
        """
        # 서비스 분석과 현재 평가 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        current_assessment_str = json.dumps(current_assessment, ensure_ascii=False, indent=2)
        
        # 윤리적 측면 한글화 (프롬프트 템플릿용)
        aspect_korean = {
            "bias": "편향성",
            "privacy": "프라이버시",
            "transparency": "투명성",
            "accountability": "책임성"
        }.get(ethical_aspect, ethical_aspect)
        
        # 심층 분석 요청
        response = self.llm.invoke(
            DEEP_DIVE_PROMPT.format(
                ethical_aspect=aspect_korean,
                service_name=service_name,
                service_analysis=service_analysis_str,
                domain_info=domain_info,
                current_assessment=current_assessment_str
            )
        )
        
        # 응답 처리
        return {
            "aspect": ethical_aspect,
            "detailed_analysis": response.content
        }

    def check_compliance(self, service_name: str, service_analysis: Dict[str, Any], 
                       risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        주요 AI 윤리 가이드라인 준수 여부 확인
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        risk_assessment_str = json.dumps(risk_assessment, ensure_ascii=False, indent=2)
        
        # 준수 여부 평가 요청
        response = self.llm.invoke(
            COMPLIANCE_CHECK_PROMPT.format(
                service_name=service_name,
                service_analysis=service_analysis_str,
                risk_assessment=risk_assessment_str
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
                # 구조화되지 않은 경우 기본 형식으로 반환
                result = {
                    "eu_ai_act": {
                        "status": "미평가",
                        "reason": "자동 파싱 실패"
                    },
                    "oecd_ai_principles": {
                        "status": "미평가",
                        "reason": "자동 파싱 실패"
                    },
                    "unesco_recommendation": {
                        "status": "미평가",
                        "reason": "자동 파싱 실패"
                    },
                    "compliance_text": response.content
                }
                
            return result
            
        except json.JSONDecodeError:
            # 파싱 실패 시 기본 형식으로 반환
            return {
                "eu_ai_act": {
                    "status": "미평가",
                    "reason": "JSON 파싱 실패"
                },
                "oecd_ai_principles": {
                    "status": "미평가",
                    "reason": "JSON 파싱 실패"
                },
                "unesco_recommendation": {
                    "status": "미평가",
                    "reason": "JSON 파싱 실패"
                },
                "compliance_text": response.content
            }

    def generate_final_assessment(self, service_name: str, service_analysis: Dict[str, Any],
                               initial_assessment: Dict[str, Any], deep_dive_results: List[Dict[str, Any]],
                               domain_info: str, domain_focus: str) -> Dict[str, Any]:
        """
        모든 분석을 종합한 최종 리스크 평가 보고서 생성
        
        Args:
            service_name: 서비스 이름
            service_analysis: 서비스 분석 정보
            initial_assessment: 초기 리스크 평가
            deep_dive_results: 심층 분석 결과 목록
            domain_info: 도메인 정보
            domain_focus: 중점 분석 요소
            
        Returns:
            최종 리스크 평가 보고서
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        initial_assessment_str = json.dumps(initial_assessment, ensure_ascii=False, indent=2)
        deep_dive_str = json.dumps(deep_dive_results, ensure_ascii=False, indent=2)
        
        # 최종 평가 요청
        response = self.llm.invoke(
            FINAL_ASSESSMENT_PROMPT.format(
                service_name=service_name,
                service_analysis=service_analysis_str,
                initial_assessment=initial_assessment_str,
                deep_dive_results=deep_dive_str,
                domain_info=domain_info,
                domain_focus=domain_focus
            )
        )
        
        try:
            # JSON 형식 응답 추출
            content = response.content
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                # 구조화되지 않은 경우 기본 구조로 반환
                result = {
                    "risk_areas": {},
                    "overall_risk_score": 0,
                    "assessment_text": response.content
                }
                
            return result
            
        except json.JSONDecodeError:
            # 파싱 실패 시 기본 구조로 반환
            return {
                "risk_areas": {},
                "overall_risk_score": 0,
                "assessment_text": response.content
            }

    def _parse_unstructured_assessment(self, text: str) -> Dict[str, Any]:
        """
        구조화되지 않은 평가 텍스트를 파싱하여 구조화
        
        Args:
            text: 구조화되지 않은 평가 텍스트
            
        Returns:
            구조화된 평가 결과
        """
        # 기본 구조 설정
        result = {
            "risk_areas": {
                "bias": {"score": 0, "evidence": [], "details": ""},
                "privacy": {"score": 0, "evidence": [], "details": ""},
                "transparency": {"score": 0, "evidence": [], "details": ""},
                "accountability": {"score": 0, "evidence": [], "details": ""}
            },
            "overall_risk_score": 0,
            "assessment_text": text
        }
        
        try:
            # 점수 추출 시도
            for aspect in ["bias", "privacy", "transparency", "accountability"]:
                # 영어 또는 한글 키워드로 검색
                english_keyword = f"{aspect.capitalize()}: "
                korean_keywords = {
                    "bias": "편향성: ", 
                    "privacy": "프라이버시: ", 
                    "transparency": "투명성: ", 
                    "accountability": "책임성: "
                }
                
                # 영어 키워드로 검색
                if english_keyword in text:
                    score_text = text.split(english_keyword)[1].split("/")[0].strip()
                    try:
                        result["risk_areas"][aspect]["score"] = int(score_text)
                    except ValueError:
                        pass
                
                # 한글 키워드로 검색
                elif aspect in korean_keywords and korean_keywords[aspect] in text:
                    score_text = text.split(korean_keywords[aspect])[1].split("/")[0].strip()
                    try:
                        result["risk_areas"][aspect]["score"] = int(score_text)
                    except ValueError:
                        pass
            
            # 전체 점수 계산
            scores = [result["risk_areas"][aspect]["score"] for aspect in result["risk_areas"]]
            if scores:
                result["overall_risk_score"] = sum(scores) / len(scores)
                
        except Exception as e:
            # 파싱 실패 시 원본 텍스트만 보존
            print(f"평가 텍스트 파싱 오류: {e}")
            
        return result

    def assess(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        전체 리스크 평가 프로세스 실행
        
        Args:
            state: 현재 시스템 상태
            
        Returns:
            업데이트된 시스템 상태
        """
        # 상태에서 필요한 정보 추출
        service_analysis = state.get("service_analysis", {})
        service_name = service_analysis.get("service_name", state.get("service_name", ""))
        domain_info = state.get("domain_info", "일반")
        domain_focus = state.get("domain_focus", "모든 측면")
        
        # 서비스 정보가 충분한지 확인
        if not service_analysis or not service_name:
            print("⚠️ 서비스 분석 정보가 부족합니다. 서비스 분석 단계로 돌아갑니다.")
            # 피드백 루프를 위한 플래그 설정
            state["feedback_required"] = True
            return state
        
        print(f"\n🔍 '{service_name}' 서비스의 윤리적 리스크 평가를 시작합니다...")
        print(f"📊 도메인: {domain_info} | 중점 분석 요소: {domain_focus}")
        
        # 1. 초기 리스크 평가 수행
        print("\n🧐 초기 윤리 리스크 평가 중...")
        initial_assessment = self.initial_risk_assessment(service_analysis, domain_info, domain_focus)
        
        # 초기 평가 결과 출력
        print("\n📊 초기 윤리 리스크 평가 결과:")
        for aspect in initial_assessment.get("risk_areas", {}):
            score = initial_assessment["risk_areas"][aspect].get("score", "N/A")
            print(f"- {aspect.capitalize()}: {score}/10")
        
        # 2. 필요시 심층 분석 수행
        deep_dive_results = []
        high_risk_aspects = []
        
        # 높은 리스크 영역 식별 (점수 7 이상)
        for aspect in self.ethical_aspects:
            if aspect in initial_assessment.get("risk_areas", {}) and \
               initial_assessment["risk_areas"][aspect].get("score", 0) >= 7:
                high_risk_aspects.append(aspect)
        
        # 높은 리스크 영역에 대한 심층 분석
        if high_risk_aspects:
            print("\n🔍 높은 리스크가 식별된 영역에 대한 심층 분석 중...")
            
            for aspect in high_risk_aspects:
                print(f"- {aspect.capitalize()} 심층 분석...")
                deep_dive_result = self.deep_dive_analysis(
                    service_name, aspect, service_analysis, domain_info, initial_assessment
                )
                deep_dive_results.append(deep_dive_result)
        
        # 3. 가이드라인 준수 여부 확인
        print("\n📋 주요 AI 윤리 가이드라인 준수 여부 평가 중...")
        compliance_status = self.check_compliance(service_name, service_analysis, initial_assessment)
        
        # 4. 최종 평가 보고서 생성
        print("\n📝 최종 윤리 리스크 평가 보고서 생성 중...")
        final_assessment = self.generate_final_assessment(
            service_name, service_analysis, initial_assessment,
            deep_dive_results, domain_info, domain_focus
        )
        
        # 종합 리스크 점수 계산 (이미 계산되어 있지 않은 경우)
        if "overall_risk_score" not in final_assessment or not final_assessment["overall_risk_score"]:
            scores = [final_assessment.get("risk_areas", {}).get(aspect, {}).get("score", 0) 
                     for aspect in self.ethical_aspects 
                     if aspect in final_assessment.get("risk_areas", {})]
            
            if scores:
                final_assessment["overall_risk_score"] = round(sum(scores) / len(scores), 1)
        
        # 최종 평가 결과 저장
        risk_assessment = {
            "guideline_references": compliance_status,
            "risk_areas": final_assessment.get("risk_areas", {}),
            "compliance_status": compliance_status,
            "overall_risk_score": final_assessment.get("overall_risk_score", 0),
            "deep_dive_analyses": deep_dive_results
        }
        
        # 평가 결과 로그
        print(f"\n✅ 윤리 리스크 평가가 완료되었습니다.")
        print(f"📊 종합 리스크 점수: {risk_assessment['overall_risk_score']}/10")
        
        # 상태 업데이트
        state["risk_assessment"] = risk_assessment
        
        return state


# 단독 테스트용 코드
if __name__ == "__main__":
    assessor = RiskAssessor()
    
    # 테스트용 서비스 분석 정보
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
    
    # 테스트 실행
    initial_state = {
        "service_name": "의료 영상 진단 AI",
        "domain_info": "의료",
        "domain_focus": "환자 프라이버시와 안전성",
        "service_analysis": test_service_analysis
    }
    
    result_state = assessor.assess(initial_state)
    print("\n윤리 리스크 평가 결과:")
    print(json.dumps(result_state["risk_assessment"], ensure_ascii=False, indent=2))
