# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import sys

from .config import YBC_CONFIG
from .gui import init as gui_init
from .log import init as logging_init
from .media import init as media_init
from .mpl import init as mpl_init

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging_init()

    if not YBC_CONFIG.is_under_ybc_env:
        logger.error('只能在猿辅导环境下运行')
        sys.exit(1)

    mpl_init()
    gui_init()
    media_init()

    if len(sys.argv) <= 1:
        logger.error('参数错误，需指定一个 script 来运行，例如 python -m ybckit.runner hello.py')
        sys.exit(1)

    script_file = sys.argv[1]
    exec(open(script_file, 'rb').read())
