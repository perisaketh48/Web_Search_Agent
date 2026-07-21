import logfire
from app.services.llm_service import LLMService
from app.agent.state import AgentState
from app.services.summarization_service import SummarizationService



def summarization_node(state: AgentState) -> AgentState:

    llm_service = LLMService(
    credentials=state.credentials,
)

    summarization_service = SummarizationService(
        llm=llm_service,
    )

    with logfire.span(
        "Summarization",
        query=state.query,
        search_results=len(state.search_results),
    ):
        try:
            state.summary = summarization_service.summarize(
                query=state.query,
                search_results=state.search_results,
            )

            logfire.info("Summary generated")

            return state
        
        except Exception:
            logfire.exception("Failed to summarize search results",query=state.query,)
            raise