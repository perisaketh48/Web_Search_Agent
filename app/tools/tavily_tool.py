from tavily import TavilyClient
from app.config.settings import settings
from app.config import constants



class TavilyTool:
    def __init__(self):
        self.client = TavilyClient(api_key=settings.tavily_api_key)

    def search_with_tavily(self, query: str):
        response = self.client.search(query=query,max_results=constants.DEFAULT_SEARCH_RESULTS)
        return response
        
