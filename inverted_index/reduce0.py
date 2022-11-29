#!/usr/bin/env python3
"""Reduce 0: Count the total number of documents in the database."""

import sys


doc_count = 0
for line in sys.stdin:
    doc_count += int(line.partition('\t')[2])

print(doc_count)
