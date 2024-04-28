import logging
from io import StringIO
import pytest
from secured.log_manager import setup_default_logger

def test_setup_default_logger():
    """Test that the logger is set up correctly with a single handler and the right format."""
    logger = setup_default_logger()
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)
    assert isinstance(logger.handlers[0].formatter, logging.Formatter)
    assert logger.handlers[0].formatter._fmt == '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Check that no additional handlers are added on subsequent calls
    logger_second_call = setup_default_logger() # noqa: F841
    assert len(logger.handlers) == 1  # Still only one handler after the second setup

def test_logger_output():
    """Test the logger outputs the correct format."""
    logger = setup_default_logger()
    stream = StringIO()
    logger.handlers[0].stream = stream  # Redirect stream to capture output

    test_message = "This is an info message"
    logger.info(test_message)

    stream_value = stream.getvalue()
    assert test_message in stream_value
    assert "INFO" in stream_value

@pytest.fixture(autouse=True)
def clean_up_logger():
    """Fixture to clean up after each test case."""
    yield
    logger = logging.getLogger(__name__)
    logger.handlers.clear()
    logger.setLevel(logging.NOTSET)
