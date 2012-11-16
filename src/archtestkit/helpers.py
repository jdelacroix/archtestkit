#!/usr/bin/env python

# Copyright (C) 2012 Jean-Pierre de la Croix
# see the LICENSE file included with this software

import subprocess
import sys

def make_sys_call(command, flags='', args=[]):
    s = [command]
    s.extend(flags.split())
    s.extend(args)
    print('executing: %s'%s)
    p = subprocess.Popen(s, stdout=subprocess.PIPE)
    return p.communicate()[0].decode(sys.stdout.encoding)