import os
import lda.utils

_test_dir = "data/topic"
ldac = 'subject2_w_date.ldac'
tokens = 'subject2_w_date.tokens'
title = 'subject2_w_date.txt'


def load_reuters():
    reuters_ldac_fn = os.path.join(_test_dir, ldac)
    return lda.utils.ldac2dtm(open(reuters_ldac_fn), offset=0)


def load_reuters_vocab():
    reuters_vocab_fn = os.path.join(_test_dir, tokens)
    with open(reuters_vocab_fn) as f:
        vocab = tuple(f.read().split())
    return vocab


def load_reuters_titles():
    reuters_titles_fn = os.path.join(_test_dir, title)
    with open(reuters_titles_fn) as f:
        titles = tuple(line.strip() for line in f.readlines())
    return titles
