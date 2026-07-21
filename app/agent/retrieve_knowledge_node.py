import logfire

from app.agent.state import AgentState
from app.services.knowledge_service import KnowledgeService

knowledge_service = KnowledgeService()


def retrieve_knowledge_node(state: AgentState) -> AgentState:
    with logfire.span(
        "Retrieve Knowledge",
        query=state.query,
    ):
        try:
            retrieved_knowledge = knowledge_service.search(state.query)

            state.retrieved_knowledge = retrieved_knowledge

            logfire.info(
                "Knowledge retrieved",
                knowledge_count=len(retrieved_knowledge),
            )

            return state

        except Exception:
            logfire.exception(
                "Failed to retrieve knowledge",
                query=state.query,
            )
            raise