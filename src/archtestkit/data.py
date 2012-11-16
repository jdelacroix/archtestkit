#!/usr/bin/env python

# Copyright (C) 2012 Jean-Pierre de la Croix
# see the LICENSE file included with this software

import re

class Package:

    def __init__(self, atom):
        self.category, self.name, self.version = re.split('^=(.*)/(.*)-(\d.*$)', atom)[1:-1]
        self.atom = atom