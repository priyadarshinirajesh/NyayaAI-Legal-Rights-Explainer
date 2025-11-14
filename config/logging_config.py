from loguru import logger
from config.settings import settings

def setup_logging():
    logger.add(
        settings.LOG_DIR / "nyayaai_{time}.log",
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        rotation="100 MB",
        retention="1 week",
        compression="zip"
    )
    return logger

log = setup_logging()