#!/usr/bin/env python3
"""Reduce 0: Count the total number of documents in the database."""

import sys


DOC_COUNT = 0
for line in sys.stdin:
    DOC_COUNT += int(line.partition('\t')[2])

print(DOC_COUNT)
