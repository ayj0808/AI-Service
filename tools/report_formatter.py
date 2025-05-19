#보고서 포맷팅 도구
from typing import Dict, List, Any, Optional
import re
import json
import markdown
from datetime import datetime
import os

class ReportFormatter:
    """
    AI 윤리성 리스크 진단 보고서를 다양한 형식으로 포맷팅하는 도구
    """

    def __init__(self):
        pass

    def format_markdown(self, content: Dict[str, Any], template_path: Optional[str] = None) -> str:
        """
        보고서 내용을 마크다운 형식으로 포맷팅
        
        Args:
            content: 보고서 내용
            template_path: 마크다운 템플릿 파일 경로 (없으면 기본 템플릿 사용)
            
        Returns:
            마크다운 형식의 보고서
        """
        # 기본 템플릿 사용
        if not template_path:
            markdown_template = """
# AI 윤리성 리스크 진단 보고서: {service_name}

**생성일시**: {date}  
**분석 도메인**: {domain_info}  
**중점 분석 요소**: {domain_focus}

## SUMMARY

{executive_summary}

## 1. 서론

{introduction}

## 2. 서비스 개요

{service_overview}

## 3. 윤리적 리스크 평가

{risk_assessment}

### 3.1 편향성 및 공정성 (점수: {bias_score}/10)

{bias_assessment}

### 3.2 프라이버시 및 데이터 보호 (점수: {privacy_score}/10)

{privacy_assessment}

### 3.3 투명성 및 설명가능성 (점수: {transparency_score}/10)

{transparency_assessment}

### 3.4 책임성 및 거버넌스 (점수: {accountability_score}/10)

{accountability_assessment}

## 4. 규정 준수 상태

{compliance_section}

## 5. 개선 권고안

{recommendations_section}

### 5.1 단기 개선 사항 (0-3개월)

{high_priority_recommendations}

### 5.2 중기 개선 사항 (3-6개월)

{medium_priority_recommendations}

### 5.3 장기 개선 사항 (6-12개월)

{low_priority_recommendations}

## 6. 결론

{conclusion}

---
*본 보고서는 자동화된 AI 윤리성 리스크 진단 시스템에 의해 생성되었습니다.*
"""
        else:
            # 지정된 템플릿 파일 로드
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    markdown_template = f.read()
            except Exception as e:
                print(f"⚠️ 템플릿 파일 로드 오류: {str(e)}")
                # 기본 템플릿 사용
                markdown_template = "# {service_name} 윤리성 리스크 진단 보고서\n"
