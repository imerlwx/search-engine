#!/usr/bin/env python3
"""Reduce 1: Parse each word into word \t {docid1: frequency1, ...}."""

import sys
import json
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""
    term_dict = {}
    for line in group:
        word = line.split('\t')[0]
        value_json = json.loads(line.split('\t')[1])
        doc_id = value_json['doc_id']
        tf = value_json['tf']
        if word not in term_dict:
            term_dict[word] = {doc_id: tf}
        else:
            if doc_id not in term_dict[word]:
                term_dict[word][doc_id] = tf
            else:
                term_dict[word][doc_id] += tf

    for word, id_tf_pair in term_dict.items():
        id_tf_pair_json = json.dumps(id_tf_pair, separators=(',', ':'))
        print(f"{key}\t{id_tf_pair_json}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
