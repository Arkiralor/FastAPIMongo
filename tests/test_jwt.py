from unittest import TestCase
from tests import client

import pytest

from auth.jwt import create_access_token, create_refresh_token

def test_both_tokens_are_different():
    data = {
        "sub": "testemail@gmail.com"
    }

    access = create_access_token(data=data)
    refresh = create_refresh_token(data=data)

    assert(access != refresh)

class TestJwtTokens(TestCase):

    def setup(self):
        self.data = {
            "sub": "test.email@gmail.com"
        }

    def check_both_tokens_are_different(self):
        access = create_access_token(data=self.data)
        refresh = create_refresh_token(data=self.data)

        self.assertNotEqual(access, refresh, msg="Access token and refresh token are exactly same.")

