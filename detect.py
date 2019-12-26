#!/usr/bin/python

import os
import sys
#print os.isatty(0)


print(sys.stdin.isatty(), os.environ.get("TERM", None))

