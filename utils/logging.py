from rich.console import Console
from rich.logging import RichHandler
import logging
from ..config import LOG_LEVEL

_console = Console()


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(console=_console, rich_tracebacks=True)],
    )
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    return logger
