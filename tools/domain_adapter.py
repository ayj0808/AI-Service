#도메인 특화 어댑터
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
import json
import os

class DomainAdapter:
    """
    다양한 도메인(의료, 금융, 교육 등)의 특성을 반영하여 AI 윤리 진단을 특화시키는 도구
    """

    def __init__(self, model_name="gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.2)
        self.domains_info = self._load_domain_info()
        
    def _load_domain_info(self) -> Dict[str, Any]:
        """도메인별 특화 정보 로드"""
        domains = {}
        domain_dir = "data/domain_info"
        
        # 디렉토리가 존재하는지 확인
        if not os.path.exists(domain_dir):
            os.makedirs(domain_dir, exist_ok=True)
            # 기본 도메인 정보 생성
            self._create_default_domain_info(domain_dir)
        
        # 도메인 정보 파일 로드
        for filename in os.listdir(domain_dir):
            if filename.endswith('.json'):
                domain_name = filename.split('.')[0]
                with open(os.path.join(domain_dir, filename), 'r', encoding='utf-8') as f:
                    try:
                        domains[domain_name] = json.load(f)
                    except json.JSONDecodeError:
                        print(f"⚠️ {filename} 파일을 파싱할 수 없습니다.")
        
        return domains
    
    def _create_default_domain_info(self, domain_dir: str):
        """기본 도메인 정보 파일 생성"""
        # 의료 도메인
        healthcare = {
            "name": "의료",
            "key_ethical_aspects": ["환자 프라이버시", "진단 정확성", "의료 형평성", "안전성"],
            "regulations": ["HIPAA", "의료기기 규제", "EU AI Act 고위험 분류"],
            "risk_weights": {
                "bias": 0.8,
                "privacy": 1.0,
                "transparency": 0.9,
                "accountability": 0.9
            },
            "domain_specific_questions": [
                "환자 데이터는 어떻게 익명화되고 보호되나요?",
                "다양한 인구집단에 대한 진단 정확도가 검증되었나요?",
                "의사결정 과정에서 의료 전문가의 역할은 무엇인가요?"
            ]
        }
        
        # 금융 도메인
        finance = {
            "name": "금융",
            "key_ethical_aspects": ["금융 포용성", "알고리즘 공정성", "설명가능성", "금융 안정성"],
            "regulations": ["GDPR", "공정대출법", "금융규제", "EU AI Act"],
            "risk_weights": {
                "bias": 1.0,
                "privacy": 0.9,
                "transparency": 1.0,
                "accountability": 0.8
            },
            "domain_specific_questions": [
                "신용평가 결정의 설명을 제공하나요?",
                "소외계층에 대한 금융 접근성이 고려되었나요?",
                "알고리즘 편향을 정기적으로 모니터링하나요?"
            ]
        }
        
        # 교육 도메인
        education = {
            "name": "교육",
            "key_ethical_aspects": ["학습자 프라이버시", "교육 형평성", "발달 적합성", "자율성"],
            "regulations": ["FERPA", "아동 온라인 개인정보보호법", "교육데이터 규제"],
            "risk_weights": {
                "bias": 0.9,
                "privacy": 1.0,
                "transparency": 0.8,
                "accountability": 0.7
            },
            "domain_specific_questions": [
                "학생 데이터는 어떻게 보호되고 사용되나요?",
                "다양한 학습 스타일과 배경을 가진 학생들에게 공정한가요?",
                "교사와 부모가 AI 의사결정을 이해하고 검토할 수 있나요?"
            ]
        }
        
        # 파일 저장
        with open(os.path.join(domain_dir, 'healthcare.json'), 'w', encoding='utf-8') as f:
            json.dump(healthcare, f, ensure_ascii=False, indent=2)
        
        with open(os.path.join(domain_dir, 'finance.json'), 'w', encoding='utf-8') as f:
            json.dump(finance, f, ensure_ascii=False, indent=2)
        
        with open(os.path.join(domain_dir, 'education.json'), 'w', encoding='utf-8') as f:
            json.dump(education, f, ensure_ascii=False, indent=2)

    def get_domain_specific_info(self, domain_info: str) -> Dict[str, Any]:
        """
        도메인 이름을 기반으로 특화 정보 반환
        
        Args:
            domain_info: 도메인 정보 (예: '의료', '금융', '교육')
            
        Returns:
            도메인 특화 정보
        """
        # 유사 도메인 찾기
        domain_key = None
        for key in self.domains_info.keys():
            if key in domain_info.lower() or self.domains_info[key]["name"] in domain_info:
                domain_key = key
                break
        
        # 도메인 정보 반환
        if domain_key and domain_key in self.domains_info:
            return self.domains_info[domain_key]
        else:
            # 기본 도메인 정보
            return {
                "name": "일반",
                "key_ethical_aspects": ["편향성", "프라이버시", "투명성", "책임성"],
                "regulations": ["EU AI Act", "OECD AI 원칙", "UNESCO AI 윤리"],
                "risk_weights": {
                    "bias": 1.0,
                    "privacy": 1.0,
                    "transparency": 1.0,
                    "accountability": 1.0
                },
                "domain_specific_questions": []
            }

    def enhance_service_analysis(self, service_analysis: Dict[str, Any], 
                              domain_info: str, domain_focus: str) -> Dict[str, Any]:
        """
        서비스 분석 정보를 도메인 특화 관점에서 강화
        
        Args:
            service_analysis: 서비스 분석 정보
            domain_info: 도메인 정보
            domain_focus: 중점 분석 요소
            
        Returns:
            강화된 서비스 분석 정보
        """
        # 도메인 특화 정보 가져오기
        domain_specific = self.get_domain_specific_info(domain_info)
        
        # 프롬프트 준비
        system_prompt = f"""
        당신은 {domain_info} 도메인의 AI 윤리 전문가입니다. 
        제공된 AI 서비스 분석 정보를 {domain_info} 도메인의 특성과 '{domain_focus}' 측면을 
        중점적으로 고려하여 강화해주세요.
        
        특히 다음 측면을 중점적으로 분석하세요:
        - {domain_info} 도메인에서의 특수한 윤리적 고려사항
        - {domain_focus}와 관련된 서비스 특성
        - {domain_info} 분야의 규제 및 표준과의 연관성
        """
        
        prompt = f"""
        AI 서비스 분석 정보:
        {json.dumps(service_analysis, ensure_ascii=False, indent=2)}
        
        도메인: {domain_info}
        중점 분석 요소: {domain_focus}
        
        도메인 특화 정보:
        {json.dumps(domain_specific, ensure_ascii=False, indent=2)}
        
        위 정보를 바탕으로 {domain_info} 도메인과 {domain_focus} 측면을 고려한 강화된 서비스 분석 정보를 
        JSON 형식으로 제공해주세요. 기존 정보를 유지하되, 'domain_specific_info' 필드에 
        도메인 특화 분석 정보를 추가해주세요.
        """
        
        # LLM에 요청
        response = self.llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ])
        
        try:
            # JSON 형식 응답 추출 시도
            content = response.content
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                enhanced_analysis = json.loads(json_str)
                
                # 기존 정보 유지하면서 업데이트
                if isinstance(enhanced_analysis, dict):
                    # domain_specific_info 필드만 가져와서 기존 정보에 추가
                    if "domain_specific_info" in enhanced_analysis:
                        service_analysis["domain_specific_info"] = enhanced_analysis["domain_specific_info"]
                    else:
                        # 전체 응답이 domain_specific_info로 간주
                        service_analysis["domain_specific_info"] = enhanced_analysis
            
            return service_analysis
            
        except json.JSONDecodeError:
            # JSON 파싱 실패 시
            service_analysis["domain_specific_info"] = {
                "raw_enhancement": response.content
            }
            return service_analysis

    def adapt(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        도메인 특화 정보를 반영하여 시스템 상태 조정
        
        Args:
            state: 현재 시스템 상태
            
        Returns:
            도메인 특화 정보가 반영된 시스템 상태
        """
        # 상태에서 필요한 정보 추출
        service_analysis = state.get("service_analysis", {})
        domain_info = state.get("domain_info", "일반")
        domain_focus = state.get("domain_focus", "모든 측면")
        
        if not service_analysis:
            print("⚠️ 서비스 분석 정보가 없습니다.")
            return state
        
        
        #1차 수정..
        # 도메인 가이드라인 자동 검색
        # 도메인 특화 정보 가져오기 - 문제가 발생한 부분 수정
        domain_specific = self.get_domain_specific_info(domain_info)
         # 수정된 코드: 가이드라인 정보를 도메인 특화 정보에서 가져옴
        domain_guidelines = domain_specific.get("regulations", [])
        state["domain_guidelines"] = domain_guidelines
        
        
        print(f"\n🔍 '{domain_info}' 도메인과 '{domain_focus}' 중점 요소를 반영하여 분석 정보 강화 중...")
        
        # 도메인 특화 정보 가져오기
        domain_specific = self.get_domain_specific_info(domain_info)
        
        # 도메인 관련 정보 출력
        print(f"📊 도메인 특화 고려사항:")
        for aspect in domain_specific.get("key_ethical_aspects", [])[:3]:
            print(f"  • {aspect}")
            
        print(f"📜 관련 규제/표준:")
        for reg in domain_specific.get("regulations", [])[:2]:
            print(f"  • {reg}")
        
        # 서비스 분석 정보 강화
        enhanced_service_analysis = self.enhance_service_analysis(
            service_analysis, domain_info, domain_focus
        )
        
        # 상태 업데이트
        state["service_analysis"] = enhanced_service_analysis
        state["domain_specific"] = domain_specific
        
        print("✅ 도메인 특화 정보 적용 완료")
        
        return state


# 단독 테스트용 코드
if __name__ == "__main__":
    adapter = DomainAdapter()
    
    # 테스트용 서비스 분석 정보
    test_service_analysis = {
        "service_name": "의료 영상 진단 AI",
        "service_provider": "HealthTech Inc.",
        "target_functionality": ["의료 영상 분석", "병변 탐지", "진단 제안"],
        "data_types": ["환자 의료 영상", "익명화된 병력 데이터"],
        "decision_processes": ["영상 전처리", "딥러닝 모델 분석", "이상 영역 식별", "진단 제안"]
    }
    
    # 테스트 실행
    initial_state = {
        "service_name": "의료 영상 진단 AI",
        "domain_info": "의료",
        "domain_focus": "환자 프라이버시와 안전성",
        "service_analysis": test_service_analysis
    }
    
    result_state = adapter.adapt(initial_state)
    print("\n도메인 특화 정보가 적용된 서비스 분석 결과:")
    print(json.dumps(result_state["service_analysis"].get("domain_specific_info", {}), 
                    ensure_ascii=False, indent=2))
