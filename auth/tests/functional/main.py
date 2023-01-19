import pytest
import logging


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    plugins = ("pytest_asyncio", "plugins.common")

    pytest.main(["-x", "src"], plugins=plugins)
