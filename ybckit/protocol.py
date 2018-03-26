# coding=utf-8
import json
import os
import time

from pathlib import Path


def send_request(method, args, kwargs):
    """
    发送一个请求，把请求的方法和参数写到 request 文件中
    :param args:
    :param kwargs:
    :param method:
    :return:
    """
    id = _generate_request_id()
    encoded_args = json.JSONEncoder().encode({"args": args, "kwargs": kwargs})
    req_file = open(_get_request_file(), 'w')

    file_content = "%d\n%s\n%s\nEOF\n" % (id, method, encoded_args)
    req_file.write(file_content)
    req_file.close()

    return id


def get_raw_response(request_id):
    """
    判断是否有响应返回
    :param request_id:
    :return:
    """
    response_file = _get_response_file(request_id)
    if not Path(response_file).exists():
        return False

    f = open(response_file, 'r')
    content = f.read()
    f.close()

    if not content.endswith("\nEOF\n"):
        return False

    return content


def _get_request_file():
    """
    返回请求对应的文件名，请求会写这个文件
    :return:
    """
    return os.environ['YBC_REQUEST_FILE']


def _generate_request_id():
    """
    生成一个请求 id，暂时用 (时间戳 % 10 分钟)
    :return:
    """
    return time.time() * 1000 % (10 * 60 * 1000)


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
