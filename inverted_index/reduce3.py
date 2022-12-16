#!/usr/bin/env python3
"""Reduce 3: Make inverted index with format: word idf docid1 tf1 norm1... ."""

import sys
import json
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""
    i = 0
    group_list = list(group)

    for line in group_list:
        word_info = line.strip().split('\t')
        json_str = json.loads(word_info[1])
        i += 1
        if i == 1:  # If it is the first line, print the term and idf
            print(f"{key} {json_str['idf']}", end='')

        if i == len(group_list):  # If it is the last line, print the newline
            print(f" {json_str['doc_id']} {json_str['tf']} {json_str['norm']}")
        else:
            print(f" {json_str['doc_id']} {json_str['tf']} \
                  {json_str['norm']}", end='')


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    word_info = line.strip().split('\t')
    json_str = json.loads(word_info[1])
    return json_str["word"]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
