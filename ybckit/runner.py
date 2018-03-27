# coding=utf-8
import logging
import sys
from logging.config import dictConfig

from .gui import init as gui_init
from .mpl import init as mpl_init
from .protocol import is_under_ybc_env

logging_config = dict(
    version=1,
    formatters={
        'f': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.INFO}
    },
    root={
        'handlers': ['h'],
        'level': logging.INFO,
    },
)

dictConfig(logging_config)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    if not is_under_ybc_env():
        logger.error('只能在猿辅导环境下运行')
        sys.exit(1)

    mpl_init()
    gui_init()

    if len(sys.argv) <= 1:
        logger.error('参数错误，需指定一个 script 来运行，例如 python -m ybckit.runner hello.py')
        sys.exit(1)

    script_file = sys.argv[1]
    execfile(script_file)
