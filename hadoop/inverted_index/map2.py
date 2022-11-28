#!/usr/bin/env python3
"""Map 2: Calculate tf, idf and normalize factor for each term in each doc."""

import sys
import math
import json


# Get the number of documents
with open('total_document_count.txt', encoding='utf-8') as text_file:
    for line in text_file:
        num_doc = float(line)

for line in sys.stdin:
    word_detail = line.strip().split('\t')
    word = word_detail[0]
    word_json = json.loads(word_detail[1])

    nk = len(word_json) # number of documents that contain the word tk
    idf = math.log(num_doc / nk, 10) # idf of term tk

    for doc_id, tf in word_json.items():
        norm = (float(tf) * idf) ** 2 # norm for one term of one doc
        info = json.dumps({
            "word": word,
            "doc_id": doc_id,
            "tf": tf,
            "idf": idf,
            "norm": norm
        }, separators=(",", ":"))
        print(f"{doc_id}\t{info}")
