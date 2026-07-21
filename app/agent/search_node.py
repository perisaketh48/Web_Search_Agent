import logfire

from app.agent.state import AgentState
from app.services.search_service import SearchService

search_service = SearchService()


def search_node(state: AgentState) -> AgentState:
    with logfire.span(
        "Web Search",
        query=state.query,
    ):
        try:
            response = search_service.search(
                query=state.query,
            )

            state.search_results = response.results

            logfire.info(
                "Search completed",
                results_found=len(response.results),
            )

            return state
        except Exception:
            logfire.exception("Failed to execute Search",query=state.query,)
            raise