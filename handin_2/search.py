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


def find_tandem_repeats(tree, string, dfs):

    tandem_repeat_list = []
    depth_count = 0
    # Takes a node in a tree, and get the branching tandem repeats
    def _get_largest_subnode(node):
        # Get v' and its leaf-list to subtract from the leaf-list of v Step 2a
        largest_subleaflist = []
        for subnode in node[0]:
            if len(subnode[-1]) > len(largest_subleaflist):
                # Larger than the current range, so the largest one
                largest_subleaflist = subnode[-1]
        # Now remove the largest sub-leaf-list from the node v's leaf-list, i.e. the leaves of v and not v'
        leaf_list_prime_v = [leaf for leaf in node[-1] if leaf not in largest_subleaflist]
        return leaf_list_prime_v

    def _step_2(leaf_list_prime, depth, dfs, v, foreward):
        """
        
        :param leaf_list_prime: the list of leafs in LL'(v)
        :param depth: Depth of node v
        :param dfs: DFS array, indexed by leaf-list number
        :param v: Node v, the root of the subtree we are looking at
        :param foreward: whether to do foreward or backwards search, boolean
        :return: list of tandem repeats and their lengths
        """
        # Get the leaf number for every leaf in the list, that number + depth gives whether its in the big leaf-list
        tandem_repeats = []
        # Steps 2b and 2c: For each leaf i in LL'(v), test whether leaf j = i +- D(v) is in LL(v)
        # To do that, just check whether, for leaf j, DFS[j] is between the DFS values recorded at v
        for leaf in leaf_list_prime:
            if foreward:
                # Checking if DFS[j] is between the ranges of DFS numbers stored at v
                if v[-2][1] > dfs[leaf + depth] > v[-2][0]:
                    # First check is true
                    if string[leaf] != string[leaf + 2*depth]:
                        # Check whether S[i] != S[i + 2D(v)]
                        # Second check is true, so tandem repeat
                        tandem_repeats.append([leaf, 2*depth])
            else:
                # Checking if DFS[j] is between the ranges of DFS numbers stored at v
                if v[-2][1] > dfs[leaf + depth] > v[-2][0]:
                    # First check is true
                    if string[leaf] != string[leaf + 2*depth]:
                        # Check whether S[i] != S[i + 2D(v)]
                        # Second check is true, so tandem repeat
                        tandem_repeats.append([leaf, string[leaf], 2*depth])
        return tandem_repeats

    def _find_nonbranching_repeat(tandem_repeats, string):
        """
        Get the non-branching tandem repeats through enumeration
        :param tandem_repeats: The list of tandem repeats
        :param string: The string used in the tree and tandem repeats
        :return: List containing all tandem repeats, branching and non-branching
        """
        for repeat in tandem_repeats:
            # For tandem repeat (i, wa, 2), see if S[i - 1] = a
            # If so, then non-branching repeat is (i - 1, aw, 2)
            if string[repeat[0] - 1] == string[repeat[0]][-1]:
                # Tandem repeat
                # Pretty sure the comparision is wrong, and should use while loop instead
                tandem_repeats.append([repeat[0] - 1, string[repeat[0][-1], repeat[2]]])

        return tandem_repeats

    def _inner(node, tandem_repeats):
        """
        Iterates through the tree, calling the other functions to find tandem repeats
        :param node: Node of the tree
        :return: The list of tandem repeats and their locations
        """
        # TODO Still need to mark the nodes that we visit
        # TODO Possible problem with going down two depths at once? (Current Node -> subnode(children) -> looks at subnode's subnodes
        for subnode in node[0]:
            # Go through each subnode
            if subnode[0] != []:
                # Is internal node, so tandem repeat finding here
                leaf_list_prime = _get_largest_subnode(subnode)
                # Get the branching tandem repeats
                tandem_repeats.append(_step_2(leaf_list_prime, depth_count, dfs, subnode, True))
                tandem_repeats.append(_step_2(leaf_list_prime, depth_count, dfs, subnode, False))

                #Continue down the subnodes
                _inner(subnode)
            # Once all tandem branching repeats found, now go for non-branching ones
            tandem_repeats = _find_nonbranching_repeat(tandem_repeat_list, string)

        return tandem_repeats
    tandem_repeat_list = _inner(tree, tandem_repeat_list)





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
