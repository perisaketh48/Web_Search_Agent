from pydantic import BaseModel

class SearchResult(BaseModel):
    def to_prompt(self) -> str:
        return f"""
        Title: {self.title}
        Content: {self.content}
        Source: {self.url}
        """
    
    title: str
    url:str
    content: str
    score: float