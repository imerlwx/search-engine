#!/usr/bin/env python3
"""Reduce 2: Calculate tf, idf and norm factor for each term in each doc."""

import sys
import json
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)
    total_norm = 0
    for line in group:
        word_info = line.strip().split('\t')
        json_str = json.loads(word_info[1])
        total_norm += float(json_str["norm"])

    for line in group:
        word_info = line.strip().split('\t')
        json_str = json.loads(word_info[1])
        json_str["norm"] = total_norm
        word_json = json.dumps(json_str, separators=(',', ':'))
        print(f"{key}\t{word_json}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
