import logfire
from app.services.llm_service import LLMService
from app.schemas.ReasoningResult import ReasoningResult
from app.prompts.reasoning_prompt import REASONING_SYSTEM_PROMPT


class ReasoningService:


    def __init__(
            self,
            llm: LLMService,
        ):
            self.llm = llm


    def decide(self,query: str, summaries: list[str],) -> ReasoningResult:
        with logfire.span(
    "Reasoning Service",
    knowledge_count=len(summaries),
):
            try:
                user_prompt = f"""
        User Query:
        {query}

        Retrieved Knowledge Summaries:
        {chr(10).join(summaries)}
        """
                return self.llm.generate_structured(
                    system_prompt=REASONING_SYSTEM_PROMPT,
                    user_prompt=user_prompt,
                    response_model=ReasoningResult,
                )
            except Exception:
                logfire.exception(
                    "Reasoning service failed",
                    knowledge_count=len(summaries),
                )
                raise