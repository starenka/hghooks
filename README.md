hghooks
=======

This package contains Mercurial hooks. Add this package to your PYTHONPATH
(f.e by adding "export PYTHONPATH=$PYTHONPATH:~/bin" to your ~/.profile
- assuming ~/bin contains symlink to hghooks dir or the dir itself).
To use some hooks just add them into ~/.hgrc like this:

    [hooks]
    pretxncommit.monkeycheck = python:{{PACKAGE}}.py.monkey.check
    pretxncommit.chimpcheck = python:{{PACKAGE}}.js.chimp.check

You can disable hook(s) by using --config option:

    hg commit -m 'meh' --config "hooks.pretxncommit.monkeycheck="
