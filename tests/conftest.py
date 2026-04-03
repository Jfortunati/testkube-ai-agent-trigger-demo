import os
import pytest


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the calculator service.

    In a Testkube Test Workflow, CALCULATOR_HOST is injected via the
    services.app.0.ip template variable. Defaults to localhost for local runs.
    """
    host = os.environ.get("CALCULATOR_HOST", "localhost")
    port = os.environ.get("CALCULATOR_PORT", "5000")
    return f"http://{host}:{port}"
