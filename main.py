from app.telemetry.logfire_config import configure_logfire
from start import initialize_application
from app.ui.home import run_app

configure_logfire()
initialize_application()

run_app()