from McM_suffix_tree_build import built_tree
import random

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


if __name__ == "__main__":
    test_McM()