# engine/core/logger.py
import logging

logger = logging.getLogger("cubenet_cms")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

# Console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
