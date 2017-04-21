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
            return [node[3] + 1]
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

    verbose = len(sys.argv) > 3 and sys.argv[3] == '--verbose'

    with open(filename, "r") as datafile:
        data = datafile.read().replace('\n', ' ')
        # Build tree from data file
        if verbose:
            print(data)
            start = time.time()
        
        tree = built_tree(data, False)

        if verbose:
            end = time.time()
            sys.stdout.write("\n")
            
            print_tree(tree, data)
            sys.stdout.write("\n")
            print("Construction Time: %f4" % (end - start))
            print("Size per character (On average): %i" % (sys.getsizeof(data)/len(data)))
            start = time.time()

        result = search(tree, search_string,data)

        if verbose:
            end = time.time()
            print("Search Time: %f4" % (end - start))
            sys.stdout.write("\n")
        
        result.sort()

        
        for i in result:
            sys.stdout.write("%i " % i)

        sys.stdout.write("\n")
