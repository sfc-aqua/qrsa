import sys
import pytest


@pytest.fixture(scope="session")
def setup_module_path():
    """
    rye run cannot solve the path under src/app since they don't have
    named parent module and it is not allow to use relative import.
    So we need to add the path to sys.path to make it work
    when we run the test under tests directory.
    """
    sys.path.append("../src/app")
