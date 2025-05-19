# 전체 시스템 상태
state = {
    # 서비스 분석 정보
    "service_analysis": {
        "service_name": "",           # 서비스 명칭
        "service_provider": "",       # 제공 업체
        "target_functionality": [],   # 주요 기능
        "data_types": [],             # 사용 데이터 유형
        "decision_processes": [],     # 의사결정 과정
        "technical_architecture": "", # 기술 구조
        "user_groups": [],            # 대상 사용자 그룹
        "deployment_context": ""      # 배포 컨텍스트
    },
    
    # 윤리 리스크 평가
    "risk_assessment": {
        "guideline_references": {},   # 사용된 가이드라인 참조
        "risk_areas": {
            "bias": {
                "score": 0,           # 0-10 점수
                "evidence": [],       # 증거 목록
                "details": ""         # 상세 설명
            },
            "privacy": {
                "score": 0,
                "evidence": [],
                "details": ""
            },
            "transparency": {
                "score": 0,
                "evidence": [],
                "details": ""
            },
            "accountability": {
                "score": 0,
                "evidence": [],
                "details": ""
            }
        },
        "compliance_status": {},      # 규정 준수 상태
        "overall_risk_score": 0       # 종합 리스크 점수
    },
    
    # 개선 권고사항
    "recommendations": {
        "high_priority": [],          # 높은 우선순위 권고사항
        "medium_priority": [],        # 중간 우선순위 권고사항
        "low_priority": [],           # 낮은 우선순위 권고사항
        "implementation_complexity": {}, # 구현 복잡성
        "expected_impact": {},        # 예상 영향
        "best_practices": {}          # 참조된 모범 사례
    },
    
    # 보고서 생성 정보
    "report_generation": {
        "report_structure": {},       # 보고서 구조
        "visualization_elements": [], # 시각화 요소
        "key_highlights": [],         # 주요 강조점
        "conclusion_statements": [],  # 결론 진술
        "executive_summary": ""       # 요약문
    }
}
