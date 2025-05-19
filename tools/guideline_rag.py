#윤리 가이드라인 검색 도구
from typing import Dict, List, Any, Optional
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader
import os
import json

class GuidelineRAG:
    """
    AI 윤리 가이드라인 문서에서 관련 정보를 검색하는 RAG(Retrieval Augmented Generation) 도구
    """

    def __init__(self, embeddings_model="text-embedding-3-small"):
        self.embeddings = OpenAIEmbeddings(model=embeddings_model)
        self.vector_store = None
        self.guidelines_info = {}
        self._initialize_vector_store()
        
    def _initialize_vector_store(self):
        """윤리 가이드라인 문서를 로드하고 벡터 스토어 초기화"""
        guidelines_dir = "data/guidelines"
        
        # 디렉토리가 존재하는지 확인
        if not os.path.exists(guidelines_dir):
            os.makedirs(guidelines_dir, exist_ok=True)
            # 기본 가이드라인 파일 생성
            self._create_sample_guidelines(guidelines_dir)
        
        # 문서 로드
        documents = []
        
        for filename in os.listdir(guidelines_dir):
            filepath = os.path.join(guidelines_dir, filename)
            
            try:
                if filename.endswith('.pdf'):
                    loader = PyPDFLoader(filepath)
                    file_docs = loader.load()
                    # 문서 메타데이터에 출처 추가
                    for doc in file_docs:
                        doc.metadata["source"] = filename
                    documents.extend(file_docs)
                    self.guidelines_info[filename] = {"type": "pdf", "pages": len(file_docs)}
                
                elif filename.endswith('.txt'):
                    loader = TextLoader(filepath)
                    file_docs = loader.load()
                    # 문서 메타데이터에 출처 추가
                    for doc in file_docs:
                        doc.metadata["source"] = filename
                    documents.extend(file_docs)
                    self.guidelines_info[filename] = {"type": "text", "pages": len(file_docs)}
            
            except Exception as e:
                print(f"⚠️ {filename} 로드 중 오류 발생: {str(e)}")
        
        if not documents:
            print("⚠️ 가이드라인 문서가 로드되지 않았습니다.")
            return
        
        # 문서 분할
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=100
        )
        splits = text_splitter.split_documents(documents)
        
        # 벡터 스토어 생성
        self.vector_store = FAISS.from_documents(splits, self.embeddings)
        print(f"✅ {len(splits)}개의 윤리 가이드라인 청크가 로드되었습니다.")
        
    def _create_sample_guidelines(self, directory: str):
        """샘플 가이드라인 파일 생성"""
        # OECD AI 윤리 원칙 샘플
        oecd_sample = """
        # OECD AI 윤리 원칙
        
        ## 1. 포용적 성장, 지속가능한 발전, 웰빙
        AI 시스템은 인간의 역량을 강화하고, 인간의 창의성을 증진하며, 포용적 성장을 지원하고, 
        모든 사람의 웰빙과 행복을 증진하는 방식으로 설계되어야 합니다.
        
        ## 2. 인간 중심적 가치와 공정성
        AI 시스템은 인간의 자율성, 인권, 다양성, 기본적 자유를 존중하는 방식으로 설계되어야 합니다. 
        AI 시스템은 불공정하거나 편향된 결과를 피하고 공정성을 보장해야 합니다.
        
        ## 3. 투명성과 설명가능성
        AI 시스템의 결정은 사용자와 관계자들이 이해할 수 있어야 하며, 
        그 기능, 결정 방식, 영향에 대한 적절한 정보를 제공해야 합니다.
        
        ## 4. 견고성, 보안성, 안전성
        AI 시스템은 전 생애주기에 걸쳐 안전하게 기능해야 하며, 
        잠재적 위험이 지속적으로 평가되고 관리되어야 합니다.
        
        ## 5. 책임성
        AI 시스템을 설계, 개발, 배포, 운영하는 조직과 개인은 이러한 원칙에 따라 
        적절한 기능을 보장하고 책임을 져야 합니다.
        """
        
        # AI 리스크 관리 프레임워크 샘플
        risk_framework_sample = """
        # AI 리스크 관리 프레임워크
        
        ## 리스크 식별
        - 편향성: AI 시스템이 특정 그룹을 불공정하게 대우하는지 평가
        - 프라이버시: 개인정보 수집, 처리, 저장, 공유 과정의 리스크 식별
        - 투명성 부족: 의사결정 과정이 불투명하거나 설명이 어려운 경우의 리스크
        - 책임성 결여: 문제 발생 시 책임 소재가 불분명한 상황의 리스크
        
        ## 리스크 평가
        - 심각도: 리스크 실현 시 발생할 수 있는 해악의 심각성
        - 발생가능성: 리스크가 실현될 확률
        - 영향 범위: 영향을 받는 사람 또는 시스템의 범위
        - 탐지 가능성: 문제가 발생했을 때 탐지할 수 있는 가능성
        
        ## 리스크 완화
        - 기술적 방법: 편향성 완화 알고리즘, 차등 프라이버시, 설명가능한 AI 도구
        - 절차적 방법: 윤리적 검토 과정, 정기적 감사, 사용자 피드백 메커니즘
        - 거버넌스: 책임 체계 수립, 윤리 위원회 구성, 제3자 검증
        
        ## 모니터링 및 피드백
        - 지속적 평가: 시스템 운영 중 발생하는 새로운 리스크 또는 문제점 지속 평가
        - 성과 측정: 리스크 완화 조치의 효과성 측정
        - 개선 및 적응: 새로운 상황이나 요구사항에 대응하여 시스템 개선
        """
        
        # 파일 저장
        with open(os.path.join(directory, 'oecd_ai_ethics.txt'), 'w', encoding='utf-8') as f:
            f.write(oecd_sample)
        
        with open(os.path.join(directory, 'risk_framework.txt'), 'w', encoding='utf-8') as f:
            f.write(risk_framework_sample)

    def search_guidelines(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """
        윤리 가이드라인에서 관련 정보 검색
        
        Args:
            query: 검색 쿼리
            n_results: 반환할 결과 수
            
        Returns:
            관련 가이드라인 내용과 출처 목록
        """
        if not self.vector_store:
            return [{"content": "가이드라인 데이터가 로드되지 않았습니다.", "source": "없음", "relevance": 0}]
        
        # 벡터 스토어에서 검색
        results = self.vector_store.similarity_search_with_score(query, k=n_results)
        
        # 결과 포맷팅
        formatted_results = []
        for doc, score in results:
            # 점수를 0-1 범위의 관련도로 변환 (점수가 낮을수록 관련성이 높음)
            relevance = 1.0 / (1.0 + score)
            
            formatted_results.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "알 수 없음"),
                "page": doc.metadata.get("page", 0) if "page" in doc.metadata else 0,
                "relevance": round(relevance, 3)
            })
        
        return formatted_results

    def query_guidelines(self, query: str, domain_info: Optional[str] = None, 
                      ethical_aspect: Optional[str] = None) -> Dict[str, Any]:
        """
        특정 도메인과 윤리적 측면에 대한 가이드라인 정보 검색
        
        Args:
            query: 기본 검색 쿼리
            domain_info: 도메인 정보 (예: '의료', '금융')
            ethical_aspect: 윤리적 측면 (예: '편향성', '프라이버시')
            
        Returns:
            검색 결과와 추천 가이드라인
        """
        # 도메인과 측면을 고려한 쿼리 강화
        enhanced_query = query
        
        if domain_info and domain_info.lower() != "일반":
            enhanced_query += f" 도메인: {domain_info}"
        
        if ethical_aspect:
            # 영어 키워드를 한글로 변환
            aspect_korean = {
                "bias": "편향성",
                "privacy": "프라이버시",
                "transparency": "투명성",
                "accountability": "책임성"
            }.get(ethical_aspect.lower(), ethical_aspect)
            
            enhanced_query += f" 윤리적 측면: {aspect_korean}"
        
        # 검색 수행
        results = self.search_guidelines(enhanced_query, n_results=5)
        
        # 관련도가 높은 가이드라인 추출
        relevant_guidelines = []
        for result in results:
            source = result["source"]
            if source not in [g.get("source") for g in relevant_guidelines]:
                relevant_guidelines.append({
                    "source": source,
                    "relevance": result["relevance"]
                })
        
        # 결과 반환
        return {
            "search_results": results,
            "recommended_guidelines": sorted(relevant_guidelines, key=lambda x: x["relevance"], reverse=True)
        }

    def get_loaded_guidelines_info(self) -> Dict[str, Any]:
        """로드된 가이드라인 정보 반환"""
        return {
            "loaded_guidelines": list(self.guidelines_info.keys()),
            "total_chunks": len(self.vector_store.index_to_docstore_id) if self.vector_store else 0,
            "guidelines_details": self.guidelines_info
        }


# 단독 테스트용 코드
if __name__ == "__main__":
    rag = GuidelineRAG()
    
    # 로드된 가이드라인 정보 출력
    print("\n로드된 가이드라인 정보:")
    info = rag.get_loaded_guidelines_info()
    print(f"총 {info['total_chunks']}개의 청크가 로드됨")
    for guideline in info.get("loaded_guidelines", []):
        print(f"- {guideline}")
    
    # 테스트 쿼리
    test_query = "의료 AI에서 프라이버시 보호를 위한 가이드라인"
    results = rag.query_guidelines(
        test_query, 
        domain_info="의료", 
        ethical_aspect="privacy"
    )
    
    # 결과 출력
    print("\n검색 결과:")
    for i, result in enumerate(results["search_results"][:2], 1):
        print(f"\n{i}. 출처: {result['source']} (관련도: {result['relevance']})")
        print(f"내용: {result['content'][:200]}...")
    
    print("\n추천 가이드라인:")
    for guideline in results["recommended_guidelines"]:
        print(f"- {guideline['source']} (관련도: {guideline['relevance']})")
