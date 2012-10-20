#!/usr/bin/env python

# Copyright (C) 2012  Jean-Pierre de la Croix
# see the LICENSE file included with this software

import subprocess
import sys

def make_call(command, flags, args):
    s = [command]
    s.extend(flags.split())
    s.extend(args)
    p = subprocess.Popen(s, stdout=subprocess.PIPE)
    return p.communicate()[0].decode(sys.stdout.encoding)

def rdepscan(package):
    
    # qlist -Ce package
    # returns list of files installed by package
    command = 'qlist'
    flags = '-Ce'
    args = [package]
    output = make_call(command, flags, args)
    
    # scanelf -L -n -q -F%n#F output
    # returns list of libraries that ELF files of package depend on 
    command = 'scanelf'
    flags = '-L -n -q -F%n#F'
    args = output.split()
    output = make_call(command, flags, args)
    
    # qfile -Cv output
    # returns list of packages that provide the library dependencies
    command = 'qfile'
    flags = '-Cv'
    args = output.replace('\n', ',').split(',')
    output = make_call(command, flags, args)
    
    # remove duplicates and return
    pkgs = output.replace('\n', ':').split(':')
    pkgs = filter(None, pkgs)
    
    uniq = set()
    for pkg in pkgs:
        uniq.add(pkg.partition(' ')[0])
        
    return list(uniq)        

if __name__ == '__main__':
    pkg = sys.argv[1]
    print('List of dependencies for packages %s'%pkg);
    pkgs = rdepscan(pkg)
    for pkg in pkgs:
        print(pkg)