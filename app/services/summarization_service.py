import logfire
from app.services.llm_service import LLMService
from app.schemas.search_result import SearchResult
from app.prompts.summarization_prompt import SUMMARIZATION_SYSTEM_PROMPT

class SummarizationService:

    def __init__(
        self,
        llm: LLMService,
    ):
        self.llm = llm

    def summarize(
        self,
        query: str,
        search_results: list[SearchResult],
    ) -> str:
        with logfire.span(
    "Summarization Service",
    result_count=len(search_results),
):
            try:
                formatted_results = "\n\n".join(
            result.to_prompt()
            for result in search_results
        )

                user_prompt = f"""
                User Query:
                {query}

                Search Results:

                {formatted_results}
                """
                return self.llm.generate(
                    system_prompt=SUMMARIZATION_SYSTEM_PROMPT,
                    user_prompt=user_prompt,
                )
            except Exception:
                logfire.exception(
                    "Summarization service failed",
                    result_count=len(search_results),
                )
                raise