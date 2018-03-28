# coding=utf-8
import logging
import os
import sys

from .config import YBC_CONFIG
from .gui import init as gui_init
from .mpl import init as mpl_init
from .oss import init as oss_init

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

if __name__ == '__main__':
    if 'YBC_DEBUG' in os.environ:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    logging.basicConfig(level=logging_level)
    if not YBC_CONFIG.is_under_ybc_env:
        logger.error('只能在猿辅导环境下运行')
        sys.exit(1)

    oss_init()
    mpl_init()
    gui_init()

    if len(sys.argv) <= 1:
        logger.error('参数错误，需指定一个 script 来运行，例如 python -m ybckit.runner hello.py')
        sys.exit(1)

    script_file = sys.argv[1]
    exec(open(script_file).read())
