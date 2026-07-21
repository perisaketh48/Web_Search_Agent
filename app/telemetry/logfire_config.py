import logfire
from app.config.settings import settings

def configure_logfire():
    print(settings.logfire_token)
    logfire.configure(
        token=settings.logfire_token,
        service_name="ai-search-agent",
    )