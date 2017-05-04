import sys

def print_tree(node, _str):
    # Add size
    size = 0
    num_nodes = 0
    def _print_sub(_node, depth, size, num_nodes):
        size += sys.getsizeof(node)
        num_nodes += 1
        print(('_' * depth) + str(_node[4]) + " : " + _str[_node[2][0]:_node[2][1]] + " : " + (str(_node[3]) if not type(_node[3]) is list else ""))
        for n in _node[0]:
            _print_sub(n, depth+1, size, num_nodes)

    _print_sub(node, 0, size, num_nodes)


def append_leaf_lists(root, str_size):
    count = [0]
    # Should create a list of length equal to the number of nodes, which will be more than the number of leaves, but
    # can just ignore the other stuff for now
    dfs2leaf_id = [0] * str_size
    leaf_id2_dfs = [0] * str_size

    def _inner(node):
        if node[0] == []:
            # Assigns the dfs number for the leaf to the array, indexed at the leaf-list number
            # Currently, they seem to be the same.... so not sure the usefulness
            dfs2leaf_id[count[0]] = node[-1]
            leaf_id2_dfs[node[-1]] = count[0]
            node.append((count[0], count[0]))
            count[0] += 1

        else:
            # Not a child node
            # Add next DFS number to the internal node as the start of the range of leafs it covers
            ranges = map(_inner, node[0])
            node.append((ranges[0][0], ranges[-1][-1]))
            # Append the last dfs_count to the internal node as the end of the range of leafs it covers
            # I think -2 is right because of the append(sum(map)) thing should be last
            # dfs_count should be updated from _inner so it is the last one it includes
        return node[-1]

    _inner(root)

    return dfs2leaf_id, leaf_id2_dfs
