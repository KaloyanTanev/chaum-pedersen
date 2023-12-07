#!/usr/bin/env python3
from mock import patch
import os
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../app/peggy'))
import app.peggy.peggy as peggy

class TestPeggy(unittest.TestCase):
    def test_register(self):
      resp = SimpleNamespace()
      resp.p = '13'
      resp.error = ""
      with patch('app.peggy.peggy.grpc_req_register', new=lambda y1, y2, p: resp):
        res = peggy.Register(123456789)
        self.assertIsInstance(res, int)

    def test_login(self):
      resp1 = SimpleNamespace()
      resp1.c = '12345'
      resp1.error = ""
      resp2 = SimpleNamespace()
      resp2.b = True
      resp2.error = ""
      with patch('app.peggy.peggy.grpc_req_login_r1', new=lambda id, r1, r2: resp1), \
          patch('app.peggy.peggy.grpc_req_login_r2', new=lambda id, s: resp2):
        res = peggy.Login(123456789, 37)
        self.assertTrue(res)

if __name__ == "__main__":
    unittest.main()
