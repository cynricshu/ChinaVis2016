import os
import lda.utils

_test_dir = "/Users/cynric/workspaces/Python/ChinaVis2016/data/topic"


def load_reuters():
    reuters_ldac_fn = os.path.join(_test_dir, 'subject2.ldac')
    return lda.utils.ldac2dtm(open(reuters_ldac_fn), offset=0)


def load_reuters_vocab():
    reuters_vocab_fn = os.path.join(_test_dir, 'subject2.tokens')
    with open(reuters_vocab_fn) as f:
        vocab = tuple(f.read().split())
    return vocab


def load_reuters_titles():
    reuters_titles_fn = os.path.join(_test_dir, 'subject2.txt')
    with open(reuters_titles_fn) as f:
        titles = tuple(line.strip() for line in f.readlines())
    return titles
