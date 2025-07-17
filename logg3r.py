import logging
from loadconfig import Config

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

CONF = Config()

LEVELS = {
    '0': logging.INFO,
    '1': logging.DEBUG
}


def setup_logging():
    level = LEVELS.get(str(CONF.LOG_LEVEL), logging.INFO)
    logging.basicConfig(
        format=FORMAT,
        filemode='a',
        level=level,
        filename=CONF.LOG_FILE
    )
    return logging.getLogger(__name__)
