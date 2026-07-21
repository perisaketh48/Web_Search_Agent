import logfire

from app.agent.state import AgentState
from app.services.llm_service import LLMService
from app.services.reasoning_service import ReasoningService



def reasoning_node(state: AgentState) -> AgentState:


    llm_service = LLMService(
    credentials=state.credentials,
)
        
    reasoning_service = ReasoningService(llm=llm_service,)
    

    with logfire.span(
        "Reasoning",
        query=state.query,
    ):
        try:
            summaries = [
                item.summary
                for item in state.retrieved_knowledge
            ]

            result = reasoning_service.decide(
                query=state.query,
                summaries=summaries,
            )

            state.should_search = result.should_search
            state.reasoning = result.reasoning

            logfire.info(
                "Reasoning completed",
                should_search=result.should_search,
                knowledge_used=len(summaries),
            )

            return state
        except Exception:
            logfire.exception("Failed to execute reasoning",query=state.query,)
            raise
