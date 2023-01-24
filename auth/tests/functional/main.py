import pytest
import logging


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    plugins = ("pytest_asyncio", "plugins.common", "utils.helpers.request_methods")

    pytest.main(["-x", "src"], plugins=plugins)
