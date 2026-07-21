from pydantic import BaseModel, Field
from app.schemas.knowledge import Knowledge
from app.schemas.search_result import SearchResult
from app.schemas.credentials import Credentials


class AgentState(BaseModel):
    query: str

    retrieved_knowledge: list[Knowledge] = Field(default_factory=list)

    search_results: list[SearchResult] = Field(default_factory=list)

    summary: str = ""

    reasoning: str = ""

    should_search: bool = False

    final_answer: str = ""

    credentials: Credentials = Credentials()