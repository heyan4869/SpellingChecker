# author = 'yanhe'


import Trie
import numpy as np
import timeit


def spell_checker(mode, rawfile, dictfile, output):
    word_raw = get_file(rawfile, 'list')
    word_dict = get_file(dictfile, 'set')
    root = build_trie(word_dict)

    f = open(output, 'w')
    for raw in word_raw:
        if raw in word_dict:
            content = raw + ' ' + str(0) + '\n'
        else:
            mtx = np.zeros((1, len(raw)+1))
            for i in xrange(len(raw)+1):
                mtx[0, i] = i
            res, word = get_dist(mode, raw, root, 100, '', mtx)
            content = word + ' ' + str(res) + '\n'
        f.write(content)
    f.close()


def build_trie(word_dict):
    root = Trie.TrieNode()
    for vocab in word_dict:
        root.insert(vocab)
    print 'Finish building Trie.'
    return root


def get_dist(mode, raw, node, res, word, mtx):
    if res == 1:
        return res, word
    children_dict = node.children
    for key, value in children_dict.iteritems():
        cur_mtx = np.zeros((1, len(raw)+1))
        cur_mtx[0, 0] = mtx[0, 0] + 1
        for i in xrange(1, len(raw) + 1):
            if raw[i-1] == key:
                cur_mtx[0, i] = mtx[0, i-1]
            else:
                cur_mtx[0, i] = min(mtx[0, i-1], mtx[0, i], cur_mtx[0, i-1]) + 1
        if value.end:
            if res > cur_mtx[0, len(raw)]:
                res = cur_mtx[0, len(raw)]
                word = value.word
        else:
            res, word = get_dist(mode, raw, value, res, word, cur_mtx)
    return res, word


def get_file(filename, mode):
    print 'Reading', filename
    if mode == 'list':
        vocab = []
        f = open(filename, 'r')
        for line in f:
            vocab.append(line.strip())
        return vocab
    if mode == 'set':
        vocab = set()
        file = open(filename, 'r')
        for line in file:
            vocab.add(line.strip())
        return vocab


if __name__ == '__main__':
    start = timeit.default_timer()
    spell_checker(1, 'raw.txt', 'dictionary.txt', 'output3.txt')
    end = timeit.default_timer()
    print end - start
