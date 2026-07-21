from pydantic import BaseModel
from app.schemas.search_result import SearchResult

class SearchResponse(BaseModel):
    success: bool
    message: str
    results:list[SearchResult]