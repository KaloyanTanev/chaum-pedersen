#!/usr/bin/env python3
from mock import patch
import os
import sys
from types import SimpleNamespace
import unittest

import redis

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../app/victor'))
import app.victor.victor as victor

class TestVictor(unittest.TestCase):
    def test_register(self):
      with patch.object(redis.Redis, 'ping') as mock_ping, \
         patch.object(redis.Redis, 'set') as mock_set:
        mock_ping.return_value = 'Ok'
        mock_set.return_value = 'Ok'

        v = victor.Victor()
        req = SimpleNamespace()
        req.y1 = '12345'
        req.y2 = '123'
        req.p = '154683845298676959165403987926494281316419213683155127126817194698027978801438005190241250823446325439003259530375969765117483828690646341746414524298615790009821094550955591801806921713955454074006630596186820463607213250252130128475530327379090837533262737950332604229832047368875411797266956070428074589687'

        res = v.Register(req, None)
        self.assertEqual(res.id, "23b095de4a7e81966b87e185e8b450c9998b49bdd26b8d2d3dd6acf415117ae4")

    def test_login_round_one(self):
      with patch.object(redis.Redis, 'ping') as mock_ping, \
         patch.object(redis.Redis, 'get') as mock_get, \
         patch.object(redis.Redis, 'set') as mock_set:
        mock_ping.return_value = 'Ok'
        mock_set.return_value = 'Ok'
        def side_effect_func(*args, **kwargs):
            if "comm" in args[0]:
              return None
            else:
              return 'Ok'
        mock_get.side_effect = side_effect_func

        v = victor.Victor()
        req = SimpleNamespace()
        req.r1 = '12345'
        req.r2 = '123'
        req.id = '0x123'

        res = v.LoginRoundOne(req, None)
        self.assertIsInstance(int(res.c), int)

    def test_login_round_two(self):
      with patch.object(redis.Redis, 'ping') as mock_ping, \
         patch.object(redis.Redis, 'get') as mock_get, \
         patch.object(redis.Redis, 'set') as mock_set, \
         patch.object(redis.Redis, 'delete') as mock_delete:
        mock_ping.return_value = 'Ok'
        mock_set.return_value = 'Ok'
        def side_effect_func(*args, **kwargs):
            if "comm" in args[0]:
              return b'10 256 6561'
            else:
              return b'1180591620717411303424 2503155504993241601315571986085849 154683845298676959165403987926494281316419213683155127126817194698027978801438005190241250823446325439003259530375969765117483828690646341746414524298615790009821094550955591801806921713955454074006630596186820463607213250252130128475530327379090837533262737950332604229832047368875411797266956070428074589687'
        mock_get.side_effect = side_effect_func
        mock_delete.return_value = 'Ok'

        v = victor.Victor()
        req = SimpleNamespace()
        req.id = '0x123'
        req.s = '77341922649338479582701993963247140658209606841577563563408597349013989400719002595120625411723162719501629765187984882558741914345323170873207262149307895004910547275477795900903460856977727037003315298093410231803606625126065064237765163689545418766631368975166302114916023684437705898633478035214037294497'

        res = v.LoginRoundTwo(req, None)
        self.assertTrue(res.b)

    def test_login_round_fail(self):
      with patch.object(redis.Redis, 'ping') as mock_ping, \
         patch.object(redis.Redis, 'get') as mock_get, \
         patch.object(redis.Redis, 'set') as mock_set, \
         patch.object(redis.Redis, 'delete') as mock_delete:
        mock_ping.return_value = 'Ok'
        mock_set.return_value = 'Ok'
        def side_effect_func(*args, **kwargs):
            if "comm" in args[0]:
              return b'10 1 6561' # INCORRECT r1
            else:
              return b'1180591620717411303424 2503155504993241601315571986085849 154683845298676959165403987926494281316419213683155127126817194698027978801438005190241250823446325439003259530375969765117483828690646341746414524298615790009821094550955591801806921713955454074006630596186820463607213250252130128475530327379090837533262737950332604229832047368875411797266956070428074589687'
        mock_get.side_effect = side_effect_func
        mock_delete.return_value = 'Ok'

        v = victor.Victor()
        req = SimpleNamespace()
        req.id = '0x123'
        req.s = '77341922649338479582701993963247140658209606841577563563408597349013989400719002595120625411723162719501629765187984882558741914345323170873207262149307895004910547275477795900903460856977727037003315298093410231803606625126065064237765163689545418766631368975166302114916023684437705898633478035214037294497'

        res = v.LoginRoundTwo(req, None)
        self.assertFalse(res.b)

if __name__ == "__main__":
    unittest.main()
