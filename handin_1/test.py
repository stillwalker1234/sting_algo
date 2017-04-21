from McM_suffix_tree_build import built_tree
import random
from search import search

def test_McM():
    m = ['a', 'b']
    s = ''.join([m[random.randint(0,1)] for _ in range(40000)])
    t = built_tree(s, False)

    def get_str(node):
        return s[node[2][0]:node[2][1]]

    def is_terminal(node, _s):
        if len(node[0]) == 0 and len(_s) == 0:
            return True
        
        for c in node[0]:
            __s = get_str(c)
            if _s[:len(__s)] == __s:
                return is_terminal(c, _s[len(__s):])
        
        return False

    for i in range(len(s)):
        _s = s[i:]

        assert is_terminal(t, _s), (i, _s)

def test_missippi():
    tree = None
    with open("mississippi.txt", "r") as text:
        s = text.readline()
        tree = built_tree(s, False)
        result = search(tree, "ss",s)
        result.sort()
        output = None
        with open("mississippi.out", "r") as out:
            output = out.readline()
        assert output == result

def test_banana():
    tree = None
    with open("banana.txt", "r") as text:
        s = text.readline()
        tree = built_tree(s, False)
        result = search(tree, "ana",s)
        result.sort()
        output = None
        with open("banana.out", "r") as out:
            output = out.readline()
        assert output == result

def test_walrus():
    tree = None
    with open("walrus-and-carpenter.txt", "r") as text:
        s = text.read().replace('\n', ' ')
        tree = built_tree(s, False)
        result = search(tree, "Walrus",s)
        result.sort()
        output = None
        with open("walrus-and-carpenter.out", "r") as out:
            output = out.readline()
        assert output == result

def test_mariner():
    tree = None
    with open("ancient-mariner.txt", "r") as text:
        s = text.read().replace('\n', ' ')
        tree = built_tree(s, False)
        result = search(tree, "Albatross",s)
        result.sort()
        output = None
        with open("ancient-mariner.out", "r") as out:
            output = out.readline()
        assert output == result

if __name__ == "__main__":
    test_McM()