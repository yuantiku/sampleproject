# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import sys
import ast

from .config import YBC_CONFIG
from .log import init as logging_init

logger = logging.getLogger(__name__)


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def init_if_needed(source_file):
    all_imports = set()

    with open(source_file) as f:
        ast_tree = ast.parse(f.read())

    for statement in ast_tree.body:
        if isinstance(statement, ast.Import):
            for _import in statement.names:
                all_imports.update(_import.name.split('.'))

    if 'matplotlib' in all_imports:
        from .mpl import init as mpl_init
        logger.debug('import mpl')
        mpl_init()

    if 'easygui' in all_imports or 'ybc_box' in all_imports:
        from .gui import init as gui_init
        logger.debug('import gui')
        gui_init()

    if 'ybc_speech' in all_imports:
        from .media import init as media_init
        logger.debug('import media')
        media_init()


if __name__ == '__main__':
    logging_init()

    if not YBC_CONFIG.is_under_ybc_env:
        logger.error('只能在猿辅导环境下运行')
        sys.exit(1)

    sys.stdout = Unbuffered(sys.stdout)
    sys.stderr = Unbuffered(sys.stderr)

    if len(sys.argv) <= 1:
        logger.error('参数错误，需指定一个 script 来运行，例如 python -m ybckit.runner hello.py')
        sys.exit(1)

    script_file = sys.argv[1]
    init_if_needed(script_file)

    exec(open(script_file, 'rb').read())
