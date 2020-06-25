#!/usr/bin/env python3

from os import getenv
from math import pi


digits = int(getenv("DIGITS") or 10)
print("%.*f" % (digits, pi))