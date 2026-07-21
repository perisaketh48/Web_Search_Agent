from app.prompts.answer_prompt import GENERATE_ANSWER_SYSTEM_PROMPT
from app.schemas.knowledge import Knowledge
from app.schemas.search_result import SearchResult
from app.services.llm_service import LLMService
import logfire

class GenerateAnswerService:

    def __init__(
        self,
        llm: LLMService,
    ):
        self.llm = llm

    def generate(
        self,
        query: str,
        retrieved_knowledge: list[Knowledge],
        summary: str,
    ) -> str:

        with logfire.span(
            "Generate Answer Service",
            knowledge_count=len(retrieved_knowledge),
        ):
            try:
                knowledge_context = "\n\n".join(
                    knowledge.summary
                    for knowledge in retrieved_knowledge
                )

                user_prompt = f"""
User Query:
{query}

Retrieved Knowledge:
{knowledge_context}

Recent Web Summary:
{summary}
"""

                return self.llm.generate(
                    system_prompt=GENERATE_ANSWER_SYSTEM_PROMPT,
                    user_prompt=user_prompt,
                )

            except Exception:
                logfire.exception(
                    "Answer generation service failed",
                    knowledge_count=len(retrieved_knowledge),
                )
                raise