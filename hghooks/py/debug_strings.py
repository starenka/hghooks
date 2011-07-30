#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This is a Mercurial hook, place this package in PYTHONPATH
# and place it in ~/.hgrc like this:
# [hooks]
# pretxncommit.pydebugstrings = python:hghooks.py.debug_strings.check
#
# This hooks try to look for common debugging stuff in your code

import re
from hghooks import Output, grep_changed_files

RE_ASSERT = r'^((?!#)\s)*assert False.*'
RE_PRINT = r'^((?!#)\s)*print.*'
RE_IPYTHON = r'^((?!#)\s)*IPShellEmbed\(\)\(\).*'

def check(ui, repo, hooktype, node, **kwargs):
    checks = {
        'assert False':re.compile(RE_ASSERT),
        'print':re.compile(RE_PRINT),
        'IPython shell embedding':re.compile(RE_IPYTHON),
    }

    errors = grep_changed_files(repo,node,ext='py',checks=checks)

    if errors:
        out = Output()
        out.append("You maybe didn't want to commit this, did you?..",'ERR')
        for file,errs in errors.items():
            out.append('file:\t%s\n%s'%(file,'-'*(len(file)+8)),'HLBOLD')
            for line,check,string in errs:
                out.append('%s\t%s%s (%s)'%(str(line).rjust(4),string,out.RESET,check),'HL',prepend='')
        out.append('\n(You can disable this hook w/ --config: hg commit --config "hooks.%s.pydebugstrings=")\n'%hooktype)

        ui.warn(out.lines())
        input = ui.promptchoice('Commit anyway? [y/n]',(('&Yes'),('&No')),default=1)
        return bool(input)
    return False