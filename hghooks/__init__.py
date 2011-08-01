#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This package contains Mercurial hooks. Add this package to your PYTHONPATH
# (f.e by adding "export PYTHONPATH=$PYTHONPATH:~/bin" to your ~/.profile
# - assuming ~/bin contains symlink to hghooks dir or the dir itself).
# To use some hooks just add them into ~/.hgrc like this:
#
# [hooks]
# pretxncommit.monkeycheck = python:{{PACKAGE}}.py.monkey.check
# pretxncommit.chimpcheck = python:{{PACKAGE}}.js.chimp.check

# You can disable hook(s) by using --config option:
# hg commit -m 'meh' --config "hooks.pretxncommit.monkeycheck="

import re

def grep_changed_files(repo,node,ext,checks):
    errors = {}
    files = []

    ctx = repo['tip']
    to_check = lambda f: f.endswith('.%s'%ext) and f in ctx #if file is not in ctx, it's being removed

    for change_id in xrange(repo[node].rev(), len(repo)):
        files += [f for f in repo[change_id].files() if to_check(f)]

    for file in set(files):
        """ Maybe this might be quite slow, but I was unable to
            think about other way to track lines too without using grep """
        for i, line in enumerate(ctx[file].data().splitlines()):
            for check, regexp in checks:
                if re.match(regexp,line):
                    if file not in errors:
                        errors[file] = []
                    errors[file].append((i+1,check,line))

    return errors

class Output(object):

    #bash colours
    OK = '\e[0;32m'
    ERR = '\033[91m'
    BOLD = '\033[1m'
    HL = '\033[37m'
    HLBOLD = '%s%s'%(HL,BOLD)
    RESET = '\033[0;0m'

    output = []

    def append(self,text,type='',prepend='\n'):
        text = '%s%s%s%s'%(prepend,getattr(self,type,''),text,self.RESET)
        self.output.append(text)

    def lines(self,glue='\n',prepend='',append='\n'):
        return '%s%s%s%s'%(prepend,glue.join(self.output),append,self.RESET)