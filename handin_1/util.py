def print_tree(node, _str):
    def _print_sub(_node, depth):
        print(('_' * depth) + str(_node[2]) + " : " + _str[_node[2][0]:_node[2][1]] + " : " + (str(_node[3]) if not type(_node[3]) is list else ""))
        
        for n in _node[0]:
            _print_sub(n, depth+1)

    _print_sub(node, 0)