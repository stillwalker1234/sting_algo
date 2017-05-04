"""
Author: Jacob Bieker and Jonas Tranberg 2017

Using suffix tree for getting tandem repeats

"""
from McM_suffix_tree_build import built_tree
from util import print_tree
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


def find_tandem_repeats(tree, string, d2l_map, l2d_map):
    """
    return list [[non_branching], [branching]]
    """

    # Takes a node in a tree, and get the branching tandem repeats
    def _leaf_list_len(node):
        return node[4][1] - node[4][0]
    
    def _get_largest_subnode(node):
        # Get v' and its leaf-list to subtract from the leaf-list of v Step 2a
        largest = node[0][0]

        for subnode in node[0][1:]:
            if _leaf_list_len(subnode) > _leaf_list_len(largest):
                # Larger than the current range, so the largest one
                largest = subnode
        # Now remove the largest sub-leaf-list from the node v's leaf-list, i.e. the leaves of v and not v'
        leaf_list_prime_v = range(node[4][0], largest[4][0]) + range(largest[4][1], node[4][1])

        return leaf_list_prime_v

    def _step_2(leaf_list_prime, depth, v, foreward):
        """
        
        :param leaf_list_prime: the list of leafs in LL'(v)
        :param depth: Depth of node v
        :param d2l_map: d2l_map array, indexed by leaf-list number
        :param v: Node v, the root of the subtree we are looking at
        :param foreward: whether to do foreward or backwards search, boolean
        :return: list of tandem repeats and their lengths
        """
        # Get the leaf number for every leaf in the list, that number + depth gives whether its in the big leaf-list
        tandem_repeats = []
        # Steps 2b and 2c: For each leaf i in LL'(v), test whether leaf j = i +- D(v) is in LL(v)
        # To do that, just check whether, for leaf j, d2l_map[j] is between the d2l_map values recorded at v
        for leaf in leaf_list_prime:
            if foreward:
                i = d2l_map[leaf]
                j = i + depth
                if not (v[4][1] >= l2d_map[j] >= v[4][0]):
                    continue
            else:
                j = d2l_map[leaf]
                i = j - depth
                if not (v[4][1] >= l2d_map[i] >= v[4][0]):
                    continue
                # Checking if DFS[j] is between the ranges of DFS numbers stored at v
                    # First check is true
            if string[i] != string[i + 2*depth]:
                # Check whether S[i] != S[i + 2D(v)]
                # Second check is true, so tandem repeat
                tandem_repeats.append((i, depth))
           
        return tandem_repeats

    def _find_nonbranching_repeat(tandem_repeats, string, depth):
        """
        Get the non-branching tandem repeats through enumeration
        :param tandem_repeats: The list of tandem repeats
        :param string: The string used in the tree and tandem repeats
        :return: List containing all tandem repeats, branching and non-branching
        """
        ret = []
        for repeat in tandem_repeats:
            # For tandem repeat (i, wa, 2), see if S[i - 1] = a
            # If so, then non-branching repeat is (i - 1, aw, 2)
            cur_pos = repeat[0]-1

            while cur_pos >= 0 and string[cur_pos] == string[cur_pos + repeat[1]]:
                ret.append((cur_pos, depth))
                cur_pos -= 1

        return ret
    
    tandem_repeats = [[], []]

    def _inner(node, depth=0):
        """
        Iterates through the tree, calling the other functions to find tandem repeats
        :param node: Node of the tree
        :return: The list of tandem repeats and their locations
        """
        # TODO Still need to mark the nodes that we visit
        # TODO Possible problem with going down two depths at once? (Current Node -> subnode(children) -> looks at subnode's subnodes
        if node[0] == []:
            pass
        else:
            for subnode in node[0]:
                _inner(subnode, depth+subnode[2][1]-subnode[2][0])
            
            # Get the branching tandem repeats
            leaf_list_prime = _get_largest_subnode(node)
            tandem_repeat_list = []
            tandem_repeat_list += _step_2(leaf_list_prime, depth, node, True)
            tandem_repeat_list += _step_2(leaf_list_prime, depth, node, False)
            
            tandem_repeats[0] += _find_nonbranching_repeat(tandem_repeat_list, string, depth)
            tandem_repeats[1] += tandem_repeat_list

    _inner(tree)

    return tandem_repeats


if __name__ == "__main__":
    filename = sys.argv[1]

    verbose = len(sys.argv) > 2 and sys.argv[2] == '--verbose'

    with open(filename, "r") as datafile:
        data = datafile.read().replace('\n', ' ')
        # Build tree from data file
        if verbose:
            print(data)
            start = time.time()
        
        tree, (d2l_map, l2d_map) = built_tree(data, False)

        if verbose:
            end = time.time()
            sys.stdout.write("\n")
            
            print_tree(tree, data)
            sys.stdout.write("\n")
            print("Construction Time: %f4" % (end - start))
            print("Size per character (On average): %i" % (sys.getsizeof(data)/len(data)))
            print("Size of suffix tree (on average): %i" % (sys.getsizeof(tree)/len(tree)))
            start = time.time()

        result = find_tandem_repeats(tree, data, d2l_map, l2d_map)

        if verbose:
            end = time.time()
            print("Search Time: %f4" % (end - start))
            sys.stdout.write("\n")
        

        for i in result[0]:
            sys.stdout.write("non_branching: (%i, %i, 2) \n" % i)
        
        for i in result[1]:
            sys.stdout.write("branching: (%i, %i, 2) \n" % i)

        sys.stdout.write("%i %i \n" % tuple([len(j) for j in result][::-1]))
