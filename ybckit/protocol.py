# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json
import logging
import time

from .config import YBC_CONFIG

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
    req_file = _open(request_file, 'w')

    file_content = '%d\n%s\n%s\nEOF\n' % (request_id, method, encoded_args)
    logger.debug('write request_content to file %s, content: %s' % (request_file, file_content))
    req_file.write(file_content)
    req_file.close()

    return request_id


def _read_file(fd):
    try:
        content = fd.read()
    except IOError:
        return None
    finally:
        fd.close()

    try:
        return content.decode('utf-8')
    except UnicodeDecodeError:
        return None
    except AttributeError:
        # Py3
        return content


def get_raw_response(request_id):
    """
    判断是否有响应返回
    :param request_id:
    :return:
    """
    response_file = _get_response_file(request_id)
    logger.debug('check response file %s' % response_file)

    try:
        response_file_fd = _open(response_file, 'r')
    except IOError:
        return False

    content = _read_file(response_file_fd)

    logger.debug('got response content: %s' % content)

    if content is None or (not content.endswith('\nEOF\n')):
        logger.debug('response is not finished')
        return False

    _cleanup_request_file(request_id)

    return content


def parse_response(raw_response):
    response = raw_response[:-5]
    return json.JSONDecoder().decode(response)


def _get_request_file():
    """
    返回请求对应的文件名，请求会写这个文件
    :return:
    """
    return YBC_CONFIG.request_file


def _generate_request_id():
    """
    生成一个请求 id，暂时用 (时间戳 % 60 分钟)
    :return:
    """
    return int(time.time() * 1000 % (60 * 60 * 1000))


def _get_response_file(request_id):
    """
    返回请求响应所在的文件，文件内容应该是 json 编码的请求响应
    :param request_id:
    :return:
    """
    prefix = YBC_CONFIG.response_file_prefix

    return "%s%d" % (prefix, request_id)


def _open(filename, mode):
    # TODO: buffer before write because of ossfs limitation
    return open(filename, mode)


def _cleanup_request_file(request_id):
    """
    请求完成，做一些微小的清理工作
    :param request_id:
    :return:
    """

    request_file = _get_request_file()

    logger.debug('cleanup request file %d, file=%s' % (request_id, request_file))

    try:
        request_fd = _open(request_file, 'r')
        content = _read_file(request_fd)
        request_fd.close()

        if content is not None and content.startswith('%d\n' % request_id):
            os.remove(request_file)
    except IOError:
        pass
