import logging

def setup_default_logger() -> logging.Logger:
    """
    Sets up and returns a logger with a basic configuration.

    This function configures a logger to output log messages to the console (standard output).
    It sets the logger's level to INFO, meaning it will handle INFO and higher level messages (WARNING, ERROR, CRITICAL).
    The log output format includes the time of the log entry, the logger's name, the log level, and the log message.

    If a logger with handlers is already set up for the module, this function does not add another handler.

    Returns:
        logging.Logger: A logger instance configured with a console handler.

    Example:
        >>> logger = setup_default_logger()
        >>> logger.info("This is an info message")
        2023-01-01 12:00:00 - __main__ - INFO - This is an info message
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger
