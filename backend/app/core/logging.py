from __future__ import annotations

import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        level = record.levelname
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


def configure_logging() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        enqueue=True,
        backtrace=False,
        diagnose=False,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)

    for noisy in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logging.getLogger(noisy).handlers = [InterceptHandler()]
        logging.getLogger(noisy).propagate = False
