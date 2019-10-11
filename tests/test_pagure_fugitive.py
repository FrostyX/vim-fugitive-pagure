import os
import sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.realpath('__file__')),
    "plugin"))


import unittest
from fugitive_pagure import pagure_url, remote2http


class TestFugitivePagure(unittest.TestCase):

    def test_remote2http(self):
        assert remote2http("ssh://git@pagure.io/copr/copr.git") \
                        == "https://pagure.io/copr/copr"

        assert remote2http("https://pagure.io/copr/copr.git") \
                        == "https://pagure.io/copr/copr"

    def test_pagure_url(self):
        opts = {
            "path": "frontend/coprs_frontend/manage.py",
            "remote": "ssh://git@pagure.io/copr/copr.git",
            "type": "blob",
            "commit": "master",
        }

        expected = "https://pagure.io/copr/copr/blob/master/f/frontend/coprs_frontend/manage.py"
        assert pagure_url(**opts) == expected

        opts["line1"] = 12
        expected = "https://pagure.io/copr/copr/blob/master/f/frontend/coprs_frontend/manage.py#_12"
        assert pagure_url(**opts) == expected

        opts["line2"] = 12
        expected = "https://pagure.io/copr/copr/blob/master/f/frontend/coprs_frontend/manage.py#_12"
        assert pagure_url(**opts) == expected

        opts["line2"] = 14
        expected = "https://pagure.io/copr/copr/blob/master/f/frontend/coprs_frontend/manage.py#_12-14"
        assert pagure_url(**opts) == expected

        opts["path"] = "README.md"
        expected = "https://pagure.io/copr/copr/blob/master/f/README.md?text=True#_12-14"
        assert pagure_url(**opts) == expected
