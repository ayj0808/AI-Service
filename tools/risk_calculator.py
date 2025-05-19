#리스크 평가 계산기
from typing import Dict, List, Any, Tuple

class RiskCalculator:
    """
    AI 윤리성 리스크를 정량적으로 평가하는 도구
    """

    def __init__(self):
        # 기본 리스크 가중치
        self.default_weights = {
            "bias": 1.0,
            "privacy": 1.0,
            "transparency": 1.0,
            "accountability": 1.0
        }
        
        # 리스크 영역별 평가 기준
        self.assessment_criteria = {
            "bias": [
                "다양성이 충분한 훈련 데이터를 사용하는가",
                "알고리즘 공정성 테스트를 수행하는가",
                "특정 그룹에 대한 불균형적 영향이 있는가",
                "편향 완화 조치가 있는가"
            ],
            "privacy": [
                "개인정보 수집이 최소한으로 제한되는가",
                "명시적 동의 절차가 있는가",
                "데이터 암호화와 보안 조치가 있는가",
                "개인정보 접근 통제와 감사 메커니즘이 있는가"
            ],
            "transparency": [
                "의사결정 과정이 설명 가능한가",
                "사용자에게 AI 사용 여부를 공개하는가",
                "신뢰도 점수를 제공하는가",
                "알고리즘 공개 또는 문서화가 되어 있는가"
            ],
            "accountability": [
                "책임 소재가 명확한가",
                "오류와 문제에 대응하는 체계가 있는가",
                "인간 감독 메커니즘이 있는가",
                "정기적인 감사와 모니터링이 이루어지는가"
            ]
        }

    def calculate_risk_score(self, risk_factors: Dict[str, float], 
                          mitigation_factors: Dict[str, float],
                          domain_weights: Dict[str, float] = None) -> float:
        """
        리스크 점수 계산
        
        Args:
            risk_factors: 리스크 요소별 점수 (0-1 범위)
            mitigation_factors: 리스크 완화 요소별 점수 (0-1 범위)
            domain_weights: 도메인별 리스크 영역 가중치
            
        Returns:
            종합 리스크 점수 (0-10 범위)
        """
        # 도메인 가중치 설정
        weights = domain_weights if domain_weights else self.default_weights
        
        # 영역별 리스크 계산
        area_scores = {}
        
        for area in self.default_weights.keys():
            # 해당 영역의 리스크 요소와 완화 요소 가져오기
            area_risk = risk_factors.get(area, 0.5)  # 기본값 0.5
            area_mitigation = mitigation_factors.get(area, 0.0)  # 기본값 0.0
            
            # 완화 요소를 고려한 최종 리스크 계산 (리스크 - 리스크 * 완화)
            net_risk = area_risk * (1 - area_mitigation)
            
            # 0-10 점수 범위로 변환
            area_scores[area] = round(net_risk * 10, 1)
        
        # 가중 평균 계산
        total_weight = sum(weights.values())
        weighted_score = 0
        
        for area, score in area_scores.items():
            area_weight = weights.get(area, 1.0)
            weighted_score += score * (area_weight / total_weight)
        
        return round(weighted_score, 1)

    def assess_risk(self, risk_type: str, impact_factors: Dict[str, float], 
                  mitigation_presence: Dict[str, bool], domain_info: str = None) -> Dict[str, Any]:
        """
        특정 유형의 리스크 평가
        
        Args:
            risk_type: 리스크 유형 (bias, privacy, transparency, accountability)
            impact_factors: 영향 요소와 해당 값
            mitigation_presence: 완화 조치 존재 여부
            domain_info: 도메인 정보
            
        Returns:
            리스크 평가 결과
        """
        # 도메인별 가중치 조정
        domain_modifier = 1.0
        if domain_info:
            domain_modifiers = {
                "의료": {"bias": 0.9, "privacy": 1.3, "transparency": 1.1, "accountability": 1.2},
                "금융": {"bias": 1.2, "privacy": 1.0, "transparency": 1.3, "accountability": 1.1},
                "교육": {"bias": 1.1, "privacy": 1.2, "transparency": 0.9, "accountability": 0.8}
            }
            
            # 도메인별 리스크 유형 가중치 적용
            for domain, modifiers in domain_modifiers.items():
                if domain in domain_info.lower():
                    domain_modifier = modifiers.get(risk_type, 1.0)
                    break
        
        # 기본 리스크 점수 계산 (0-1 범위)
        base_score = sum(impact_factors.values()) / max(len(impact_factors), 1)
        
        # 완화 요소 고려
        mitigation_factor = 0
        if mitigation_presence:
            mitigation_count = sum(1 for present in mitigation_presence.values() if present)
            mitigation_factor = mitigation_count / max(len(mitigation_presence), 1) * 0.7  # 최대 70% 완화
            
        # 도메인 가중치를 적용한 최종 점수 계산
        final_score = base_score * (1 - mitigation_factor) * domain_modifier
        
        # 0-10 범위로 변환
        final_score_10 = min(max(round(final_score * 10, 1), 0), 10)
        
        # 리스크 분류
        risk_category = "높음" if final_score_10 >= 7 else "중간" if final_score_10 >= 4 else "낮음"
        risk_severity = "심각" if final_score_10 >= 8 else "중대" if final_score_10 >= 6 else "보통" if final_score_10 >= 3 else "경미"
        
        return {
            "score": final_score_10,
            "category": risk_category,
            "severity": risk_severity,
            "domain_modifier": domain_modifier,
            "impact_score": base_score * 10,
            "mitigation_effect": mitigation_factor
        }

    def get_assessment_criteria(self, risk_type: str = None, domain_info: str = None) -> Dict[str, List[str]]:
        """
        리스크 평가 기준 제공
        
        Args:
            risk_type: 특정 리스크 유형 (지정하지 않으면 모든 유형)
            domain_info: 도메인 정보 (도메인별 추가 기준 제공)
            
        Returns:
            평가 기준 목록
        """
        criteria = {}
        
        # 특정 리스크 유형만 요청한 경우
        if risk_type and risk_type in self.assessment_criteria:
            criteria[risk_type] = self.assessment_criteria[risk_type].copy()
        else:
            # 모든 리스크 유형의 기준 제공
            criteria = {k: v.copy() for k, v in self.assessment_criteria.items()}
        
        # 도메인별 추가 기준
        if domain_info:
            domain_specific_criteria = {
                "의료": {
                    "bias": ["다양한 인구통계학적 그룹의 진단 정확도 차이 측정", "의료 형평성 고려"],
                    "privacy": ["환자 식별 정보 보호 수준", "민감한 건강 데이터 처리 방식"],
                    "transparency": ["의료진에게 의사결정 근거 제공", "환자에게 진단 신뢰도 설명"],
                    "accountability": ["의료 오류 발생 시 책임 체계", "인간 의사의 최종 검토 과정"]
                },
                "금융": {
                    "bias": ["취약계층에 대한 금융 접근성 영향", "불균형적 대출 거부율"],
                    "privacy": ["금융 거래 데이터 보호 수준", "신용 정보 사용에 대한 동의 절차"],
                    "transparency": ["신용 평가 요소 설명 가능성", "금융 결정의 근거 제공"],
                    "accountability": ["금융 조언의 책임 소재", "알고리즘 결정에 대한 이의제기 가능성"]
                },
                "교육": {
                    "bias": ["다양한 학습 스타일 고려", "문화적 배경에 따른 평가 차이"],
                    "privacy": ["학생 데이터 보호 수준", "미성년자 정보 처리 동의 절차"],
                    "transparency": ["학습 평가 기준의 명확성", "학부모와 교사의 이해도"],
                    "accountability": ["교육적 결정에 대한 책임", "알고리즘과 교사 역할 구분"]
                }
            }
            
            # 도메인별 추가 기준 적용
            for domain, domain_criteria in domain_specific_criteria.items():
                if domain in domain_info.lower():
                    if risk_type:
                        if risk_type in domain_criteria:
                            criteria[risk_type].extend(domain_criteria[risk_type])
                    else:
                        for area, area_criteria in domain_criteria.items():
                            if area in criteria:
                                criteria[area].extend(area_criteria)
        
        return criteria

    def calculate_risk_distribution(self, service_analysis: Dict[str, Any], 
                                 domain_info: str = None) -> Dict[str, float]:
        """
        서비스 분석 정보를 바탕으로 리스크 분포 계산
        
        Args:
            service_analysis: 서비스 분석 정보
            domain_info: 도메인 정보
            
        Returns:
            리스크 영역별 예상 분포
        """
        # 기본 리스크 분포
        risk_distribution = {
            "bias": 0.25,
            "privacy": 0.25, 
            "transparency": 0.25,
            "accountability": 0.25
        }
        
        # 데이터 유형에 따른 리스크 조정
        data_types = service_analysis.get("data_types", [])
        for data_type in data_types:
            data_type_lower = data_type.lower()
            
            if "개인" in data_type_lower or "민감" in data_type_lower or "personal" in data_type_lower:
                risk_distribution["privacy"] += 0.1
            
            if "인구" in data_type_lower or "demographic" in data_type_lower:
                risk_distribution["bias"] += 0.05
        
        # 의사결정 과정에 따른 리스크 조정
        decision_processes = service_analysis.get("decision_processes", [])
        for process in decision_processes:
            process_lower = process.lower()
            
            if "자동" in process_lower or "automatic" in process_lower:
                risk_distribution["accountability"] += 0.05
                risk_distribution["transparency"] += 0.05
            
            if "딥러닝" in process_lower or "deep learning" in process_lower:
                risk_distribution["transparency"] += 0.1
        
        # 도메인별 리스크 조정
        if domain_info:
            domain_risk_adjustments = {
                "의료": {"privacy": 0.15, "accountability": 0.1, "bias": -0.05, "transparency": -0.05},
                "금융": {"bias": 0.15, "transparency": 0.1, "privacy": 0.05, "accountability": -0.05},
                "교육": {"privacy": 0.15, "bias": 0.1, "accountability": -0.05, "transparency": -0.05}
            }
            
            for domain, adjustments in domain_risk_adjustments.items():
                if domain in domain_info.lower():
                    for area, adjustment in adjustments.items():
                        risk_distribution[area] += adjustment
        
        # 총합이 1이 되도록 정규화
        total = sum(risk_distribution.values())
        normalized_distribution = {k: round(v / total, 3) for k, v in risk_distribution.items()}
        
        return normalized_distribution


# 단독 테스트용 코드
if __name__ == "__main__":
    calculator = RiskCalculator()
    
    # 테스트 1: 리스크 점수 계산
    risk_factors = {
        "bias": 0.7,  # 높은 편향성 리스크
        "privacy": 0.8,  # 높은 프라이버시 리스크
        "transparency": 0.5,  # 중간 투명성 리스크
        "accountability": 0.4   # 낮은 책임성 리스크
    }
    
    mitigation_factors = {
        "bias": 0.3,  # 30% 완화
        "privacy": 0.2,  # 20% 완화
        "transparency": 0.4,  # 40% 완화
        "accountability": 0.5   # 50% 완화
    }
    
    # 의료 도메인 가중치
    medical_weights = {
        "bias": 0.8,
        "privacy": 1.3,
        "transparency": 0.9,
        "accountability": 1.0
    }
    
    score = calculator.calculate_risk_score(risk_factors, mitigation_factors, medical_weights)
    print(f"종합 리스크 점수: {score}/10")
    
    # 테스트 2: 특정 리스크 평가
    impact_factors = {"데이터_편향": 0.8, "알고리즘_편향": 0.6, "사용자_편향": 0.4}
    mitigation_presence = {"다양성_확보": True, "편향성_테스트": False, "인적_검토": True}
    
    result = calculator.assess_risk("bias", impact_factors, mitigation_presence, "의료")
    print(f"\n편향성 리스크 평가 결과:")
    print(f"점수: {result['score']}/10")
    print(f"분류: {result['category']}")
    print(f"심각도: {result['severity']}")
    
    # 테스트 3: 평가 기준 확인
    criteria = calculator.get_assessment_criteria("privacy", "의료")
    print(f"\n의료 도메인의 프라이버시 평가 기준:")
    for i, criterion in enumerate(criteria.get("privacy", []), 1):
        print(f"{i}. {criterion}")
