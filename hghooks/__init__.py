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

class Output(object):

    #bash colours
    OK = '\e[0;32m'
    ERR = '\033[91m'
    BOLD = '\033[1m'
    HL = '\033[37m'
    HLBOLD = '%s%s'%(HL,BOLD)
    RESET = '\033[0;0m'

    output = []

    def append(self,text,type,prepend='\n'):
        text = '%s%s%s%s'%(prepend,getattr(self,type,''),text,self.RESET)
        self.output.append(text)

    def lines(self,glue='\n',prepend='',append='\n'):
        return '%s%s%s%s'%(prepend,glue.join(self.output),append,self.RESET)