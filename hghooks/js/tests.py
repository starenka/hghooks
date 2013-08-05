#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, unittest2, sys

from hghooks.js.debug_strings import RE_ALERT, RE_CONSOLE_LOG

class DebugStrings(unittest2.TestCase):
    def setUp(self):
        pass

    def test_regexps(self):
        map = {
            're_alert':[
                (False,'//alert("Spam")'),
                (False,'//  alert("Hullo")'),
                (False,'   //alert("Hullo")  '),
                (False,'//alert("Hullo")  '),
                (False,'this is supposed to be false //alert("Hullo")  '),
                (False,' nalert("Hullo")  '),
                (False,'alertology  '),
                (True,'alert("Hullo")'),
                (True,'     /alert("Hullo")'),
                (True,'     alert("Hullo")    '),
                (True,'   alert("Hullo")'),
            ],
            're_console_log':[
            ],
        }

        for regexp,tests in map.items():
            rc = re.compile(getattr(sys.modules[__name__],regexp.upper()))
            for t in tests:
                print rc, t[0], t[1]
                self.assertEqual(t[0],bool(re.match(rc,t[1])))

if __name__ == '__main__':
    unittest2.main()