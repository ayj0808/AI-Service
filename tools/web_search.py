#웹 검색 기능 Tool
# tools/web_search.py
from typing import Dict, List, Any
import requests
import os

class WebSearchTool:
    """웹 검색을 통해 AI 서비스 정보를 수집하는 도구"""
    
    def __init__(self):
        # API 키 설정 (환경 변수에서 로드)
        self.serpapi_key = os.getenv("SERPAPI_KEY")
    
    def search_service_info(self, service_name: str, domain_info: str) -> str:
        """서비스에 대한 정보 검색"""
        query = f"{service_name} {domain_info} AI 서비스 특징"
        
        # API 키가 있으면 실제 검색, 없으면 모의 결과 생성
        if self.serpapi_key:
            return self._real_search(query)
        else:
            print("ℹ️ 검색 API 키가 없어 모의 검색 결과를 생성합니다")
            return self._generate_mock_results(service_name, domain_info)
    
    def _real_search(self, query: str) -> str:
        """실제 SerpAPI 검색 수행"""
        try:
            url = "https://serpapi.com/search"
            params = {
                "q": query,
                "api_key": self.serpapi_key
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            results = []
            if "organic_results" in data:
                for result in data["organic_results"][:3]:
                    results.append(f"제목: {result['title']}\n"
                                  f"설명: {result['snippet']}\n"
                                  f"URL: {result['link']}\n")
            
            return "\n".join(results)
        except Exception as e:
            return f"검색 중 오류 발생: {str(e)}"
    
    def _generate_mock_results(self, service_name: str, domain_info: str) -> str:
        """API 키 없을 때 모의 검색 결과 생성"""
        return f"""
        {service_name} 정보:
        - {domain_info} 분야의 AI 기반 서비스로, 최신 머신러닝 알고리즘 활용
        - 사용자 개인화 기능과 자연어 처리 기술로 상호작용성 제공
        - 데이터 보안 및 프라이버시 보호 기능 내장
        - 클라우드 기반으로 구축되어 다양한 기기에서 접근 가능
        """
