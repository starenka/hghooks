#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This is a Mercurial hook, place this package in PYTHONPATH
# and place it in ~/.hgrc like this:
# [hooks]
# pretxncommit.monkeycheck = python:hghooks.py.debug_strings.check
#
# This hooks try to look for common debugging stuff in your code

import re
from hghooks import Output

RE_ASSERT = r'^((?!#)\s)*assert False.*'
RE_PRINT = r'^((?!#)\s)*print.*'
RE_IPYTHON = r'^((?!#)\s)*IPShellEmbed\(\)\(\).*'

def check(ui, repo, hooktype, node, **kwargs):
    errors = {}
    files = set()

    CHECKS = {
        'assert False':re.compile(RE_ASSERT),
        'print':re.compile(RE_PRINT),
        'IPython shell embedding':re.compile(RE_IPYTHON),
    }
    
    for change_id in xrange(repo[node].rev(), len(repo)):
        files = [f for f in repo[change_id].files() if f.endswith('.py')]

    ctx = repo['tip']
    for file in files:
        if file not in ctx: #file is being removed
            continue
        """ Maybe this might be quite slow, but I was unable to
            think about other way to track lines too without using grep """
        for i, line in enumerate(ctx[file].data().splitlines()):
            for check, regexp in CHECKS.items():
                if re.match(regexp,line):
                    if file not in errors:
                        errors[file] = []
                    errors[file].append((i+1,check,line))

    if errors:
        out = Output()
        out.append('OH NOES! Monkey code check failed..','ERR')
        for file,errs in errors.items():
            out.append('file:\t%s\n%s'%(file,'-'*(len(file)+8)),'HLBOLD')
            for line,check,string in errs:
                out.append('%s\t%s%s (%s)'%(str(line).rjust(4),string,out.RESET,check),'HL',prepend='')
        out.append('If you think this a false-positive feel free to disable hook by using --config:\
            \nhg commit --config "hooks.pretxncommit.monkeycheck="\n','BOLD')

        ui.warn(out.lines())
        return True
    return False