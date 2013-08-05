#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, unittest, sys

from hghooks.py.debug_strings import RE_ASSERT, RE_PRINT, RE_IPYTHON, RE_PPRINT

class DebugStrings(unittest.TestCase):
    def setUp(self):
        pass

    def test_regexps(self):
        map = {
            're_assert':[
                    (False,'#assert False'),
                    (False,'#  assert False'),
                    (False,'   #assert False  '),
                    (False,'#assert False  '),
                    (False,'ur mama is so fat #assert False  '),
                    (False,'nassert False  '),
                    (False,'assertFalse  '),
                    (True,'assert False'),
                    (True,'     assert False'),
                    (True,'     assert False    '),
            ],
            're_print':[
                    (False,'#print 1'),
                    (False,'#  print 2'),
                    (False,'   #print cucumber  '),
                    (False,'#print bill  '),
                    (False,'ur mama is so fat you can #print her on billboards  '),
                    (False,'prettyprint  '),
                    (True,'print'),
                    (True,'     print money'),
                    (True,'     print    '),
            ],
            're_pprint':[
                    (False,'#pprint.print("fap")'),
                    (False,'#  print 2'),
                    (False,'   #pprint(obj)'),
                    (False,'#import pprint;pprint.pprint(bill)  '),
                    (False,'ur mama is so fat you can #pprint her on billboards  '),
                    (False,'prettypprint  '),
                    (True,'pprint('),
                    (True,'pprint.pprint(one)'),
                    (True,'import pprint; pprint.pprint(one)'),
                    (True,'     pprint(money'),
                    (True,'     pprint.pprint()    '),
            ],
            're_ipython':[
                    (False,'#IPShellEmbed()()'),
                    (False,'#  IPShellEmbed()()'),
                    (False,'   #IPShellEmbed()()  '),
                    (False,'#IPShellEmbed()()  '),
                    (False,'ur mama is so fat #IPShellEmbed()()  '),
                    (False,'nIPShellEmbed()()  '),
                    (False,'IPShellEmbed()  '),
                    (True,'IPShellEmbed()()'),
                    (True,'     IPShellEmbed()()'),
                    (True,'     IPShellEmbed()()    '),
            ],
        }

        for regexp,tests in map.items():
            rc = getattr(sys.modules[__name__],regexp.upper())[1]
            for t in tests:
                #print rc, t[0], t[1]
                self.assertEqual(t[0],bool(re.match(rc,t[1])), t)

if __name__ == '__main__':
    unittest.main()