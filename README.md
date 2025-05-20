# AI 윤리성 리스크 진단 시스템
본 프로젝트는 AI 서비스의 윤리적 리스크를 진단하고 개선 권고안을 제시하는 에이전트 시스템을 설계하고 구현한 실습 프로젝트입니다.

# Overview
목적: 특정 AI 서비스를 대상으로 윤리적 리스크(편향성, 프라이버시 침해, 투명성 부족 등)를 분석하고, 개선 권고안 작성

방법론: 순차적 피드백 루프 아키텍처, 다중 에이전트 협업, 리스크 평가 프레임워크, 웹 검색 기반 정보 수집

도구: 윤리 가이드라인 데이터베이스, 리스크 평가 프레임워크, 권고안 생성기, 보고서 템플릿 엔진, PDF 보고서 생성

# Features
-AI 서비스에 대한 포괄적 윤리 리스크 진단 (웹 검색 기반 자동화)
-EU AI Act, UNESCO, OECD 등 주요 윤리 가이드라인 기반 리스크 평가
-도메인별(의료, 금융, 교육 등) 특화된 윤리 평가 기준 적용
-편향성, 프라이버시, 투명성, 책임성 등 다양한 윤리적 측면 평가
-실행 가능한 구체적 개선 권고안 제시
-마크다운 및 PDF 형식의 상세 보고서 자동 생성

# 설치 및 실행 방법
필수 패키지 설치

#기본 라이브러리 설치
pip install -r requirements.txt

#PDF 생성 기능을 위한 추가 패키지
pip install markdown weasyprint

#Windows 사용자 추가 설정
PDF 생성을 위해 GTK 라이브러리 설치가 필요합니다:

1. GTK+ 런타임 환경에서 설치 파일 다운로드 및 실행

2. 설치 완료 후 환경 변수 설정:
set WEASYPRINT_DLL_DIRECTORIES=C:\Program Files\GTK3-Runtime Win64\bin

#실행 방법
python app.py


Tech Stack
Category	Details
Framework	LangGraph, LangChain, Python
LLM	GPT-4o-mini via OpenAI API
Retrieval	FAISS, RAG
PDF Generation	WeasyPrint
Web Search	Custom Search Tool



# Agents
서비스 분석 에이전트: AI 서비스 개요 파악 (대상 기능 정리, 주요 특징 등)

윤리 리스크 진단 에이전트: 편향성, 개인정보, 설명가능성 등 윤리성 항목별 리스크 평가

개선안 제안 에이전트: 윤리성 강화를 위한 구체적 개선 방향 제안

리포트 작성 에이전트: 진단 결과 및 권고사항 리포트 생성 (마크다운 및 PDF)

# State
service_analysis: 대상 AI 서비스의 기능, 특징, 데이터 유형, 의사결정 과정에 대한 분석 정보

risk_assessment: 윤리 가이드라인에 따른 리스크 평가 결과, 점수, 증거

recommendations: 각 리스크에 대한 개선 권고사항과 우선순위

report_generation: 최종 보고서 구조와 주요 강조점

# Architecture

[서비스 분석 에이전트] → [윤리 리스크 진단 에이전트] → [개선안 제안 에이전트] → [리포트 작성 에이전트]
          ↑                         |
          └─────────────────────────┘
                 피드백 루프
# Directory Structure

```
AI-Service/
├── README.md                 # 프로젝트 설명
├── app.py                    # 메인 실행 파일
├── requirements.txt          # 필요 패키지 목록
├── agents/                   # 에이전트 모듈
│   ├── __init__.py
│   ├── service_analyzer.py   # 서비스 분석 에이전트
│   ├── risk_assessor.py      # 윤리 리스크 진단 에이전트
│   ├── recommender.py        # 개선안 제안 에이전트
│   └── report_generator.py   # 리포트 작성 에이전트
├── prompts/                  # 프롬프트 템플릿
│   ├── __init__.py
│   ├── service_analysis.py   # 서비스 분석 프롬프트
│   ├── risk_assessment.py    # 리스크 평가 프롬프트
│   ├── recommendations.py    # 권고사항 프롬프트
│   └── report_generation.py  # 보고서 생성 프롬프트
├── tools/                    # 도구 모듈
│   ├── __init__.py
│   ├── guideline_rag.py      # 윤리 가이드라인 검색 도구
│   ├── risk_calculator.py    # 리스크 평가 계산기
│   ├── domain_adapter.py     # 도메인 특화 어댑터
│   ├── report_formatter.py   # 보고서 포맷팅 도구
│   └── web_search.py         # 웹 검색 기능
├── data/                     # 참조 데이터/가이드라인
│   ├── guidelines/
│   │   ├── oecd_ai_ethics.txt      # OECD AI 윤리 가이드라인
│   │   └── risk_framework.txt      # AI 리스크 관리 프레임워크
│   └── domain_info/
│       ├── healthcare.json         # 의료 분야 특화 정보
│       ├── finance.json            # 금융 분야 특화 정보
│       └── education.json          # 교육 분야 특화 정보
└── outputs/                 # 출력 결과 저장
    ├── reports/             # 생성된 보고서 (마크다운, PDF)
    └── visualizations/
```

테스트 권장 AI 서비스
교육 도메인
Cognii: NLP 기반 가상 학습 도우미, 작문 과제에 실시간 피드백 제공

Century Tech: 실시간 학생 진도 평가 및 개인화된 학습 경로 제공

금융 도메인
Zest AI: 대출 결정 자동화 및 최적화 AI 시스템

CredoLab: 스마트폰 메타데이터 활용 대안적 신용 평가 시스템

의료 도메인
IBM Watson (의료): 유전 데이터 분석을 통한 희귀 질환 진단 및 맞춤형 치료법 제안

Siemens Healthineers의 Atellica: 환자 데이터 분석을 통한 질병 진행 예측

Contributors
안예진: Architecture Design, Agent Design, Prompt Engineering, PDF Generation