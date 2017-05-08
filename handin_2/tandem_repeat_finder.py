"""
Author: Jonas Tranberg and Jacob Bieker 2017 

Implementation of tandem repeat finder in O(nlog(n)) time

"""


def find_tandem_repeats(tree, string):
    """
    return list [[non_branching], [branching]]
    """

    def append_leaf_lists(root, str_size):
        """
        creates the dfs numbering of each leaf, and add implicit child ranges to internal nodes
        returns: map from dfs numbering to leaf numbering,
                 map from leaf numbering to dfs numbering
        """

        count = [0]
        dfs2leaf_id = [0] * str_size
        leaf_id2_dfs = [0] * str_size

        def _inner(node):
            if node[0] == []:
                dfs2leaf_id[count[0]] = node[-1]
                leaf_id2_dfs[node[-1]] = count[0]

                node.append((count[0], count[0]))
                count[0] += 1
            else:
                ranges = list(map(_inner, node[0]))
                node.append((ranges[0][0], ranges[-1][-1]))
            return node[-1]

        _inner(root)

        return dfs2leaf_id, leaf_id2_dfs

    d2l_map, l2d_map = append_leaf_lists(tree, len(string))

    def _leaf_list_len(node):
        return node[-1][1] - node[-1][0]
    
    def _get_LL_small_range(node):
        largest = node[0][0]

        # find largest child node
        for subnode in node[0][1:]:
            if _leaf_list_len(subnode) > _leaf_list_len(largest):
                largest = subnode

        # return range excluding largest child node
        leaf_list_prime_v = list(range(node[-1][0], largest[-1][0])) + list(range(largest[-1][1]+1, node[-1][1]+1))

        return leaf_list_prime_v

    def _step_2(leaf_list_prime, depth, v):
        """
        
        :param leaf_list_prime: the list of leafs in LL'(v)
        :param depth: Depth of node v
        :param v: Node v, the root of the subtree we are looking at
        :return: list of tandem repeats and their lengths
        """
        node_dfs_range = v[-1]
        tandem_repeats = set()

        for leaf in leaf_list_prime:
            # first try if d2l_map[leaf] == i
            i = d2l_map[leaf]
            j = i + depth
            if not (node_dfs_range[1] >= l2d_map[j] >= node_dfs_range[0]):
                # that did not work out so check d2l_map[leaf] == j
                j = d2l_map[leaf]
                i = j - depth
                if not (node_dfs_range[1] >= l2d_map[i] >= node_dfs_range[0]) or ((i, depth) in tandem_repeats):
                    # either d2l_map[leaf] == j didnt work out or the tandem repeat was allready there, so we continue
                    continue
            
            # First check is true (there is a tandem repeat), now check if its branching
            if string[i] != string[i + 2*depth]:
                tandem_repeats.add((i, depth))
           
        return list(tandem_repeats)

    def _find_nonbranching_repeat(tandem_repeats, string, depth):
        """
        Get the non-branching tandem repeats through enumeration
        :param tandem_repeats: The list of tandem repeats
        :param string: The string used in the tree and tandem repeats
        :return: List containing all tandem repeats, branching and non-branching
        """
        ret = []
        for tandem_repeat in tandem_repeats:
            # For tandem_repeat (i, wa, 2), see if S[i - 1] = a
            # If so, then non-branching tandem_repeat is (i - 1, aw, 2)
            cur_pos = tandem_repeat[0]-1

            while cur_pos >= 0 and string[cur_pos] == string[cur_pos + tandem_repeat[1]]:
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
        if node[0] == []:
            pass
        else:
            for subnode in node[0]:
                node_range = subnode[2]
                _inner(subnode, depth+node_range[1]-node_range[0])
            
            tandem_repeat_list = _step_2(_get_LL_small_range(node), depth, node)

            tandem_repeats[0] += _find_nonbranching_repeat(tandem_repeat_list, string, depth)
            tandem_repeats[1] += tandem_repeat_list
    
    _inner(tree)

    return tandem_repeats

