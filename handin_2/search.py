"""
Author: Jacob Bieker and Jonas Tranberg 2017

Using suffix tree for getting tandem repeats

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


def find_tandem_repeats(tree, string):
    # TODO Add in DFS array
    # Takes a node in a tree, and get the branching tandem repeats, currently, tree holds
    # leaf-list at each node, not DFS numbering
    dfs = []
    def dfs_create(tree):
        """
        Return the DFS numbering of the tree
        :param tree: The tree with leaf-list
        :return: 
        """
        def _depth_first

    def _get_largest_subnode(node):
        # Get v' and its leaf-list to subtract from the leaf-list of v Step 2a
        largest_subnode = None
        largest_subleaflist = (0,0)
        for subnode in node[0]:
            if subnode[2][1] - subnode[2][0] > largest_subleaflist[1] - largest_subleaflist[2]:
                # Larger than the current range, so the largest one
                largest_subleaflist = subnode[2]
                largest_subnode = subnode
        # Now remove the largest sub-leaf-list from the node v's leaf-list, i.e. the children of v and not v'
        leaf_list_prime_v = node[0] - largest_subnode[0]
        leaf_list_prime_v = []
        # Now have list of child nodes not in the largest subnode, not leaf-list though. Leaf list would just be range?
        new_range_start = (node[2][0], largest_subnode[2][0] - node[2][0])
        new_range_end = (node[2][1] - largest_subnode[2][1], node[2][1])
        # new_range_start, new_range_end are the ranges of leafs not under LL(v')
        for i in range(new_range_start[0], new_range_start[1]):
            leaf_list_prime_v.append(i)
        for i in range(new_range_end[0], new_range_end[0]):
            leaf_list_prime_v.append(i)
        return leaf_list_prime_v

    def _step_2(leaf_list_prime, leaf_list, depth, foreward):
        """
        
        :param leaf_list_prime: the list of leafs in LL'(v)
        :param leaf_list: the list of leafs in LL(v)
        :param depth: Depth of node v
        :param foreward: whether to do foreward or backwards search, boolean
        :return: list of tandem repeats and their lengths
        """
        # Get the leaf number for every leaf in the list, that number + depth gives whether its in the big leaf-list
        tandem_repeats = []
        # Steps 2b and 2c: For each leaf i in LL'(v), test whether leaf j = i +- D(v) is in LL(v)
        for leaf in leaf_list_prime:
            if foreward:
                if leaf + depth in leaf_list:
                    # First check is true
                    if string[leaf] != string[leaf + 2*depth]:
                        # Check whether S[i] != S[i + 2D(v)]
                        tandem_repeats.append([leaf, 2*depth])
            else:
                if leaf - depth in leaf_list:
                    # First check is true
                    if string[leaf] != string[leaf + 2*depth]:
                        # Check whether S[i] != S[i + 2D(v)]
                        tandem_repeats.append([leaf, 2*depth])
        return tandem_repeats




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
            print("Size of suffix tree (on average): %i" % (sys.getsizeof(tree)/len(tree)))
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
