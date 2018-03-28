# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
import os
import time

from pathlib import Path

logger = logging.getLogger(__name__)


def send_request(method, args, kwargs):
    """
    发送一个请求，把请求的方法和参数写到 request 文件中
    :param args:
    :param kwargs:
    :param method:
    :return:
    """

    logger.debug('send_request method=%s, args=%s, kwargs=%s' % (method, str(args), str(kwargs)))

    request_id = _generate_request_id()
    logger.debug('generated request request_id %d' % request_id)
    encoded_args = json.JSONEncoder().encode({"args": args, "kwargs": kwargs})
    logger.debug('encoded_args %s' % encoded_args)

    request_file = _get_request_file()
    req_file = open(request_file, 'w')

    file_content = '%d\n%s\n%s\nEOF\n' % (request_id, method, encoded_args)
    logger.debug('write request_content to file %s, content: %s' % (request_file, file_content))
    req_file.write(file_content)
    req_file.close()

    return request_id


def _cleanup_request_file(request_id):
    """
    请求完成，做一些微小的清理工作
    :param request_id:
    :return:
    """

    request_file = _get_request_file()

    logger.debug('cleanup request file %d, file=%s' % (request_id, request_file))

    try:
        request_fd = open(request_file, 'r')
        content = request_fd.read()
        request_fd.close()

        if content.startswith('%d\n' % request_id):
            os.remove(request_file)
    except IOError:
        pass


def get_raw_response(request_id):
    """
    判断是否有响应返回
    :param request_id:
    :return:
    """
    response_file = _get_response_file(request_id)

    logger.debug('check response file %s' % response_file)

    if not Path(response_file).exists():
        logger.debug('response file doesn\'t existed')
        return False

    f = open(response_file, 'r')
    content = f.read()
    f.close()

    logger.debug('got response content: %s' % content)

    if not content.endswith('\nEOF\n'):
        logger.debug('response is not finished')
        return False

    _cleanup_request_file(request_id)

    return content


def _get_request_file():
    """
    返回请求对应的文件名，请求会写这个文件
    :return:
    """
    return os.environ['YBC_REQUEST_FILE']


def _generate_request_id():
    """
    生成一个请求 id，暂时用 (时间戳 % 60 分钟)
    :return:
    """
    return time.time() * 1000 % (60 * 60 * 1000)


def _get_response_file(request_id):
    """
    返回请求响应所在的文件，文件内容应该是 json 编码的请求响应
    :param request_id:
    :return:
    """
    return "%s%d" % (os.environ['YBC_RESPONSE_FILE_PREFIX'], request_id)


def parse_response(raw_response):
    response = raw_response[:-5]
    return json.JSONDecoder().decode(response)
