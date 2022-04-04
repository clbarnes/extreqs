import pytest
from pathlib import Path

here = Path(__file__).resolve().parent


@pytest.fixture
def fixture_dir():
    return here / "fixtures"
