import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='{"level":"%(levelname)s","message":"%(message)s"}',
    stream=sys.stdout,
)

logger = logging.getLogger("app")
