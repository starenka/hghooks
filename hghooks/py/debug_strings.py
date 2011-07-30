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
    files = []

    CHECKS = {
        'assert False':re.compile(RE_ASSERT),
        'print':re.compile(RE_PRINT),
        'IPython shell embedding':re.compile(RE_IPYTHON),
    }

    ctx = repo['tip']
    to_check = lambda f: f.endswith('py') and f in ctx #if file is not in ctx, it's being removed

    for change_id in xrange(repo[node].rev(), len(repo)):
        files += [f for f in repo[change_id].files() if to_check(f)]

    for file in set(files):
        """ Maybe this might be quite slow, but I was unable to
            think about other way to track lines too without using grep """
        for i, line in enumerate(ctx[file].data().splitlines()):
            errors[file] = [(i+1, check, line) for check in CHECKS if re.match(CHECKS[check], line)]

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
        input = ui.promptchoice('Commit anyway? [y/n]',(('&Yes'),('&No')),default=1)
        return bool(input)
    return False