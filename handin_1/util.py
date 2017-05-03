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
        print("Node Range: " + str(_node[2]))
        for n in _node[0]:
            _print_sub(n, depth+1, size, num_nodes)

    _print_sub(node, 0, size, num_nodes)