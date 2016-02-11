# author = 'yanhe'


import timeit


def spell_check(mode, rawfile, dictfile, output):
    word_raw = get_file(rawfile, 'list')
    word_dict = get_file(dictfile, 'set')
    f = open(output, 'w')
    for raw in word_raw:
        if raw in word_dict:
            content = raw + ' ' + str(0) + '\n'
            f.write(content)
        else:
            min_dist = 100
            min_correct = ''
            for vocab in word_dict:
                cur_dist = get_dist(mode, raw, vocab)
                if cur_dist < min_dist:
                    min_dist = cur_dist
                    min_correct = vocab
            content = min_correct + ' ' + str(min_dist) + '\n'
            f.write(content)
    f.close()


def get_file(filename, mode):
    print 'Reading', filename
    if mode == 'list':
        vocab = []
        file = open(filename, 'r')
        for line in file:
            vocab.append(line.strip())
        return vocab
    if mode == 'set':
        vocab = set()
        f = open(filename, 'r')
        for line in f:
            vocab.add(line.strip())
        return vocab


def get_dist(mode, word1, word2):
    dp_mtx = [[0 for x in range(len(word2)+1)] for x in range(len(word1)+1)]
    for i in xrange(len(word1)+1):
        dp_mtx[i][0] = i
    for j in xrange(len(word2)+1):
        dp_mtx[0][j] = j
    for i in xrange(1, len(word1)+1):
        for j in xrange(1, len(word2)+1):
            if word1[i-1] == word2[j-1]:
                dp_mtx[i][j] = dp_mtx[i-1][j-1]
            else:
                if mode == 2 and i > 1 and j > 1 and word1[i-1] == word2[j-2] and word1[i-2] == word2[j-1]:
                    edit_list = [dp_mtx[i-1][j-1], dp_mtx[i-1][j], dp_mtx[i][j-1], dp_mtx[i-2][j-2]]
                    dp_mtx[i][j] = min(edit_list) + 1
                else:
                    edit_list = [dp_mtx[i-1][j-1], dp_mtx[i-1][j], dp_mtx[i][j-1]]
                    dp_mtx[i][j] = min(edit_list) + 1
    return dp_mtx[len(word1)][len(word2)]


if __name__ == "__main__":
    start = timeit.default_timer()
    spell_check(2, 'raw.txt', 'dictionary.txt', 'output2.txt')
    end = timeit.default_timer()
    print end - start