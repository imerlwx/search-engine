#!/usr/bin/env python3
"""Map 0: Count the total number of documents in the database."""

import sys


DOC_COUNT = 0
for doc in sys.stdin:
    DOC_COUNT += 1

print(f"docs\t{DOC_COUNT}")
