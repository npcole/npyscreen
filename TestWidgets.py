#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import npyscreen

import inspect
import npyscreen
from npyscreen.widget import Widget

def main(*args):
    members = inspect.getmembers(npyscreen)
    for m in members:
        name, cl = m
        if isinstance(m, npyscreen.Form):
            print "True"
        


if __name__ == '__main__':
    main()
    #npyscreen.wrapper(main)

