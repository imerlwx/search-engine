#!/usr/bin/env python3
"""Map 3: Produce 3 files, one for each segment."""

import sys
import json

# Set doc_id % 3 as the mapper output key
for line in sys.stdin:
    word_info = line.strip().split('\t')
    json_str = json.loads(word_info[1])
    key = int(word_info[0]) % 3

    word_json = json.dumps(json_str, separators=(',', ':'))
    print(f"{key}\t{word_json}")
