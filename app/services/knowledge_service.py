from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService
from app.schemas.knowledge import Knowledge
import logfire

class KnowledgeService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()


    def store(self, knowledge: Knowledge)-> Knowledge:
        with logfire.span("Knowledge Store",knowledge_id=knowledge.id,):
            try:

                embedding = self.embedding_service.embed(knowledge.embedding_text)

                knowledge_payload  = knowledge.model_dump()

                self.qdrant_service.upsert(point_id=knowledge.id,vector=embedding,payload=knowledge_payload)

                return knowledge
            except Exception:
                logfire.exception("Knowledge storage failed",knowledge_id=knowledge.id,)
                raise



    def search(self, query: str, limit: int = 5) -> list[Knowledge]:
        with logfire.span("Knowledge Search",query=query,):
            try:
                query_embedding = self.embedding_service.embed(query)

                payloads = self.qdrant_service.search(
                    query_embedding,
                    limit=limit,
                )

                return [
                    Knowledge.model_validate(payload)
                    for payload in payloads
                ]
            except Exception:
                    logfire.exception("Knowledge search failed",query=query,)
                    raise


    def delete(self, knowledge_id: str) -> None:
        with logfire.span("Knowledge Delete",knowledge_id=knowledge_id,):
            try:
                self.qdrant_service.delete(knowledge_id)
            except Exception:
                logfire.exception("Knowledge deletion failed", knowledge_id=knowledge_id,)
                raise