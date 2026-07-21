import logfire
from sentence_transformers import SentenceTransformer
from app.config.settings import settings

class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)

    def embed(self, text: str) -> list[float]:
       with logfire.span(
        "Generate Embedding",model=settings.embedding_model,
    ):
        try:
            embedding = self.model.encode(text).tolist()
            return embedding

        except Exception:
            logfire.exception(
                "Embedding generation failed",
            )
            raise
