# author = 'yanhe'


class TrieNode:
    def __init__(self):
        self.char = None
        self.children = {}
        self.end = False
        self.word = None

    def set(self, letter):
        node = self
        node.char = letter

    def insert(self, word):
        node = self
        children_dict = node.children
        for i in xrange(len(word)):
            c = word[i]

            if c in children_dict:
                t = children_dict[c]
            else:
                t = TrieNode()
                t.set(c)
                children_dict[c] = t
            children_dict = t.children

            if i == len(word) - 1:
                t.end = True
                t.word = word
