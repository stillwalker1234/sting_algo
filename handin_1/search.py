"""
Author: Jacob Bieker and Jonas Tranberg 2017

Using suffix tree for searching in filename

"""
from McM_suffix_tree_build import built_tree
from util import print_tree
import os, sys, time


def search(tree, query, string):
    def report_terminals(node):
        if node[0] == []:
            return [node[3]]
        else:
            ret = []
            for c in node[0]:
                ret += report_terminals(c)

            return ret

    def _search(node, q):
        ret = []
        r = range(*node[2])
        for i in r:
            c, c_q, q = string[i], q[0], q[1:]

            if c != c_q:
                return ret
            elif len(q) == 0:
                return report_terminals(node)

        for c in node[0]:
            ret += _search(c, q)

        return ret

    return _search(tree, query)


if __name__ == "__main__":
    filename = sys.argv[1]
    search_string = sys.argv[2]

    with open(filename, "r") as datafile:
        data = datafile.read().replace('\n', '')
        # Build tree from data file
        print(data)
        start = time.time()
        tree = built_tree(data, False)
        print_tree(tree, data)
        end = time.time()
        print("Construction Time")
        print(end - start)
        print("Size per character (On average): ")
        print(sys.getsizeof(data)/len(data))
        print(search(tree, search_string, data))
