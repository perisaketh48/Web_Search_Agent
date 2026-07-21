from pydantic import BaseModel


class ReasoningResult(BaseModel):
    should_search: bool
    reasoning: str