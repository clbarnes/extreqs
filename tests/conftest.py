from pathlib import Path

import pytest

here = Path(__file__).resolve().parent


@pytest.fixture
def fixture_dir():
    return here / "fixtures"
