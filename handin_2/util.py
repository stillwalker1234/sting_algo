import sys

def print_tree(node, _str):
    # Add size
    size = 0
    num_nodes = 0
    def _print_sub(_node, depth, size, num_nodes):
        size += sys.getsizeof(node)
        num_nodes += 1
        print(('_' * depth) + str(_node[2]) + " : " + _str[_node[2][0]:_node[2][1]] + " : " + (str(_node[3]) if not type(_node[3]) is list else ""))
        print(size/num_nodes)
        for n in _node[0]:
            _print_sub(n, depth+1, size, num_nodes)

    _print_sub(node, 0, size, num_nodes)

def append_leaf_lists(root):
    count = [0]
    # Should create a list of length equal to the number of nodes, which will be more than the number of leaves, but
    # can just ignore the other stuff for now
    dfs = [0] * len(root[0])
    dfs_counter = 0

    def _inner(node, dfs_count):
        if node[0] == []:
            # Adds the successive DFS ordering number to the node if its a leaf
            dfs_count += 1
            # So should be second-to-last in the node, same as the DFS range in the internal nodes
            node.append(dfs_count)
            # Added above the count, so node[-1] gives the leaf-list count and not DFS count
            node.append([count])
            count[0] += 1
            # Assigns the dfs number for the leaf to the array, indexed at the leaf-list number
            # Currently, they seem to be the same.... so not sure the usefulness
            dfs[count[0]] = dfs_count
        else:
            # Not a child node
            # Add next DFS number to the internal node as the start of the range of leafs it covers
            node.append([dfs_count+1])
            node.append(sum(map(_inner, node[0]), []))
            # Append the last dfs_count to the internal node as the end of the range of leafs it covers
            # I think -2 is right because of the append(sum(map)) thing should be last
            # dfs_count should be updated from _inner so it is the last one it includes
            node[-2].append(dfs_count)

        return node[-1]

    _inner(root, dfs_counter)
