#!/usr/bin/env python

# Copyright (C) 2012 Jean-Pierre de la Croix
# see the LICENSE file included with this software

import sys, os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from archtestkit.helpers import make_sys_call
from archtestkit.data import Package

import re

def repoman(package):
    current_dir = os.getcwd()
    print(current_dir)
    
    os.chdir(os.path.join('/usr/portage/', package.category, package.name))
    print(os.getcwd())
    
    ebuild = os.path.realpath(package.name + '-' + package.version + '.ebuild')
    print(ebuild)
    
    with open(ebuild, 'r') as file:
        lines = file.readlines()
        
    with open(ebuild, 'w') as file:
        for line in lines:
            if 'KEYWORDS=' in line:
                line = re.sub(r'~amd64', 'amd64', line)
            file.write(line)
    
#    count = 1
#    for line in open(ebuild):
#        if 'KEYWORDS=' in line:
#            break
#        count += 1
#    
#    command = 'sed'
#    flags = '-ie'
#    args = ['%ds/~amd64/amd64/g'%count, ebuild]
#    output = make_sys_call(command, flags, args)
#    print(output)
    
    output = make_sys_call('repoman', args=['manifest'])
    print(output)
    
    output = make_sys_call('repoman', args=['full']);
    print(output)
    
    s = output.split('\n')[-2]

    qa_ok = ("If everyone were like you, I'd be out of business!" in s)

    with open(ebuild, 'w') as file:
        for line in lines:
            file.write(line)
    
#    command = 'sed'
#    flags = '-ie'
#    args = ['%ds/amd64/~amd64/g'%count, ebuild]
#    output = make_sys_call(command, flags, args)
#    print(output)
    
    output = make_sys_call('repoman', args=['manifest'])
    print(output)
        
    os.chdir(current_dir)
    print(os.getcwd())    

    return qa_ok


if __name__ == '__main__':
    pkg = Package(sys.argv[1]) # for now assume, =category/package-version
    if repoman(pkg):
    	print('repoman checked out ok')
    else:
    	print('repoman detected QA problems, so check above output')
