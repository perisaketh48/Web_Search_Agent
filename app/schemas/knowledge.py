from pydantic import BaseModel
from app.schemas.search_result import SearchResult
from datetime import datetime

class Knowledge(BaseModel):
    @property
    def embedding_text(self) -> str:
        return f"{self.query}\n{self.summary}"
    
    id:str
    query:str
    summary: str
    search_results: list[SearchResult]
    sources: list[str]
    created_at: datetime
    updated_at: datetime