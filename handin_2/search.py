"""
Author: Jacob Bieker and Jonas Tranberg 2017

Using suffix tree for getting tandem repeats

"""
from McM_suffix_tree_build import built_tree
from tandem_repeat_finder import find_tandem_repeats
from util import print_tree, compare_tandem_repeats_result
import sys, time


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

    verbose = len(sys.argv) > 2 and sys.argv[2] == '--verbose'

    with open(filename, "r") as datafile:
        data = datafile.read().replace('\n', ' ')
        # Build tree from data file
        if verbose:
            print(data)
            start = time.time()
        
        tree = built_tree(data, False)

        if False and verbose:
            end = time.time()
            sys.stdout.write("\n")
            
            print_tree(tree, data)
            sys.stdout.write("\n")
            print("Construction Time: %f4" % (end - start))
            print("Size per character (On average): %i" % (sys.getsizeof(data)/len(data)))
            print("Size of suffix tree (on average): %i" % (sys.getsizeof(tree)/len(tree)))
            start = time.time()

        result = find_tandem_repeats(tree, data)

        if verbose:
            out_str = ""

            if verbose:
                end = time.time()
                print("Search Time: %f4" % (end - start))
                sys.stdout.write("\n")
            
            for i in result[0]:
                out_str += "(%i,%i,2) non_branching\n" % i
            
            for i in result[1]:
                out_str += "(%i,%i,2) branching\n" % i

            with open(filename[:-4] + ".out", 'r') as gt_fp:
                compare_tandem_repeats_result(gt_fp, out_str.split('\n'), data)

        sys.stdout.write("%i %i \n" % tuple([len(j) for j in result][::-1]))
