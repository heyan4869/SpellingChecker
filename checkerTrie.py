# author = 'yanhe'


import Trie
import numpy as np
import timeit


def spell_checker(mode, rawfile, dictfile, output):
    word_raw = get_file(rawfile, 'list')
    word_dict = get_file(dictfile, 'set')
    root = Trie.TrieNode()
    for vocab in word_dict:
        root.insert(vocab)
    print 'Finish building Trie.'

    f = open(output, 'w')
    for raw in word_raw:
        if raw in word_dict:
            content = raw + ' ' + str(0) + '\n'
            f.write(content)
        else:
            mtx = np.zeros((1, len(raw)+1))
            for i in xrange(len(raw)+1):
                mtx[0, i] = i
            res, word = get_dist(mode, raw, root, 100, '', mtx)
            content = word + ' ' + str(res) + '\n'
            f.write(content)
    f.close()


def get_dist(mode, raw, node, res, word, mtx):
    if res == 1:
        return res, word
    children_dict = node.children
    for key, value in children_dict.iteritems():
        add_row = [0] * (len(raw)+1)
        add_mtx = np.vstack([mtx, add_row])
        row_num, col_num = add_mtx.shape
        add_mtx[row_num-1, 0] = add_mtx[row_num-2, 0] + 1
        for i in xrange(1, len(raw) + 1):
            if raw[i-1] == key:
                add_mtx[row_num-1, i] = add_mtx[row_num-2, i-1]
            else:
                edit_dist = [add_mtx[row_num-2, i-1], add_mtx[row_num-2, i], add_mtx[row_num-1, i-1]]
                add_mtx[row_num-1, i] = min(edit_dist) + 1
        if value.end:
            if res > add_mtx[row_num-1, len(raw)]:
                res = add_mtx[row_num-1, len(raw)]
                word = value.word
            if len(value.children) != 0:
                res, word = get_dist(mode, raw, value, res, word, add_mtx[row_num-1: row_num])
        else:
            res, word = get_dist(mode, raw, value, res, word, add_mtx[row_num-1: row_num])
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
    spell_checker(1, 'raw.txt', 'dictionary.txt', 'output4.txt')
    end = timeit.default_timer()
    print end - start
