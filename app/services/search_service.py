import logfire
from app.schemas.search_request import SearchRequest
from app.schemas.search_response import SearchResponse
from app.schemas.search_result import SearchResult

from app.tools.tavily_tool import TavilyTool


class SearchService:
    def __init__(self):
        self.tavily_tool = TavilyTool()

    def search(self, query: str,) -> SearchResponse:
        with logfire.span("Tavily Search",query=query,):
            try:
                tavily_response = self.tavily_tool.search_with_tavily(query)

                required_result=[]
                for result in tavily_response["results"]:
                    required_result.append(
                        SearchResult(
                            title=result["title"],
                            url=result["url"],
                            content=result["content"],
                            score=result["score"]
                        )
                    )

                return SearchResponse(success=True, message="Search completed",results=required_result)
            except Exception:
                logfire.exception(
                "Tavily search failed",
                query=query,
            )
            raise


