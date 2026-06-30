import logging
import sys


def configure_logging() -> None:
    """
    Call this ONCE at application startup in main.py.
    After that, every module just does:
        logger = logging.getLogger(__name__)
    """
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    # Silence noisy third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("aiokafka").setLevel(logging.WARNING)