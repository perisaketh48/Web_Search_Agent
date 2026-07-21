import logfire

from uuid import uuid4
from datetime import datetime

from app.agent.state import AgentState
from app.schemas.knowledge import Knowledge
from app.services.knowledge_service import KnowledgeService

knowledge_service = KnowledgeService()


def store_knowledge_node(state: AgentState) -> AgentState:
    with logfire.span(
        "Store Knowledge",
        query=state.query,
    ):
        try:
            knowledge = Knowledge(
                id=str(uuid4()),
                query=state.query,
                summary=state.summary,
                search_results=state.search_results,
                sources=[result.url for result in state.search_results],
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            knowledge_service.store(knowledge)

            state.retrieved_knowledge.append(knowledge)

            logfire.info(
                "Knowledge stored",
                sources=len(knowledge.sources),
            )

            return state
        
        except Exception:
            logfire.exception("Failed to perform web search",query=state.query,)
            raise