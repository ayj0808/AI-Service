#TITLE
AI 윤리성 리스크 진단 시스템
본 프로젝트는 AI 서비스의 윤리적 리스크를 진단하고 개선 권고안을 제시하는 에이전트를 설계하고 구현한 실습 프로젝트입니다.

#Overview
Objective: 특정 AI 서비스를 대상으로 윤리적 리스크(편향성, 프라이버시 침해, 투명성 부족 등)를 분석하고, 개선 권고안 작성

Methods: 순차적 피드백 루프 아키텍처, 다중 에이전트 협업, 리스크 평가 프레임워크

Tools: 윤리 가이드라인 데이터베이스, 리스크 평가 프레임워크, 권고안 생성기, 보고서 템플릿 엔진

#Features
최대 3개 AI 서비스에 대한 포괄적 윤리 리스크 진단

EU AI Act, UNESCO, OECD 등 주요 윤리 가이드라인 기반 리스크 평가

편향성, 프라이버시, 투명성, 책임성 등 다양한 윤리적 측면 평가

실행 가능한 구체적 개선 권고안 제시

#Tech Stack
Category	Details
Framework	LangGraph, LangChain, Python
LLM	GPT-4o-mini via OpenAI API
Retrieval	FAISS, Chroma

#Agents
서비스 분석 에이전트: AI 서비스 개요 파악 (대상 기능 정리, 주요 특징 등)

윤리 리스크 진단 에이전트: 편향성, 개인정보, 설명가능성 등 윤리성 항목별 리스크 평가

개선안 제안 에이전트: 윤리성 강화를 위한 구체적 개선 방향 제안

리포트 작성 에이전트: 진단 결과 및 권고사항 리포트 생성

#State
service_analysis: 대상 AI 서비스의 기능, 특징, 데이터 유형, 의사결정 과정에 대한 분석 정보

risk_assessment: 윤리 가이드라인에 따른 리스크 평가 결과, 점수, 증거

recommendations: 각 리스크에 대한 개선 권고사항과 우선순위

report_generation: 최종 보고서 구조와 주요 강조점

#Architecture

[서비스 분석 에이전트] → [윤리 리스크 진단 에이전트] → [개선안 제안 에이전트] → [리포트 작성 에이전트]
          ↑                         |
          └─────────────────────────┘
                 피드백 루프


#Directory Structure
text
├── data/                  # 윤리 가이드라인 참조 문서
├── agents/                # 각 에이전트 모듈
│   ├── service_analyzer.py   # 서비스 분석 에이전트
│   ├── risk_assessor.py      # 윤리 리스크 진단 에이전트
│   ├── recommender.py        # 개선안 제안 에이전트
│   └── report_generator.py   # 리포트 작성 에이전트
├── tools/                 # 에이전트가 사용하는 도구 모듈
│   ├── guideline_rag.py      # 윤리 가이드라인 검색 도구
│   ├── risk_calculator.py    # 리스크 평가 도구
│   └── report_formatter.py   # 보고서 포맷팅 도구
├── prompts/               # 프롬프트 템플릿
├── outputs/               # 평가 결과 저장
├── app.py                 # 실행 스크립트
└── README.md


#Contributors
안예진 : Architecture Design, Agent Design, Prompt Engineering