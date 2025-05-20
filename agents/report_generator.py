#리포트 작성 에이전트
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
import json
import os
import datetime

# 프롬프트 임포트
from prompts.report_generation import (
    REPORT_STRUCTURE_PROMPT,
    EXECUTIVE_SUMMARY_PROMPT,
    INTRODUCTION_SECTION_PROMPT,
    SERVICE_OVERVIEW_SECTION_PROMPT,
    RISK_ASSESSMENT_SECTION_PROMPT,
    COMPLIANCE_SECTION_PROMPT,
    RECOMMENDATIONS_SECTION_PROMPT,
    CONCLUSION_SECTION_PROMPT,
    VISUALIZATION_SUGGESTIONS_PROMPT,
    FINAL_REPORT_ASSEMBLY_PROMPT
)

class ReportGenerator:
    """
    AI 서비스의 윤리적 리스크 진단 결과를 종합적인 보고서로 작성하는 에이전트
    """

    def __init__(self, model_name="gpt-4o-mini"):
        # LLM 모델 초기화 - 보고서 작성은 창의성이 약간 필요하므로 온도 조정
        self.llm = ChatOpenAI(model=model_name, temperature=0.3)

    def create_report_structure(self, service_analysis: Dict[str, Any],
                              risk_assessment: Dict[str, Any],
                              recommendations: Dict[str, Any],
                              domain_info: str, domain_focus: str) -> Dict[str, Any]:
        """
        보고서의 전체 구조 설계
        
        Args:
            service_analysis: 서비스 분석 정보
            risk_assessment: 윤리 리스크 평가 결과
            recommendations: 개선 권고안
            domain_info: 도메인 정보
            domain_focus: 중점 분석 요소
            
        Returns:
            보고서 구조
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        risk_assessment_str = json.dumps(risk_assessment, ensure_ascii=False, indent=2)
        recommendations_str = json.dumps(recommendations, ensure_ascii=False, indent=2)
        
        # 보고서 구조 요청
        response = self.llm.invoke(
            REPORT_STRUCTURE_PROMPT.format(
                service_analysis=service_analysis_str,
                risk_assessment=risk_assessment_str,
                recommendations=recommendations_str,
                domain_info=domain_info,
                domain_focus=domain_focus
            )
        )
        
        # 구조 반환 (텍스트 형태로)
        return {
            "structure": response.content
        }

    def generate_executive_summary(self, service_name: str, service_analysis: Dict[str, Any],
                                risk_assessment: Dict[str, Any], recommendations: Dict[str, Any],
                                domain_info: str, domain_focus: str) -> str:
        """
        보고서 요약(Executive Summary) 작성
        
        Args:
            service_name: 서비스 이름
            service_analysis: 서비스 분석 정보
            risk_assessment: 윤리 리스크 평가 결과
            recommendations: 개선 권고안
            domain_info: 도메인 정보
            domain_focus: 중점 분석 요소
            
        Returns:
            보고서 요약문
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        risk_assessment_str = json.dumps(risk_assessment, ensure_ascii=False, indent=2)
        recommendations_str = json.dumps(recommendations, ensure_ascii=False, indent=2)
        
        # 요약 생성 요청
        response = self.llm.invoke(
            EXECUTIVE_SUMMARY_PROMPT.format(
                service_name=service_name,
                service_analysis=service_analysis_str,
                risk_assessment=risk_assessment_str,
                recommendations=recommendations_str,
                domain_info=domain_info,
                domain_focus=domain_focus
            )
        )
        
        return response.content

    def generate_introduction(self, service_name: str, service_analysis: Dict[str, Any],
                           domain_info: str, domain_focus: str) -> str:
        """
        보고서 서론 섹션 작성
        Returns:
            서론 섹션 내용
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        
        # 서론 생성 요청
        response = self.llm.invoke(
            INTRODUCTION_SECTION_PROMPT.format(
                service_name=service_name,
                service_analysis=service_analysis_str,
                domain_info=domain_info,
                domain_focus=domain_focus
            )
        )
        
        return response.content

    def generate_service_overview(self, service_name: str, service_analysis: Dict[str, Any],
                              domain_info: str, domain_focus: str) -> str:
        """
        서비스 개요 섹션 작성
        Returns:
            서비스 개요 섹션 내용
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        
        # 서비스 개요 생성 요청
        response = self.llm.invoke(
            SERVICE_OVERVIEW_SECTION_PROMPT.format(
                service_name=service_name,
                service_analysis=service_analysis_str,
                domain_info=domain_info,
                domain_focus=domain_focus
            )
        )
        
        return response.content

    def generate_risk_assessment_section(self, service_name: str, service_analysis: Dict[str, Any],
                                     risk_assessment: Dict[str, Any], domain_info: str,
                                     domain_focus: str) -> str:
        """
        리스크 평가 섹션 작성
        Returns:
            리스크 평가 섹션 내용
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        risk_assessment_str = json.dumps(risk_assessment, ensure_ascii=False, indent=2)
        
        # 리스크 점수 추출 (기본값 0 사용)
        risk_areas = risk_assessment.get("risk_areas", {})
        bias_score = risk_areas.get("bias", {}).get("score", 0)
        privacy_score = risk_areas.get("privacy", {}).get("score", 0)
        transparency_score = risk_areas.get("transparency", {}).get("score", 0)
        accountability_score = risk_areas.get("accountability", {}).get("score", 0)
        
        # 리스크 평가 섹션 생성 요청
        response = self.llm.invoke(
            RISK_ASSESSMENT_SECTION_PROMPT.format(
                service_name=service_name,
                service_analysis=service_analysis_str,
                risk_assessment=risk_assessment_str,
                domain_info=domain_info,
                domain_focus=domain_focus,
                bias_score=bias_score,
                privacy_score=privacy_score,
                transparency_score=transparency_score,
                accountability_score=accountability_score
            )
        )
        
        return response.content

    def generate_compliance_section(self, service_name: str, risk_assessment: Dict[str, Any],
                                domain_info: str) -> str:
        """
        규정 준수 상태 섹션 작성
        Returns:
            규정 준수 상태 섹션 내용
        """
        # 입력 정보 문자열화
        risk_assessment_str = json.dumps(risk_assessment, ensure_ascii=False, indent=2)
        compliance_status_str = json.dumps(risk_assessment.get("compliance_status", {}), 
                                          ensure_ascii=False, indent=2)
        
        # 규정 준수 섹션 생성 요청
        response = self.llm.invoke(
            COMPLIANCE_SECTION_PROMPT.format(
                service_name=service_name,
                risk_assessment=risk_assessment_str,
                compliance_status=compliance_status_str,
                domain_info=domain_info
            )
        )
        
        return response.content

    def generate_recommendations_section(self, service_name: str, service_analysis: Dict[str, Any],
                                     risk_assessment: Dict[str, Any], recommendations: Dict[str, Any],
                                     domain_info: str, domain_focus: str) -> str:
        """
        개선 권고안 섹션 작성   
        Returns:
            권고안 섹션 내용
        """
        # 입력 정보 문자열화
        service_analysis_str = json.dumps(service_analysis, ensure_ascii=False, indent=2)
        risk_assessment_str = json.dumps(risk_assessment, ensure_ascii=False, indent=2)
        recommendations_str = json.dumps(recommendations, ensure_ascii=False, indent=2)
        
        # 권고안 섹션 생성 요청
        response = self.llm.invoke(
            RECOMMENDATIONS_SECTION_PROMPT.format(
                service_name=service_name,
                service_analysis=service_analysis_str,
                risk_assessment=risk_assessment_str,
                recommendations=recommendations_str,
                domain_info=domain_info,
                domain_focus=domain_focus
            )
        )
        
        return response.content

    def generate_conclusion(self, service_name: str, risk_assessment: Dict[str, Any],
                         recommendations: Dict[str, Any], domain_info: str,
                         domain_focus: str) -> str:
        """
        결론 섹션 작성
        Returns:
            결론 섹션 내용
        """
        # 입력 정보 문자열화
        risk_assessment_str = json.dumps(risk_assessment, ensure_ascii=False, indent=2)
        recommendations_str = json.dumps(recommendations, ensure_ascii=False, indent=2)
        
        # 결론 생성 요청
        response = self.llm.invoke(
            CONCLUSION_SECTION_PROMPT.format(
                service_name=service_name,
                risk_assessment=risk_assessment_str,
                recommendations=recommendations_str,
                domain_info=domain_info,
                domain_focus=domain_focus
            )
        )
        
        return response.content

    def suggest_visualizations(self, service_name: str, risk_assessment: Dict[str, Any],
                            recommendations: Dict[str, Any], domain_info: str) -> str:
        """
        보고서에 포함할 시각화 요소 제안
        Returns:
            시각화 제안 내용
        """
        # 입력 정보 문자열화
        risk_assessment_str = json.dumps(risk_assessment, ensure_ascii=False, indent=2)
        recommendations_str = json.dumps(recommendations, ensure_ascii=False, indent=2)
        
        # 시각화 제안 요청
        response = self.llm.invoke(
            VISUALIZATION_SUGGESTIONS_PROMPT.format(
                service_name=service_name,
                risk_assessment=risk_assessment_str,
                recommendations=recommendations_str,
                domain_info=domain_info
            )
        )
        
        return response.content

    def assemble_final_report(self, service_name: str, executive_summary: str, introduction: str,
                           service_overview: str, risk_assessment_section: str,
                           compliance_section: str, recommendations_section: str,
                           conclusion: str, visualization_suggestions: str) -> str:
        """
        모든 섹션을 종합하여 최종 보고서 생성
        Returns:
            최종 보고서 내용
        """
        # 최종 보고서 조립 요청
        response = self.llm.invoke(
            FINAL_REPORT_ASSEMBLY_PROMPT.format(
                service_name=service_name,
                executive_summary=executive_summary,
                introduction=introduction,
                service_overview=service_overview,
                risk_assessment_section=risk_assessment_section,
                compliance_section=compliance_section,
                recommendations_section=recommendations_section,
                conclusion=conclusion,
                visualization_suggestions=visualization_suggestions
            )
        )
        
        return response.content

    def save_report_to_file(self, report_content: str, service_name: str) -> str:
        """
        생성된 보고서를 파일로 저장  및 PDF저장
        Returns:
            저장된 파일 경로
        """
        # 출력 디렉토리 확인 및 생성
        output_dir = "outputs/reports"
        os.makedirs(output_dir, exist_ok=True)
        
        # 타임스탬프 생성 (현재 날짜/시간 포함)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        service_name_safe = service_name.replace(' ', '_')
        
         # 마크다운 파일 저장
        md_filename = f"{service_name_safe}_{timestamp}.md"
        md_filepath = os.path.join(output_dir, md_filename)
        
        with open(md_filepath, "w", encoding="utf-8") as f:
            f.write(report_content)
        
        # PDF 파일 생성
        pdf_filename = f"{service_name_safe}_{timestamp}.pdf"
        pdf_filepath = os.path.join(output_dir, pdf_filename)
    
        try:
            # weasyprint 사용 (더 안정적)
            import markdown
            from weasyprint import HTML
            
            # 마크다운을 HTML로 변환
            html_content = markdown.markdown(
                report_content,
                extensions=['tables', 'fenced_code']
            )
            
            # 스타일을 추가한 HTML 생성
            styled_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{service_name} 윤리성 리스크 진단 보고서</title>
                <style>
                    @page {{ size: A4; margin: 2cm; }}
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                    h1 {{ color: #2c3e50; border-bottom: 1px solid #3498db; padding-bottom: 10px; }}
                    h2 {{ color: #2980b9; margin-top: 20px; }}
                    h3 {{ color: #3498db; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    .risk-high {{ color: #e74c3c; font-weight: bold; }}
                    .risk-medium {{ color: #f39c12; font-weight: bold; }}
                    .risk-low {{ color: #27ae60; font-weight: bold; }}
                    .footer {{ margin-top: 30px; border-top: 1px solid #ddd; padding-top: 10px; }}
                </style>
            </head>
            <body>
                {html_content}
                <div class="footer">
                    <p>이 보고서는 AI 윤리성 리스크 진단 시스템에 의해 생성되었습니다.</p>
                    <p>생성일: {datetime.datetime.now().strftime("%Y년 %m월 %d일")}</p>
                </div>
            </body>
            </html>
            """
            
            # HTML을 PDF로 변환
            HTML(string=styled_html).write_pdf(pdf_filepath)
            print(f"✅ PDF 보고서가 생성되었습니다: {pdf_filepath}")
        except Exception as e:
            print(f"⚠️ PDF 생성 실패: {str(e)}")
        
        # 파일 경로 반환 (기존 코드와 호환성 유지)
        return md_filepath
                        

    def generate(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        전체 보고서 생성 프로세스 실행
        
        Args:
            state: 현재 시스템 상태
            
        Returns:
            업데이트된 시스템 상태
        """
        # 상태에서 필요한 정보 추출
        service_analysis = state.get("service_analysis", {})
        risk_assessment = state.get("risk_assessment", {})
        recommendations = state.get("recommendations", {})
        service_name = service_analysis.get("service_name", state.get("service_name", ""))
        domain_info = state.get("domain_info", "일반")
        domain_focus = state.get("domain_focus", "모든 측면")
        
        # 필요한 정보가 충분한지 확인
        if not service_analysis or not risk_assessment or not recommendations:
            print("⚠️ 보고서 생성에 필요한 정보가 부족합니다.")
            return state
        
        print(f"\n📝 '{service_name}' 서비스에 대한 윤리 리스크 진단 보고서 생성을 시작합니다...")
        print(f"📊 도메인: {domain_info} | 중점 분석 요소: {domain_focus}")
        
        # 1. 보고서 구조 설계
        print("\n📋 보고서 구조 설계 중...")
        report_structure = self.create_report_structure(
            service_analysis, risk_assessment, recommendations, domain_info, domain_focus
        )
        
        # 2. 요약(Executive Summary) 작성
        print("✍️ 보고서 요약(Executive Summary) 작성 중...")
        executive_summary = self.generate_executive_summary(
            service_name, service_analysis, risk_assessment,
            recommendations, domain_info, domain_focus
        )
        
        # 3. 각 섹션 생성
        print("✍️ 서론 섹션 작성 중...")
        introduction = self.generate_introduction(
            service_name, service_analysis, domain_info, domain_focus
        )
        
        print("✍️ 서비스 개요 섹션 작성 중...")
        service_overview = self.generate_service_overview(
            service_name, service_analysis, domain_info, domain_focus
        )
        
        print("✍️ 리스크 평가 섹션 작성 중...")
        risk_assessment_section = self.generate_risk_assessment_section(
            service_name, service_analysis, risk_assessment, domain_info, domain_focus
        )
        
        print("✍️ 규정 준수 상태 섹션 작성 중...")
        compliance_section = self.generate_compliance_section(
            service_name, risk_assessment, domain_info
        )
        
        print("✍️ 개선 권고안 섹션 작성 중...")
        recommendations_section = self.generate_recommendations_section(
            service_name, service_analysis, risk_assessment,
            recommendations, domain_info, domain_focus
        )
        
        print("✍️ 결론 섹션 작성 중...")
        conclusion = self.generate_conclusion(
            service_name, risk_assessment, recommendations, domain_info, domain_focus
        )
        
        # 4. 시각화 제안
        print("🎨 시각화 요소 제안 중...")
        visualization_suggestions = self.suggest_visualizations(
            service_name, risk_assessment, recommendations, domain_info
        )
        
        # 5. 최종 보고서 조립
        print("📄 최종 보고서 조립 중...")
        final_report = self.assemble_final_report(
            service_name, executive_summary, introduction, service_overview,
            risk_assessment_section, compliance_section, recommendations_section,
            conclusion, visualization_suggestions
        )
        
        # 6. 보고서 저장
        print("💾 보고서 파일 저장 중...")
        report_filepath = self.save_report_to_file(final_report, service_name)
        
        # PDF 파일 경로 추론 (마크다운 파일 경로에서 확장자만 변경)
        pdf_filepath = report_filepath.replace('.md', '.pdf')
        pdf_exists = os.path.exists(pdf_filepath)
        
        # 보고서 생성 정보 저장
        report_generation = {
            "report_structure": report_structure.get("structure", ""),
            "executive_summary": executive_summary,
            "introduction": introduction,
            "service_overview": service_overview,
            "risk_assessment_section": risk_assessment_section,
            "compliance_section": compliance_section,
            "recommendations_section": recommendations_section,
            "conclusion": conclusion,
            "visualization_suggestions": visualization_suggestions,
            "final_report": final_report,
            "report_filepath": report_filepath,
            "pdf_filepath": pdf_filepath if pdf_exists else None
        }
        
        # 결과 로그
        # print(f"\n✅ 윤리 리스크 진단 보고서가 생성되었습니다.")
        # print(f"📄 보고서 파일: {report_filepath}")
        print(f"\n✅ 윤리 리스크 진단 보고서가 생성되었습니다.")
        print(f"📄 마크다운 보고서: {report_filepath}")
        if pdf_exists:
            print(f"📑 PDF 보고서: {pdf_filepath}")
                
        # 상태 업데이트
        state["report_generation"] = report_generation
        
        return state


# 단독 테스트용 코드
if __name__ == "__main__":
    report_generator = ReportGenerator()
    
    # 테스트용 데이터
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
            "oecd_ai_principles": {"status": "부분 준수", "reason": "투명성 원칙 불충족"},
            "unesco_recommendation": {"status": "미준수", "reason": "포용성 측면에서 기준 미달"}
        }
    }
    
    test_recommendations = {
        "high_priority": [
            "환자 데이터 익명화 강화",
            "다양한 인구통계학적 그룹의 데이터 수집"
        ],
        "medium_priority": [
            "설명 가능한 AI 기능 구현",
            "정기적인 편향성 감사 체계 수립"
        ],
        "low_priority": [
            "외부 윤리 위원회 설립",
            "사용자 피드백 시스템 구축"
        ],
        "implementation_complexity": {
            "환자 데이터 익명화 강화": "중",
            "다양한 인구통계학적 그룹의 데이터 수집": "상"
        },
        "expected_impact": {
            "환자 데이터 익명화 강화": "프라이버시 리스크 40% 감소",
            "다양한 인구통계학적 그룹의 데이터 수집": "편향성 리스크 30% 감소"
        }
    }
    
    # 테스트 실행
    initial_state = {
        "service_name": "의료 영상 진단 AI",
        "domain_info": "의료",
        "domain_focus": "환자 프라이버시와 안전성",
        "service_analysis": test_service_analysis,
        "risk_assessment": test_risk_assessment,
        "recommendations": test_recommendations
    }
    
    result_state = report_generator.generate(initial_state)
    print("\n보고서 생성 완료!")
    print(f"파일 경로: {result_state['report_generation']['report_filepath']}")
