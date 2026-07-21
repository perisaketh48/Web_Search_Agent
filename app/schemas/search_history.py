from uuid import uuid4
from datetime import datetime

from pydantic import BaseModel, Field


class SearchHistory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    query: str
    answer: str
    provider: str = "unknown"
    timestamp: datetime = Field(default_factory=datetime.now)