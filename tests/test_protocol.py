import logging
import sys
import unittest

import ybckit.protocol as protocol
from . import ybc_env

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))


class ProtocolTestCase(unittest.TestCase):

    def setUp(self):
        super(ProtocolTestCase, self).setUp()
        ybc_env.setup()

    def tearDown(self):
        super(ProtocolTestCase, self).tearDown()
        ybc_env.cleanup()

    def test_get_response_file(self):
        self.assertEqual("/tmp/response_123", protocol._get_response_file(123))

    def test_send_request(self):
        request_id = protocol.send_request("foo", [1, 2, 3])
        logger.info("request_id is %d", request_id)
        self.assertGreater(request_id, 0)

        request_file = protocol._get_request_file()
        f = open(request_file, 'r')
        content = f.read()
        self.assertEqual("%d\nfoo\n[1, 2, 3]\nEOF\n" % request_id, content)

        f.close()

    def test_get_raw_response(self):
        response_content = "[1,2,3]\nEOF"
        f = open(protocol._get_response_file(123), 'w')
        f.write(response_content)
        f.close()

        self.assertFalse(protocol.get_raw_response(123))

        response_content = "[1,2,3]\nEOF\n"
        f = open(protocol._get_response_file(123), 'w')
        f.write(response_content)
        f.close()

        raw_response = protocol.get_raw_response(123)
        self.assertTrue(raw_response is not False)
        self.assertEqual(response_content, raw_response)

    def test_parse_response(self):
        response_content = "[1,2,3]\nEOF\n"
        f = open(protocol._get_response_file(123), 'w')
        f.write(response_content)
        f.close()

        raw_response = protocol.get_raw_response(123)
        response = protocol.parse_response(raw_response)
        self.assertEqual([1, 2, 3], response)


if __name__ == '__main__':
    unittest.main()
