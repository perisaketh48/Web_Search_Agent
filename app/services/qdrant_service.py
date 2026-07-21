from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)
import logfire
from app.config.settings import settings


class QdrantService:

    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )



    def create_collection(self):
        """
        Creates the collection if it doesn't already exist.
        """

        if self.client.collection_exists(settings.QDRANT_COLLECTION):
            logfire.info("Qdrant collection already exists", collection=settings.QDRANT_COLLECTION,)
        return
            

        with logfire.span("Create Qdrant Collection"):
            try:
                self.client.create_collection(
                    collection_name=settings.QDRANT_COLLECTION,
                    vectors_config=VectorParams(
                        size=settings.EMBEDDING_DIMENSION,
                        distance=Distance.COSINE,
                    ),
                )
            except Exception:
                logfire.exception("Failed to create Qdrant collection")
                raise
        
    def upsert(
        self,
        point_id: str,
        vector: list[float],
        payload: dict,
    ):
        """
        Insert or update a vector.
        """
        with logfire.span("Qdrant Upsert",point_id=point_id,):
            try:
                self.client.upsert(
                    collection_name=settings.QDRANT_COLLECTION,
                    wait=True,
                    points=[
                        PointStruct(
                            id=point_id,
                            vector=vector,
                            payload=payload,
                        )
                    ],
                )
            except Exception:
                logfire.exception(
                    "Qdrant upsert failed",
                    point_id=point_id,
                )
                raise

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ):
        """
        Search similar vectors.
        """
        with logfire.span("Qdrant Search",collection=settings.QDRANT_COLLECTION, limit=limit,):
            try:
                results = self.client.query_points(
                    collection_name=settings.QDRANT_COLLECTION,
                    query=query_vector,
                    limit=limit,
                )

                return [point.payload for point in results.points]
            except Exception:
                logfire.exception(
                    "Qdrant search failed",
                    limit=limit,
                )
                raise

    def delete(self, point_id: str):
        """
        Delete a point by id.
        """
        with logfire.span("Qdrant Delete",point_id=point_id,):
            try:
                self.client.delete(
                    collection_name=settings.QDRANT_COLLECTION,
                    points_selector=[point_id],
                )
            except Exception:
                logfire.exception("Qdrant delete failed", point_id=point_id,)
                raise