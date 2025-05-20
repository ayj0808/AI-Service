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
    AI 윤리 가이드라인 정보 검색 도구(로컬문서 + 웹 검색 하이브리드 방식)
    """

    def __init__(self, model_name="gpt-4o-mini", embeddings_model="text-embedding-3-small"):
        # 임베딩 및 LLM 모델 초기화
        self.embeddings = OpenAIEmbeddings(model=embeddings_model)
        self.llm = ChatOpenAI(model=model_name, temperature=0.2)
        
        # 벡터 저장소 및 가이드라인 정보 초기화
        self.vector_store = None
        self.guidelines_info = {}
        
        # 벡터 저장소 초기화 (로컬 PDF/TXT 파일 로드)
        self._initialize_vector_store()
        
        # API 키 설정 (환경 변수에서 로드)
        self.serpapi_key = os.getenv("SERPAPI_KEY")
        
    def _initialize_vector_store(self):
        """윤리 가이드라인 문서를 로드하고 벡터 스토어 초기화"""
        guidelines_dir = "data/guidelines"
        
        # 디렉토리가 존재하는지 확인 없으면 생성
        if not os.path.exists(guidelines_dir):
            os.makedirs(guidelines_dir, exist_ok=True)
            # 기본 가이드라인 파일 생성
            self._create_sample_guidelines(guidelines_dir) #샘플 파일 생성
        
        # 문서 로드
        documents = []
        
        for filename in os.listdir(guidelines_dir):
            filepath = os.path.join(guidelines_dir, filename)
            
            try:
                #PDF 파일 처리
                if filename.endswith('.pdf'):
                    loader = PyPDFLoader(filepath)
                    file_docs = loader.load()
                    # 문서 메타데이터에 출처 추가
                    for doc in file_docs:
                        doc.metadata["source"] = filename
                    documents.extend(file_docs)
                    self.guidelines_info[filename] = {"type": "pdf", "pages": len(file_docs)}
                #텍스트 파일 처리
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
        #문서가 없으면 종료
        if not documents:
            print("⚠️ 가이드라인 문서가 로드되지 않았습니다.")
            return
        
        # 문서 분할
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=100
        )
        splits = text_splitter.split_documents(documents)
        
        # 벡터 저장소(스토어) 생성 -> 디스크 저장 X 메모리 저장 코드
        self.vector_store = FAISS.from_documents(splits, self.embeddings)
        print(f"✅ {len(splits)}개의 윤리 가이드라인 청크가 로드되었습니다.")
        
    def search_web(self, query: str) -> str:
        """웹 검색을 통해 최신 정보 가져오기"""
        if not self.serpapi_key:
            # API 키가 없으면 간단한 메시지 반환
            return "웹 검색을 사용하려면 SERPAPI_KEY 환경 변수를 설정하세요."
        
        try:
            # SerpAPI를 이용한 웹 검색
            url = "https://serpapi.com/search"
            params = {
                "q": query,
                "api_key": self.serpapi_key,
                "num": 3  # 상위 3개 결과만
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            # 검색 결과 추출
            results = []
            if "organic_results" in data:
                for result in data["organic_results"][:3]:
                    results.append(f"제목: {result.get('title')}\n"
                                 f"요약: {result.get('snippet')}\n"
                                 f"링크: {result.get('link')}\n")
            
            return "\n\n".join(results)
            
        except Exception as e:
            return f"웹 검색 오류: {str(e)}"

    def query_hybrid(self, query: str, domain_info: str = "", 
                    ethical_aspect: str = "", use_web_search: bool = True) -> Dict[str, Any]:
        """로컬 가이드라인과 웹 검색을 결합한 하이브리드 검색"""
        # 쿼리 개선 (도메인과 윤리적 측면 포함)
        enhanced_query = f"{query} {domain_info} {ethical_aspect} AI 윤리"
        
        # 1. 로컬 가이드라인 검색
        local_results = self.search_local_guidelines(enhanced_query)
        
        # 2. 웹 검색 (선택적)
        web_results = ""
        if use_web_search:
            print("🔎 웹에서 최신 정보 검색 중...")
            web_results = self.search_web(enhanced_query)
        
        # 3. 결과 결합 및 분석
        combined_info = self._combine_and_analyze(query, local_results, web_results, domain_info, ethical_aspect)
        
        return {
            "local_results": local_results,
            "web_results": web_results if use_web_search else "웹 검색 사용 안함",
            "combined_analysis": combined_info
        }
    
    def search_local_guidelines(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """로컬 가이드라인 문서에서 관련 정보 검색"""
        # 벡터 저장소가 없으면 빈 결과 반환
        if not self.vector_store:
            return []
        
        # 벡터 유사도 검색 실행
        results = self.vector_store.similarity_search_with_score(query, k=n_results)
        
        # 결과 가공
        formatted_results = []
        for doc, score in results:
            # 점수를 관련도로 변환 (낮을수록 관련성 높음)
            relevance = 1.0 / (1.0 + score)
            
            formatted_results.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "알 수 없음"),
                "relevance": round(relevance, 3)
            })
        
        return formatted_results
    
    def _combine_and_analyze(self, query: str, local_results: List[Dict[str, Any]], 
                           web_results: str, domain_info: str, ethical_aspect: str) -> str:
        """로컬 가이드라인과 웹 검색 결과를 결합하여 분석"""
        # 로컬 가이드라인 텍스트 추출
        local_texts = []
        for result in local_results:
            local_texts.append(f"출처: {result['source']} (관련도: {result['relevance']})\n"
                             f"내용: {result['content']}")
        
        local_content = "\n\n".join(local_texts)
        
        # 분석 프롬프트 생성
        prompt = f"""
        다음은 "{query}"에 관한 정보입니다:
        
        ## 로컬 가이드라인 정보:
        {local_content}
        
        ## 웹 검색 결과:
        {web_results}
        
        위 정보를 종합하여 {domain_info} 도메인에서 {ethical_aspect} 관련 AI 윤리 지침과 
        모범 사례를 요약해주세요. 로컬 가이드라인의 핵심 원칙과 웹에서 찾은 최신 정보를 
        결합하여 설명해주세요.
        """
        
        # LLM으로 종합 분석
        response = self.llm.invoke(prompt)
        return response.content

    # 기존 메소드들은 간단하게 유지 (호환성 위해)
    def query_guidelines(self, query: str, domain_info: Optional[str] = None, 
                      ethical_aspect: Optional[str] = None) -> Dict[str, Any]:
        """기존 API와의 호환성을 위한 메소드"""
        # 하이브리드 검색 호출
        results = self.query_hybrid(
            query=query,
            domain_info=domain_info or "",
            ethical_aspect=ethical_aspect or ""
        )
        
        return {
            "search_results": results["local_results"],
            "web_results": results["web_results"],
            "combined_analysis": results["combined_analysis"],
            "recommended_guidelines": self._get_recommended_guidelines(results["local_results"])
        }
    
    def _get_recommended_guidelines(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """검색 결과에서 추천 가이드라인 추출"""
        recommended = []
        for result in results:
            source = result["source"]
            if source not in [g.get("source") for g in recommended]:
                recommended.append({
                    "source": source,
                    "relevance": result["relevance"]
                })
        
        return sorted(recommended, key=lambda x: x["relevance"], reverse=True)

    def _create_sample_guidelines(self, directory: str):
        """샘플 가이드라인 파일 생성 (필요시)"""
        # 샘플 데이터 생략 - 기존 함수 유지
        pass
