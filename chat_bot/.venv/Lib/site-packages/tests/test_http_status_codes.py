from httpz import HTTPStatusCodes
from httpz.http_status_code import HTTPStatusCode
from httpz.status_codes import status_codes

import unittest


class TestHTTPStatusCodes(unittest.TestCase):

    def test_factory_code(self):

        c = "100"
        code = HTTPStatusCodes.get(c)
        self.assertEqual(code.code, 100)

    def test_factory_message(self):

        c = "100"
        code = HTTPStatusCodes.get(c)
        self.assertEqual(code.message, "Continue")

    def test_factory_description(self):

        c = "100"
        code = HTTPStatusCodes.get(c)
        self.assertEqual(code.description, "This interim response indicates that everything so far is OK and that the "
                                           "client should continue the request, or ignore the response if the request "
                                           "is already finished")

    def test_factory_category(self):
        c = "100"
        code = HTTPStatusCodes.get(c)
        self.assertEqual(code.category, "informational")

    def test_factory_webdav(self):

        c = "100"
        code = HTTPStatusCodes.get(c)
        self.assertEqual(code.webdav, False)

    def test_factory_to_dict(self):

        c = "100"
        code = HTTPStatusCodes.get(c)
        self.assertIsInstance(code.to_dict(), dict)

    def test_factory_with_int_code(self):

        c = 100
        code = HTTPStatusCodes.get(c)
        self.assertEqual(code.code, 100)

    def test_factory_raises_keyerror(self):

        c = -1
        with self.assertRaises(KeyError):
            code = HTTPStatusCodes.get(c)

    def test_factory_get_category_success(self):

        c = "informational"
        objs = HTTPStatusCodes.get_category(c)
        self.assertEqual(len(objs), 4)

    def test_factory_get_category_fails(self):

        c = "foo"
        with self.assertRaises(KeyError):
            objs = HTTPStatusCodes.get_category(c)

    def test_all_status_code_keys_match_their_values(self):

        for k, v in status_codes.items():
            self.assertEqual(k, str(v["code"]))

    def test_create_all_instances(self):

        for k, v in status_codes.items():
            HTTPStatusCode(**v)

    def test_get_all(self):

        all_status_codes = HTTPStatusCodes.get_all()
        self.assertEqual(len(all_status_codes), 63)
