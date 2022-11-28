#!/usr/bin/env python3
"""Map 1: Parse each word into word /t {docid, 1} for each document."""

import sys
import re
import csv
import json


csv.field_size_limit(sys.maxsize)

STOP_WORDS = []
with open('./stopwords.txt', encoding='utf-8') as stop_words_file:
    for line in stop_words_file:
        STOP_WORDS.append(line.strip().casefold())

for doc in csv.reader(sys.stdin):
    if not doc:
        continue

    doc_id = doc[0]
    doc_title = doc[1]
    doc_text = doc[2]
    # Remove non-alphanumeric characters (that also aren’t spaces)
    # Combine both document title and document body by concatenating them
    doc_title_text = doc_title + " " + doc_text
    doc_title_text = re.sub(r"[^a-zA-Z0-9 ]+", "", doc_title_text)
    doc_title_text = re.sub(r"[ ]+", " ", doc_title_text)

    # Convert upper case characters to lower case
    doc_title_text = doc_title_text.casefold()

    # Split the text into whitespace-delimited terms.
    doc_words = doc_title_text.split()

    # Remove stop words
    word_list = []
    for word in doc_words:
        if word not in STOP_WORDS:
            word_list.append(word)

    # Annotate each word belongs to which document
    # map1: word \t {doc_id, frequency}
    for word in word_list:
        value = json.dumps({
            "doc_id": doc_id,
            "tf": 1
        })
        print(f"{word}\t{value}")
