import logging
from logging import FileHandler
from typing import Any


def setup_logging() -> Any:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[FileHandler('log_file.log', mode='w', encoding='utf-8')]
                        )

    return logging.getLogger()
