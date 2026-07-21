from app.services.qdrant_service import QdrantService

def initialize_application():
    qdrant = QdrantService()
    qdrant.create_collection()