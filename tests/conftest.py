#   tests/conftest.py
#   session-scoped fixture that manages Containerlab lifecycle

import pytest

@pytest.fixture(scope="session")
def lab(clab) :
    # deploy topology once per test session & tear down after
    return clab("topology/topology.clab.yml")