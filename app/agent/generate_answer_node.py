import logfire

from app.agent.state import AgentState
from app.services.generate_answer import GenerateAnswerService
from app.services.llm_service import LLMService



def generate_answer_node(state: AgentState) -> AgentState:
    llm_service = LLMService(
        credentials=state.credentials,
    )

    generate_answer_service = GenerateAnswerService(
        llm=llm_service,
    )


    with logfire.span(
        "Generate Answer",
        query=state.query,
    ):
        try:
            state.final_answer = generate_answer_service.generate(
    query=state.query,
    retrieved_knowledge=state.retrieved_knowledge,
    summary=state.summary,
)

            logfire.info("Answer generated")

            return state
        except Exception:
            logfire.exception("Failed to generate final answer",query=state.query,)
            raise