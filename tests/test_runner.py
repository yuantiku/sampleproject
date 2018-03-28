#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

logging.getLogger('urllib3').setLevel(logging.INFO)
logging.getLogger('oss2').setLevel(logging.INFO)
logging.getLogger('ybckit.gui').setLevel(logging.INFO)
logging.getLogger('matplotlib').setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.info("inited")
logger.debug('今天天气不错啊挺风和日丽的')
print('hello world!')
