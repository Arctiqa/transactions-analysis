import logging
from typing import Any


def setup_logging() -> Any:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        encoding='utf-8'
                        )
    logging.FileHandler('src/log_file.log', mode='w')
    return logging.getLogger()
