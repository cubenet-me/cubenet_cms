import logging

logger = logging.getLogger("cubenet_cms")
logger.setLevel(logging.INFO)  # уровень логирования

# Добавляем обработчик только если его ещё нет
if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
